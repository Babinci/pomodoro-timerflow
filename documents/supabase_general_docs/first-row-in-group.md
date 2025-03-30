Database

# Select first row for each group in PostgreSQL

* * *

Given a table `seasons`:

| id | team | points |
| --- | :-: | --: |
| 1 | Liverpool | 82 |
| 2 | Liverpool | 84 |
| 3 | Brighton | 34 |
| 4 | Brighton | 28 |
| 5 | Liverpool | 79 |

We want to find the rows containing the maximum number of points _per team_.

The expected output we want is:

| id | team | points |
| --- | :-: | --: |
| 3 | Brighton | 34 |
| 2 | Liverpool | 84 |

From the [SQL Editor](https://supabase.com/dashboard/project/_/sql), you can run a query like:

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
select distinct  on (team) id,  team,  pointsfrom  seasonsorder BY  id,  points desc,  team;
```

The important bits here are:

- The `desc` keyword to order the `points` from highest to lowest.
- The `distinct` keyword that tells Postgres to only return a single row per team.

This query can also be executed via `psql` or any other query editor if you prefer to [connect directly to the database](https://supabase.com/docs/guides/database/connecting-to-postgres#direct-connections).

### Is this helpful?

NoYes