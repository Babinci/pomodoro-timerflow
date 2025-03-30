31 APR - 04 MAR / 7AM PT

Launch Week 14

03d

:

17h

:

51m

:

22s

[Claim ticket](https://supabase.com/launch-week)Dismiss

![](https://supabase.com/docs/_next/image?url=%2Fdocs%2Fimg%2Flaunchweek%2F14%2Fpromo-banner-bg.png&w=3840&q=100&dpl=dpl_2DQMEZHm5P9QNZGKAqcszuVSdHSJ)

Local Development

# Local development with schema migrations

## Develop locally with the Supabase CLI and schema migrations.

* * *

Supabase is a flexible platform that lets you decide how you want to build your projects. You can use the Dashboard directly to get up and running quickly, or use a proper local setup. We suggest you work locally and deploy your changes to a linked project on the [Supabase Platform](https://app.supabase.io/).

Develop locally using the CLI to run a local Supabase stack. You can use the integrated Studio Dashboard to make changes, then capture your changes in schema migration files, which can be saved in version control.

Alternatively, if you're comfortable with migration files and SQL, you can write your own migrations and push them to the local database for testing before sharing your changes.

## Database migrations [\#](https://supabase.com/docs/guides/local-development/overview\#database-migrations)

Database changes are managed through "migrations." Database migrations are a common way of tracking changes to your database over time.

How to Manage Database Migration Using Supabase CLI - SupabaseTips - YouTube

Supabase

47.5K subscribers

[How to Manage Database Migration Using Supabase CLI - SupabaseTips](https://www.youtube.com/watch?v=Kx5nHBmIxyQ)

Supabase

Search

Info

Shopping

Tap to unmute

If playback doesn't begin shortly, try restarting your device.

You're signed out

Videos you watch may be added to the TV's watch history and influence TV recommendations. To avoid this, cancel and sign in to YouTube on your computer.

CancelConfirm

Share

Include playlist

An error occurred while retrieving sharing information. Please try again later.

Watch later

Share

Copy link

Watch on

0:00

/ •Live

•

[Watch on YouTube](https://www.youtube.com/watch?v=Kx5nHBmIxyQ "Watch on YouTube")

For this guide, we'll create a table called `employees` and see how we can make changes to it.

1

### Create your first migration file

To get started, generate a [new migration](https://supabase.com/docs/reference/cli/supabase-migration-new) to store the SQL needed to create our `employees` table

```flex

1
supabase migration new create_employees_table
```

2

### Add the SQL to your migration file

This creates a new migration: supabase/migrations/<timestamp>
\_create\_employees\_table.sql.

To that file, add the SQL to create this `employees` table

```flex

1
2
3
4
5
6
7
create tableemployees (id bigint primary key generated always as identity,name text,email text,created_at timestamptz default now());
```

3

### Apply your migration

Now that you have a migration file, you can run this migration and create the `employees` table.

Use the `reset` command here to reset the database to the current migrations

```flex

1
supabase db reset
```

4

### Modify your employees table

Now you can visit your new `employees` table in the Dashboard.

Next, modify your `employees` table by adding a column for department. Create a new migration file for that.

```flex

1
supabase migration new add_department_to_employees_table
```

5

### Add a new column to your table

This creates a new migration file: supabase/migrations/<timestamp>
\_add\_department\_to\_employees\_table.sql.

To that file, add the SQL to create a new department column

```flex

1
2
alter tableif exists public.employees add department text default 'Hooli';
```

### Add sample data [\#](https://supabase.com/docs/guides/local-development/overview\#add-sample-data)

Now that you are managing your database with migrations scripts, it would be great have some seed data to use every time you reset the database.

For this, you can create a seed script in `supabase/seed.sql`.

1

### Populate your table

Insert data into your `employees` table with your `supabase/seed.sql` file.

```flex

1
2
3
4
5
6
7
-- in supabase/seed.sqlinsert intopublic.employees (name)values('Erlich Bachman'),('Richard Hendricks'),('Monica Hall');
```

2

### Reset your database

Reset your database (apply current migrations), and populate with seed data

```flex

1
supabase db reset
```

You should now see the `employees` table, along with your seed data in the Dashboard! All of your database changes are captured in code, and you can reset to a known state at any time, complete with seed data.

### Diffing changes [\#](https://supabase.com/docs/guides/local-development/overview\#diffing-changes)

This workflow is great if you know SQL and are comfortable creating tables and columns. If not, you can still use the Dashboard to create tables and columns, and then use the CLI to diff your changes and create migrations.

Create a new table called `cities`, with columns `id`, `name` and `population`. To see the corresponding SQL for this, you can use the `supabase db diff --schema public` command. This will show you the SQL that will be run to create the table and columns. The output of `supabase db diff` will look something like this:

```flex

1
2
3
4
5
6
7
8
Diffing schemas: publicFinished supabase db diff on branch main.create table "public"."cities" (    "id" bigint primary key generated always as identity,    "name" text,    "population" bigint);
```

Alternately, you can view your table definitions directly from the Table Editor:

![SQL Definition](https://supabase.com/docs/img/guides/cli/sql-definitions.png)

You can then copy this SQL into a new migration file, and run `supabase db reset` to apply the changes.

The last step is deploying these changes to a live Supabase project.

## Deploy your project [\#](https://supabase.com/docs/guides/local-development/overview\#deploy-your-project)

You've been developing your project locally, making changes to your tables via migrations. It's time to deploy your project to the Supabase Platform and start scaling up to millions of users! Head over to [Supabase](https://supabase.com/dashboard) and create a new project to deploy to.

### Log in to the Supabase CLI [\#](https://supabase.com/docs/guides/local-development/overview\#log-in-to-the-supabase-cli)

Terminalnpx

```flex

1
supabase login
```

### Link your project [\#](https://supabase.com/docs/guides/local-development/overview\#link-your-project)

Associate your project with your remote project using [`supabase link`](https://supabase.com/docs/reference/cli/usage#supabase-link).

```flex

1
2
3
4
5
6
supabase link --project-ref <project-id># You can get <project-id> from your project's dashboard URL: https://supabase.com/dashboard/project/<project-id>supabase db pull# Capture any changes that you have made to your remote database before you went through the steps above# If you have not made any changes to the remote database, skip this step
```

`supabase/migrations` is now populated with a migration in `<timestamp>_remote_schema.sql`.
This migration captures any changes required for your local database to match the schema of your remote Supabase project.

Review the generated migration file and once happy, apply the changes to your local instance:

```flex

1
2
3
4
5
# To apply the new migration to your local database:supabase migration up# To reset your local database completely:supabase db reset
```

There are a few commands required to link your project. We are in the process of consolidating these commands into a single command. Bear with us!

### Deploy database changes [\#](https://supabase.com/docs/guides/local-development/overview\#deploy-database-changes)

Deploy any local database migrations using [`db push`](https://supabase.com/docs/reference/cli/usage#supabase-db-push):

```flex

1
supabase db push
```

Visiting your live project on [Supabase](https://supabase.com/dashboard), you'll see a new `employees` table, complete with the `department` column you added in the second migration above.

### Deploy Edge Functions [\#](https://supabase.com/docs/guides/local-development/overview\#deploy-edge-functions)

If your project uses Edge Functions, you can deploy these using [`functions deploy`](https://supabase.com/docs/reference/cli/usage#supabase-functions-deploy):

```flex

1
supabase functions deploy <function_name>
```

### Use Auth locally [\#](https://supabase.com/docs/guides/local-development/overview\#use-auth-locally)

To use Auth locally, update your project's `supabase/config.toml` file that gets created after running `supabase init`. Add any providers you want, and set enabled to `true`.

```flex

1
2
3
4
5
[auth.external.github]enabled = trueclient_id = "env(SUPABASE_AUTH_GITHUB_CLIENT_ID)"secret = "env(SUPABASE_AUTH_GITHUB_SECRET)"redirect_uri = "http://localhost:54321/auth/v1/callback"
```

As a best practice, any secret values should be loaded from environment variables. You can add them to `.env` file in your project's root directory for the CLI to automatically substitute them.

```flex

1
2
SUPABASE_AUTH_GITHUB_CLIENT_ID="redacted"SUPABASE_AUTH_GITHUB_SECRET="redacted"
```

For these changes to take effect, you need to run `supabase stop` and `supabase start` again.

If you have additional triggers or RLS policies defined on your `auth` schema, you can pull them as a migration file locally.

```flex

1
supabase db pull --schema auth
```

### Sync storage buckets [\#](https://supabase.com/docs/guides/local-development/overview\#sync-storage-buckets)

Your RLS policies on storage buckets can be pulled locally by specifying `storage` schema. For example,

```flex

1
supabase db pull --schema storage
```

The buckets and objects themselves are rows in the storage tables so they won't appear in your schema. You can instead define them via `supabase/config.toml` file. For example,

```flex

1
2
3
4
5
[storage.buckets.images]public = falsefile_size_limit = "50MiB"allowed_mime_types = ["image/png", "image/jpeg"]objects_path = "./images"
```

This will upload files from `supabase/images` directory to a bucket named `images` in your project with one command.

```flex

1
supabase seed buckets
```

### Sync any schema with `--schema` [\#](https://supabase.com/docs/guides/local-development/overview\#sync-any-schema-with---schema)

You can synchronize your database with a specific schema using the `--schema` option as follows:

```flex

1
supabase db pull --schema <schema_name>
```

Using `--schema`

If the local `supabase/migrations` directory is empty, the `db pull` command will ignore the `--schema` parameter.

To fix this, you can pull twice:

```flex

1
2
supabase db pullsupabase db pull --schema <schema_name>
```

## Limitations and considerations [\#](https://supabase.com/docs/guides/local-development/overview\#limitations-and-considerations)

The local development environment is not as feature-complete as the Supabase Platform. Here are some of the differences:

- You cannot update your project settings in the Dashboard. This must be done using the local config file.
- The CLI version determines the local version of Studio used, so make sure you keep your local [Supabase CLI up to date](https://github.com/supabase/cli#getting-started). We're constantly adding new features and bug fixes.

Watch video guide

![Video guide preview](https://supabase.com/docs/_next/image?url=https%3A%2F%2Fimg.youtube.com%2Fvi%2FvyHyYpvjaks%2F0.jpg&w=3840&q=75&dpl=dpl_2DQMEZHm5P9QNZGKAqcszuVSdHSJ)

### Is this helpful?

NoYes

### On this page

[Database migrations](https://supabase.com/docs/guides/local-development/overview#database-migrations) [Add sample data](https://supabase.com/docs/guides/local-development/overview#add-sample-data) [Diffing changes](https://supabase.com/docs/guides/local-development/overview#diffing-changes) [Deploy your project](https://supabase.com/docs/guides/local-development/overview#deploy-your-project) [Log in to the Supabase CLI](https://supabase.com/docs/guides/local-development/overview#log-in-to-the-supabase-cli) [Link your project](https://supabase.com/docs/guides/local-development/overview#link-your-project) [Deploy database changes](https://supabase.com/docs/guides/local-development/overview#deploy-database-changes) [Deploy Edge Functions](https://supabase.com/docs/guides/local-development/overview#deploy-edge-functions) [Use Auth locally](https://supabase.com/docs/guides/local-development/overview#use-auth-locally) [Sync storage buckets](https://supabase.com/docs/guides/local-development/overview#sync-storage-buckets) [Sync any schema with --schema](https://supabase.com/docs/guides/local-development/overview#sync-any-schema-with---schema) [Limitations and considerations](https://supabase.com/docs/guides/local-development/overview#limitations-and-considerations)