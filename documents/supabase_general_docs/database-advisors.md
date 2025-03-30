Database

# Performance and Security Advisors

## Check your database for performance and security issues

* * *

You can use the Database Performance and Security Advisors to check your database for issues such as missing indexes and improperly set-up RLS policies.

## Using the Advisors [\#](https://supabase.com/docs/guides/database/database-advisors\#using-the-advisors)

In the dashboard, navigate to [Security Advisor](https://supabase.com/dashboard/project/_/database/security-advisor) and [Performance Advisor](https://supabase.com/dashboard/project/_/database/performance-advisor) under Database. The advisors run automatically. You can also manually rerun them after you've resolved issues.

## Available checks [\#](https://supabase.com/docs/guides/database/database-advisors\#available-checks)

0001 unindexed foreign keys0002 auth users exposed0003 auth rls initplan0004 no primary key0005 unused index0006 multiple permissive policies0007 policy exists rls disabled0008 rls enabled no policy0009 duplicate index0010 security definer view0011 function search path mutable0012 auth allow anonymous sign ins0013 rls disabled in public0014 extension in public0015 rls references user metadata0016 materialized view in api0017 foreign table in api0018 unsupported reg types0019 insecure queue exposed in api0020 table bloat0021 fkey to auth unique

Level: INFO

### Rationale [\#](https://supabase.com/docs/guides/database/database-advisors\#rationale)

In relational databases, indexing foreign key columns is a standard practice for improving query performance. Indexing these columns is recommended in most cases because it improves query join performance along a declared relationship.

### What is a Foreign Key? [\#](https://supabase.com/docs/guides/database/database-advisors\#what-is-a-foreign-key)

A foreign key is a constraint on a column (or set of columns) that enforces a relationship between two tables. For example, a foreign key from `book.author_id` to `author.id` enforces that every value in `book.author_id` exists in `author.id`. Once the foriegn key is declared, it is not possible to insert a value into `book.author_id` that does not exist in `author.id`. Similarly, Postgres will not allow us to delete a value from `author.id` that is referenced by `book.author_id`. This concept is known as referential integrity.

### Why Index Foreign Key Columns? [\#](https://supabase.com/docs/guides/database/database-advisors\#why-index-foreign-key-columns)

Given that foreign keys define relationships among tables, it is common to use foreign key columns in join conditions when querying the database. Adding an index to the columns making up the foreign key improves the performance of those joins and reduces database resource consumption.

```flex

1
2
3
4
5
6
7
8
9
10
select    book.id,    book.title,    author.namefrom    book    join author        -- Both sides of the following condition should be indexed        -- for best performance        on book.author_id = author.id
```

### How to Resolve [\#](https://supabase.com/docs/guides/database/database-advisors\#how-to-resolve)

Given a table:

```flex

1
2
3
4
5
create table book (    id serial primary key,    title text not null,    author_id int references author(id) -- this defines the foreign key);
```

To apply the best practice of indexing foreign keys, an index is needed on the `book.author_id` column. We can create that index using:

```flex

1
create index ix_book_author_id on book(author_id);
```

In this case we used the default B-tree index type. Be sure to choose an index type that is appropriate for the data types and use case when working with your own tables.

### Example [\#](https://supabase.com/docs/guides/database/database-advisors\#example)

Let's look at a practical example involving two tables: `order_item` and `customer`, where `order_item` references `customer`.

Given the schema:

```flex

1
2
3
4
5
6
7
8
9
10
create table customer (    id serial primary key,    name text not null);create table order_item (    id serial primary key,    order_date date not null,    customer_id integer not null references customer (id));
```

We expect the tables to be joined on the condition

```flex

1
customer.id = order_item.customer_id
```

As in:

```flex

1
2
3
4
5
6
7
select    customer.name,    order_item.order_datefrom    customer    join order_item        on customer.id = order_item.customer_id
```

Using Postgres' "explain plan" functionality, we can see how its query planner expects to execute the query.

```flex

1
2
3
4
5
Hash Join  (cost=38.58..74.35 rows=2040 width=36)  Hash Cond: (order_item.customer_id = customer.id)  ->  Seq Scan on order_item  (cost=0.00..30.40 rows=2040 width=8)  ->  Hash  (cost=22.70..22.70 rows=1270 width=36)        ->  Seq Scan on customer  (cost=0.00..22.70 rows=1270 width=36)
```

Notice that the condition `order_item.customer_id = customer.id` is being serviced by a `Seq Scan`, a sequential scan across the `order_items` table. That means Postgres intends to sequentially iterate over each row in the table to identify the value of `customer_id`.

Next, if we index `order_item.customer_id` and recompute the query plan:

```flex

1
2
3
4
5
6
7
8
9
10
create index ix_order_item_customer_id on order_item(customer_id);explainselect    customer.name,    order_item.order_datefrom    customer    join order_item        on customer.id = order_item.customer_id
```

We get the query plan:

```flex

1
2
3
4
5
Hash Join  (cost=38.58..74.35 rows=2040 width=36)  Hash Cond: (order_item.customer_id = customer.id)  ->  Seq Scan on order_item  (cost=0.00..30.40 rows=2040 width=8)  ->  Hash  (cost=22.70..22.70 rows=1270 width=36)        ->  Seq Scan on customer  (cost=0.00..22.70 rows=1270 width=36)
```

Note that nothing changed.

We get an identical result because Postgres' query planner is clever enough to know that a `Seq Scan` over an empty table is extremely fast, so theres no reason for it to reach out to an index. As more rows are inserted into the `order_item` table the tradeoff between sequentially scanning and retriving the index steadily tip in favor of the index. Rather than manually finding this inflection point, we can hint to the query planner that we'd like to use indexes by disabling sequentials scans except where they are the only available option. To provides that hint we can use:

```flex

1
set local enable_seqscan = off;
```

With that change:

```flex

1
2
3
4
5
6
7
8
9
10
set local enable_seqscan = off;explainselect    customer.name,    order_item.order_datefrom    customer    join order_item        on customer.id = order_item.customer_id
```

We get the query plan:

```flex

1
2
3
4
5
Hash Join  (cost=79.23..159.21 rows=2040 width=36)  Hash Cond: (order_item.customer_id = customer.id)  ->  Index Scan using ix_order_item_customer_id on order_item  (cost=0.15..74.75 rows=2040 width=8)  ->  Hash  (cost=63.20..63.20 rows=1270 width=36)        ->  Index Scan using customer_pkey on customer  (cost=0.15..63.20 rows=1270 width=36)
```

The new plan services the `order_item.customer_id = customer.id` join condition using an `Index Scan` on `ix_order_item_customer_id` which is far more efficient at scale.

### Is this helpful?

NoYes

### On this page

[Using the Advisors](https://supabase.com/docs/guides/database/database-advisors#using-the-advisors) [Available checks](https://supabase.com/docs/guides/database/database-advisors#available-checks) [Rationale](https://supabase.com/docs/guides/database/database-advisors#rationale) [What is a Foreign Key?](https://supabase.com/docs/guides/database/database-advisors#what-is-a-foreign-key) [Why Index Foreign Key Columns?](https://supabase.com/docs/guides/database/database-advisors#why-index-foreign-key-columns) [How to Resolve](https://supabase.com/docs/guides/database/database-advisors#how-to-resolve) [Example](https://supabase.com/docs/guides/database/database-advisors#example)

1. We use first-party cookies to improve our services. [Learn more](https://supabase.com/privacy#8-cookies-and-similar-technologies-used-on-our-european-services)



   [Learn more](https://supabase.com/privacy#8-cookies-and-similar-technologies-used-on-our-european-services)•Privacy settings





   AcceptOpt outPrivacy settings