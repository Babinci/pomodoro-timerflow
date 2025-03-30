Local Development

# Advanced pgTAP Testing

* * *

While basic pgTAP provides excellent testing capabilities, you can enhance the testing workflow using database development tools and helper packages. This guide covers advanced testing techniques using database.dev and community-maintained test helpers.

## Using database.dev [\#](https://supabase.com/docs/guides/local-development/testing/pgtap-extended\#using-databasedev)

[Database.dev](https://database.dev/) is a package manager for Postgres that allows installation and use of community-maintained packages, including testing utilities.

### Setting up dbdev [\#](https://supabase.com/docs/guides/local-development/testing/pgtap-extended\#setting-up-dbdev)

To use database development tools and packages, install some prerequisites:

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
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
create extension if not exists http with schema extensions;create extension if not exists pg_tle;drop extension if exists "supabase-dbdev";select pgtle.uninstall_extension_if_exists('supabase-dbdev');select    pgtle.install_extension(        'supabase-dbdev',        resp.contents ->> 'version',        'PostgreSQL package manager',        resp.contents ->> 'sql'    )from http(    (        'GET',        'https://api.database.dev/rest/v1/'        || 'package_versions?select=sql,version'        || '&package_name=eq.supabase-dbdev'        || '&order=version.desc'        || '&limit=1',        array[            ('apiKey', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhtdXB0cHBsZnZpaWZyYndtbXR2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODAxMDczNzIsImV4cCI6MTk5NTY4MzM3Mn0.z2CN0mvO2No8wSi46Gw59DFGCTJrzM0AQKsu_5k134s')::http_header        ],        null,        null    )) x,lateral (    select        ((row_to_json(x) -> 'content') #>> '{}')::json -> 0) resp(contents);create extension "supabase-dbdev";select dbdev.install('supabase-dbdev');-- Drop and recreate the extension to ensure a clean installationdrop extension if exists "supabase-dbdev";create extension "supabase-dbdev";
```

### Installing test helpers [\#](https://supabase.com/docs/guides/local-development/testing/pgtap-extended\#installing-test-helpers)

The Test Helpers package provides utilities that simplify testing Supabase-specific features:

```flex

1
2
select dbdev.install('basejump-supabase_test_helpers');create extension if not exists "basejump-supabase_test_helpers" version '0.0.6';
```

## Test helper benefits [\#](https://supabase.com/docs/guides/local-development/testing/pgtap-extended\#test-helper-benefits)

The test helpers package provides several advantages over writing raw pgTAP tests:

1. **Simplified User Management**
   - Create test users with `tests.create_supabase_user()`
   - Switch contexts with `tests.authenticate_as()`
   - Retrieve user IDs using `tests.get_supabase_uid()`
2. **Row Level Security (RLS) Testing Utilities**
   - Verify RLS status with `tests.rls_enabled()`
   - Test policy enforcement
   - Simulate different user contexts
3. **Reduced Boilerplate**
   - No need to manually insert auth.users
   - Simplified JWT claim management
   - Clean test setup and cleanup

## Schema-wide Row Level Security testing [\#](https://supabase.com/docs/guides/local-development/testing/pgtap-extended\#schema-wide-row-level-security-testing)

When working with Row Level Security, it's crucial to ensure that RLS is enabled on all tables that need it. Create a simple test to verify RLS is enabled across an entire schema:

```flex

1
2
3
4
5
6
7
8
begin;select plan(1);-- Verify RLS is enabled on all tables in the public schemaselect tests.rls_enabled('public');select * from finish();rollback;
```

## Test file organization [\#](https://supabase.com/docs/guides/local-development/testing/pgtap-extended\#test-file-organization)

When working with multiple test files that share common setup requirements, it's beneficial to create a single "pre-test" file that handles the global environment setup. This approach reduces duplication and ensures consistent test environments.

### Creating a pre-test hook [\#](https://supabase.com/docs/guides/local-development/testing/pgtap-extended\#creating-a-pre-test-hook)

Since pgTAP test files are executed in alphabetical order, create a setup file that runs first by using a naming convention like `000-setup-tests-hooks.sql`:

```flex

1
supabase test new 000-setup-tests-hooks
```

This setup file should contain:

1. All shared extensions and dependencies
2. Common test utilities
3. A simple always green test to verify the setup

Here's an example setup file:

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
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
-- install tests utilities-- install pgtap extension for testingcreate extension if not exists pgtap with schema extensions;/*------------------------- install dbdev --------------------------Requires:  - pg_tle: https://github.com/aws/pg_tle  - pgsql-http: https://github.com/pramsey/pgsql-http*/create extension if not exists http with schema extensions;create extension if not exists pg_tle;drop extension if exists "supabase-dbdev";select pgtle.uninstall_extension_if_exists('supabase-dbdev');select    pgtle.install_extension(        'supabase-dbdev',        resp.contents ->> 'version',        'PostgreSQL package manager',        resp.contents ->> 'sql'    )from http(    (        'GET',        'https://api.database.dev/rest/v1/'        || 'package_versions?select=sql,version'        || '&package_name=eq.supabase-dbdev'        || '&order=version.desc'        || '&limit=1',        array[            ('apiKey', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhtdXB0cHBsZnZpaWZyYndtbXR2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODAxMDczNzIsImV4cCI6MTk5NTY4MzM3Mn0.z2CN0mvO2No8wSi46Gw59DFGCTJrzM0AQKsu_5k134s')::http_header        ],        null,        null    )) x,lateral (    select        ((row_to_json(x) -> 'content') #>> '{}')::json -> 0) resp(contents);create extension "supabase-dbdev";select dbdev.install('supabase-dbdev');drop extension if exists "supabase-dbdev";create extension "supabase-dbdev";-- Install test helpersselect dbdev.install('basejump-supabase_test_helpers');create extension if not exists "basejump-supabase_test_helpers" version '0.0.6';-- Verify setup with a no-op testbegin;select plan(1);select ok(true, 'Pre-test hook completed successfully');select * from finish();rollback;
```

### Benefits [\#](https://supabase.com/docs/guides/local-development/testing/pgtap-extended\#benefits)

This approach provides several advantages:

- Reduces code duplication across test files
- Ensures consistent test environment setup
- Makes it easier to maintain and update shared dependencies
- Provides immediate feedback if the setup process fails

Your subsequent test files ( `001-auth-tests.sql`, `002-rls-tests.sql`) can focus solely on their specific test cases, knowing that the environment is properly configured.

## Example: Advanced RLS testing [\#](https://supabase.com/docs/guides/local-development/testing/pgtap-extended\#example-advanced-rls-testing)

Here's a complete example using test helpers to verify RLS policies putting it all together:

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
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
begin;-- Assuming 000-setup-tests-hooks.sql file is present to use tests helpersselect plan(4);-- Set up test data-- Create test supabase usersselect tests.create_supabase_user('user1@test.com');select tests.create_supabase_user('user2@test.com');-- Create test datainsert into public.todos (task, user_id) values  ('User 1 Task 1', tests.get_supabase_uid('user1@test.com')),  ('User 1 Task 2', tests.get_supabase_uid('user1@test.com')),  ('User 2 Task 1', tests.get_supabase_uid('user2@test.com'));-- Test as User 1select tests.authenticate_as('user1@test.com');-- Test 1: User 1 should only see their own todosselect results_eq(  'select count(*) from todos',  ARRAY[2::bigint],  'User 1 should only see their 2 todos');-- Test 2: User 1 can create their own todoselect lives_ok(  $$insert into todos (task, user_id) values ('New Task', tests.get_supabase_uid('user1@test.com'))$$,  'User 1 can create their own todo');-- Test as User 2select tests.authenticate_as('user2@test.com');-- Test 3: User 2 should only see their own todosselect results_eq(  'select count(*) from todos',  ARRAY[1::bigint],  'User 2 should only see their 1 todo');-- Test 4: User 2 cannot modify User 1's todoSELECT results_ne(    $$ update todos set task = 'Hacked!' where user_id = tests.get_supabase_uid('user1@test.com') returning 1 $$,    $$ values(1) $$,    'User 2 cannot modify User 1 todos');select * from finish();rollback;
```

## Not another todo app: Testing complex organizations [\#](https://supabase.com/docs/guides/local-development/testing/pgtap-extended\#not-another-todo-app-testing-complex-organizations)

Todo apps are great for learning, but this section explores testing a more realistic scenario: a multi-tenant content publishing platform. This example demonstrates testing complex permissions, plan restrictions, and content management.

### System overview [\#](https://supabase.com/docs/guides/local-development/testing/pgtap-extended\#system-overview)

This demo app implements:

- Organizations with tiered plans (free/pro/enterprise)
- Role-based access (owner/admin/editor/viewer)
- Content management (posts/comments)
- Premium content restrictions
- Plan-based limitations

### What makes this complex? [\#](https://supabase.com/docs/guides/local-development/testing/pgtap-extended\#what-makes-this-complex)

1. **Layered Permissions**
   - Role hierarchies affect access rights
   - Plan types influence user capabilities
   - Content state (draft/published) affects permissions
2. **Business Rules**
   - Free plan post limits
   - Premium content visibility
   - Cross-organization security

### Testing focus areas [\#](https://supabase.com/docs/guides/local-development/testing/pgtap-extended\#testing-focus-areas)

When writing tests, verify:

- Organization member access control
- Content visibility across roles
- Plan limitation enforcement
- Cross-organization data isolation

#### 1\. App schema definitions [\#](https://supabase.com/docs/guides/local-development/testing/pgtap-extended\#1-app-schema-definitions)

The app schema tables are defined like this:

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
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
create table public.profiles (  id uuid references auth.users(id) primary key,  username text unique not null,  full_name text,  bio text,  created_at timestamptz default now(),  updated_at timestamptz default now());create table public.organizations (  id bigint primary key generated always as identity,  name text not null,  slug text unique not null,  plan_type text not null check (plan_type in ('free', 'pro', 'enterprise')),  max_posts int not null default 5,  created_at timestamptz default now());create table public.org_members (  org_id bigint references public.organizations(id) on delete cascade,  user_id uuid references auth.users(id) on delete cascade,  role text not null check (role in ('owner', 'admin', 'editor', 'viewer')),  created_at timestamptz default now(),  primary key (org_id, user_id));create table public.posts (  id bigint primary key generated always as identity,  title text not null,  content text not null,  author_id uuid references public.profiles(id) not null,  org_id bigint references public.organizations(id),  status text not null check (status in ('draft', 'published', 'archived')),  is_premium boolean default false,  scheduled_for timestamptz,  category text,  view_count int default 0,  published_at timestamptz,  created_at timestamptz default now(),  updated_at timestamptz default now());create table public.comments (  id bigint primary key generated always as identity,  post_id bigint references public.posts(id) on delete cascade,  author_id uuid references public.profiles(id),  content text not null,  is_deleted boolean default false,  created_at timestamptz default now(),  updated_at timestamptz default now());
```

#### 2\. RLS policies declaration [\#](https://supabase.com/docs/guides/local-development/testing/pgtap-extended\#2-rls-policies-declaration)

Now to setup the RLS policies for each tables:

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
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
-- Create a private schema to store all security definer functions utils-- As such functions should never be in a API exposed schemacreate schema if not exists private;-- Helper function for role checkscreate or replace function private.get_user_org_role(org_id bigint, user_id uuid)returns textset search_path = ''as $$  select role from public.org_members  where org_id = $1 and user_id = $2;-- Note the use of security definer to avoid RLS checking recursion issue-- see: https://supabase.com/docs/guides/database/postgres/row-level-security#use-security-definer-functions$$ language sql security definer;-- Helper utils to check if an org is below the max post limitcreate or replace function private.can_add_post(org_id bigint)returns booleanset search_path = ''as $$  select (select count(*)          from public.posts p          where p.org_id = $1) < o.max_posts  from public.organizations o  where o.id = $1$$ language sql security definer;-- Enable RLS for all tablesalter table public.profiles enable row level security;alter table public.organizations enable row level security;alter table public.org_members enable row level security;alter table public.posts enable row level security;alter table public.comments enable row level security;-- Profiles policiescreate policy "Public profiles are viewable by everyone"  on public.profiles for select using (true);create policy "Users can insert their own profile"  on public.profiles for insert with check ((select auth.uid()) = id);create policy "Users can update their own profile"  on public.profiles for update using ((select auth.uid()) = id)  with check ((select auth.uid()) = id);-- Organizations policiescreate policy "Public org info visible to all"  on public.organizations for select using (true);create policy "Org management restricted to owners"  on public.organizations for all using (    private.get_user_org_role(id, (select auth.uid())) = 'owner'  );-- Org Members policiescreate policy "Members visible to org members"  on public.org_members for select using (    private.get_user_org_role(org_id, (select auth.uid())) is not null  );create policy "Member management restricted to admins and owners"  on public.org_members for all using (    private.get_user_org_role(org_id, (select auth.uid())) in ('owner', 'admin')  );-- Posts policiescreate policy "Complex post visibility"  on public.posts for select using (    -- Published non-premium posts are visible to all    (status = 'published' and not is_premium)    or    -- Premium posts visible to org members only    (status = 'published' and is_premium and    private.get_user_org_role(org_id, (select auth.uid())) is not null)    or    -- All posts visible to editors and above    private.get_user_org_role(org_id, (select auth.uid())) in ('owner', 'admin', 'editor')  );create policy "Post creation rules"  on public.posts for insert with check (    -- Must be org member with appropriate role    private.get_user_org_role(org_id, (select auth.uid())) in ('owner', 'admin', 'editor')    and    -- Check org post limits for free plans    (      (select o.plan_type != 'free'      from organizations o      where o.id = org_id)      or      (select private.can_add_post(org_id))    )  );create policy "Post update rules"  on public.posts for update using (    exists (      select 1      where        -- Editors can update non-published posts        (private.get_user_org_role(org_id, (select auth.uid())) = 'editor' and status != 'published')        or        -- Admins and owners can update any post        private.get_user_org_role(org_id, (select auth.uid())) in ('owner', 'admin')    )  );-- Comments policiescreate policy "Comments on published posts are viewable by everyone"  on public.comments for select using (    exists (      select 1 from public.posts      where id = post_id      and status = 'published'    )    and not is_deleted  );create policy "Authenticated users can create comments"  on public.comments for insert with check ((select auth.uid()) = author_id);create policy "Users can update their own comments"  on public.comments for update using (author_id = (select auth.uid()));
```

#### 3\. Test cases: [\#](https://supabase.com/docs/guides/local-development/testing/pgtap-extended\#3-test-cases)

Now everything is setup, let's write RLS test cases, note that each section could be in its own test:

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
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
-- Assuming we already have: 000-setup-tests-hooks.sql file we can use tests helpersbegin;-- Declare total number of testsselect plan(10);-- Create test usersselect tests.create_supabase_user('org_owner', 'owner@test.com');select tests.create_supabase_user('org_admin', 'admin@test.com');select tests.create_supabase_user('org_editor', 'editor@test.com');select tests.create_supabase_user('premium_user', 'premium@test.com');select tests.create_supabase_user('free_user', 'free@test.com');select tests.create_supabase_user('scheduler', 'scheduler@test.com');select tests.create_supabase_user('free_author', 'free_author@test.com');-- Create profiles for test usersinsert into profiles (id, username, full_name)values  (tests.get_supabase_uid('org_owner'), 'org_owner', 'Organization Owner'),  (tests.get_supabase_uid('org_admin'), 'org_admin', 'Organization Admin'),  (tests.get_supabase_uid('org_editor'), 'org_editor', 'Organization Editor'),  (tests.get_supabase_uid('premium_user'), 'premium_user', 'Premium User'),  (tests.get_supabase_uid('free_user'), 'free_user', 'Free User'),  (tests.get_supabase_uid('scheduler'), 'scheduler', 'Scheduler User'),  (tests.get_supabase_uid('free_author'), 'free_author', 'Free Author');-- First authenticate as service role to bypass RLS for initial setupselect tests.authenticate_as_service_role();-- Create test organizations and setup datawith new_org as (  insert into organizations (name, slug, plan_type, max_posts)  values    ('Test Org', 'test-org', 'pro', 100),    ('Premium Org', 'premium-org', 'enterprise', 1000),    ('Schedule Org', 'schedule-org', 'pro', 100),    ('Free Org', 'free-org', 'free', 2)  returning id, slug),-- Setup members and postsmember_setup as (  insert into org_members (org_id, user_id, role)  select    org.id,    user_id,    role  from new_org org cross join (    values      (tests.get_supabase_uid('org_owner'), 'owner'),      (tests.get_supabase_uid('org_admin'), 'admin'),      (tests.get_supabase_uid('org_editor'), 'editor'),      (tests.get_supabase_uid('premium_user'), 'viewer'),      (tests.get_supabase_uid('scheduler'), 'editor'),      (tests.get_supabase_uid('free_author'), 'editor')  ) as members(user_id, role)  where org.slug = 'test-org'     or (org.slug = 'premium-org' and role = 'viewer')     or (org.slug = 'schedule-org' and role = 'editor')     or (org.slug = 'free-org' and role = 'editor'))-- Setup initial postsinsert into posts (title, content, org_id, author_id, status, is_premium, scheduled_for)select  title,  content,  org.id,  author_id,  status,  is_premium,  scheduled_forfrom new_org org cross join (  values    ('Premium Post', 'Premium content', tests.get_supabase_uid('premium_user'), 'published', true, null),    ('Free Post', 'Free content', tests.get_supabase_uid('premium_user'), 'published', false, null),    ('Future Post', 'Future content', tests.get_supabase_uid('scheduler'), 'published', false, '2024-01-02 12:00:00+00'::timestamptz)) as posts(title, content, author_id, status, is_premium, scheduled_for)where org.slug in ('premium-org', 'schedule-org');-- Test owner privilegesselect tests.authenticate_as('org_owner');select lives_ok(  $$    update organizations    set name = 'Updated Org'    where id = (select id from organizations limit 1)  $$,  'Owner can update organization');-- Test admin privilegesselect tests.authenticate_as('org_admin');select results_eq(    $$select count(*) from org_members$$,    ARRAY[6::bigint],    'Admin can view all members');-- Test editor restrictionsselect tests.authenticate_as('org_editor');select throws_ok(  $$    insert into org_members (org_id, user_id, role)    values (      (select id from organizations limit 1),      (select tests.get_supabase_uid('org_editor')),      'viewer'    )  $$,  '42501',  'new row violates row-level security policy for table "org_members"',  'Editor cannot manage members');-- Premium Content Access Testsselect tests.authenticate_as('premium_user');select results_eq(    $$select count(*) from posts where org_id = (select id from organizations where slug = 'premium-org')$$,    ARRAY[3::bigint],    'Premium user can see all posts');select tests.clear_authentication();select results_eq(    $$select count(*) from posts where org_id = (select id from organizations where slug = 'premium-org')$$,    ARRAY[2::bigint],    'Anonymous users can only see free posts');-- Time-Based Publishing Testsselect tests.authenticate_as('scheduler');select tests.freeze_time('2024-01-01 12:00:00+00'::timestamptz);select results_eq(    $$select count(*) from posts where scheduled_for > now() and org_id = (select id from organizations where slug = 'schedule-org')$$,    ARRAY[1::bigint],    'Can see scheduled posts');select tests.freeze_time('2024-01-02 13:00:00+00'::timestamptz);select results_eq(    $$select count(*) from posts where scheduled_for < now() and org_id = (select id from organizations where slug = 'schedule-org')$$,    ARRAY[1::bigint],    'Can see posts after schedule time');select tests.unfreeze_time();-- Plan Limit Testsselect tests.authenticate_as('free_author');select lives_ok(  $$    insert into posts (title, content, org_id, author_id, status)    select 'Post 1', 'Content 1', id, auth.uid(), 'draft'    from organizations where slug = 'free-org' limit 1  $$,  'First post creates successfully');select lives_ok(  $$    insert into posts (title, content, org_id, author_id, status)    select 'Post 2', 'Content 2', id, auth.uid(), 'draft'    from organizations where slug = 'free-org' limit 1  $$,  'Second post creates successfully');select throws_ok(  $$    insert into posts (title, content, org_id, author_id, status)    select 'Post 3', 'Content 3', id, auth.uid(), 'draft'    from organizations where slug = 'free-org' limit 1  $$,  '42501',  'new row violates row-level security policy for table "posts"',  'Cannot exceed free plan post limit');select * from finish();rollback;
```

## Additional resources [\#](https://supabase.com/docs/guides/local-development/testing/pgtap-extended\#additional-resources)

- [Test Helpers Documentation](https://database.dev/basejump/supabase_test_helpers)
- [Test Helpers Reference](https://github.com/usebasejump/supabase-test-helpers)
- [Row Level Security Writing Guide](https://usebasejump.com/blog/testing-on-supabase-with-pgtap)
- [Database.dev Package Registry](https://database.dev/)
- [Row Level Security Performance and Best Practices](https://github.com/orgs/supabase/discussions/14576)

### Is this helpful?

NoYes

### On this page

[Using database.dev](https://supabase.com/docs/guides/local-development/testing/pgtap-extended#using-databasedev) [Setting up dbdev](https://supabase.com/docs/guides/local-development/testing/pgtap-extended#setting-up-dbdev) [Installing test helpers](https://supabase.com/docs/guides/local-development/testing/pgtap-extended#installing-test-helpers) [Test helper benefits](https://supabase.com/docs/guides/local-development/testing/pgtap-extended#test-helper-benefits) [Schema-wide Row Level Security testing](https://supabase.com/docs/guides/local-development/testing/pgtap-extended#schema-wide-row-level-security-testing) [Test file organization](https://supabase.com/docs/guides/local-development/testing/pgtap-extended#test-file-organization) [Creating a pre-test hook](https://supabase.com/docs/guides/local-development/testing/pgtap-extended#creating-a-pre-test-hook) [Benefits](https://supabase.com/docs/guides/local-development/testing/pgtap-extended#benefits) [Example: Advanced RLS testing](https://supabase.com/docs/guides/local-development/testing/pgtap-extended#example-advanced-rls-testing) [Not another todo app: Testing complex organizations](https://supabase.com/docs/guides/local-development/testing/pgtap-extended#not-another-todo-app-testing-complex-organizations) [System overview](https://supabase.com/docs/guides/local-development/testing/pgtap-extended#system-overview) [What makes this complex?](https://supabase.com/docs/guides/local-development/testing/pgtap-extended#what-makes-this-complex) [Testing focus areas](https://supabase.com/docs/guides/local-development/testing/pgtap-extended#testing-focus-areas) [Additional resources](https://supabase.com/docs/guides/local-development/testing/pgtap-extended#additional-resources)

1. We use first-party cookies to improve our services. [Learn more](https://supabase.com/privacy#8-cookies-and-similar-technologies-used-on-our-european-services)



   [Learn more](https://supabase.com/privacy#8-cookies-and-similar-technologies-used-on-our-european-services)•Privacy settings





   AcceptOpt outPrivacy settings