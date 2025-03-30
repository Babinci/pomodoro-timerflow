31 APR - 04 MAR / 7AM PT

Launch Week 14

03d

:

17h

:

50m

:

31s

[Claim ticket](https://supabase.com/launch-week)Dismiss

![](https://supabase.com/docs/_next/image?url=%2Fdocs%2Fimg%2Flaunchweek%2F14%2Fpromo-banner-bg.png&w=3840&q=100&dpl=dpl_2DQMEZHm5P9QNZGKAqcszuVSdHSJ)

Database

# Database configuration

## Updating the default configuration for your Postgres database.

* * *

Postgres provides a set of sensible defaults for you database size. In some cases, these defaults can be updated. We do not recommend changing these defaults unless you know what you're doing.

## Timeouts [\#](https://supabase.com/docs/guides/database/postgres/configuration\#timeouts)

See the [Timeouts](https://supabase.com/docs/guides/database/postgres/timeouts) section.

## Statement optimization [\#](https://supabase.com/docs/guides/database/postgres/configuration\#statement-optimization)

All Supabase projects come with the [`pg_stat_statements`](https://www.postgresql.org/docs/current/pgstatstatements.html) extension installed, which tracks planning and execution statistics for all statements executed against it. These statistics can be used in order to diagnose the performance of your project.

This data can further be used in conjunction with the [`explain`](https://www.postgresql.org/docs/current/using-explain.html) functionality of Postgres to optimize your usage.

## Managing timezones [\#](https://supabase.com/docs/guides/database/postgres/configuration\#managing-timezones)

Every Supabase database is set to UTC timezone by default. We strongly recommend keeping it this way, even if your users are in a different location.
This is because it makes it much easier to calculate differences between timezones if you adopt the mental model that everything in your database is in UTC time.

### Change timezone [\#](https://supabase.com/docs/guides/database/postgres/configuration\#change-timezone)

SQL

```flex

1
2
alter database postgresset timezone to 'America/New_York';
```

### Full list of timezones [\#](https://supabase.com/docs/guides/database/postgres/configuration\#full-list-of-timezones)

Get a full list of timezones supported by your database. This will return the following columns:

- `name`: Time zone name
- `abbrev`: Time zone abbreviation
- `utc_offset`: Offset from UTC (positive means east of Greenwich)
- `is_dst`: True if currently observing daylight savings

SQL

```flex

1
2
3
select name, abbrev, utc_offset, is_dstfrom pg_timezone_names()order by name;
```

### Search for a specific timezone [\#](https://supabase.com/docs/guides/database/postgres/configuration\#search-for-a-specific-timezone)

Use `ilike` (case insensitive search) to find specific timezones.

SQL

```flex

1
2
3
select *from pg_timezone_names()where name ilike '%york%';
```

### Is this helpful?

NoYes

### On this page

[Timeouts](https://supabase.com/docs/guides/database/postgres/configuration#timeouts) [Statement optimization](https://supabase.com/docs/guides/database/postgres/configuration#statement-optimization) [Managing timezones](https://supabase.com/docs/guides/database/postgres/configuration#managing-timezones) [Change timezone](https://supabase.com/docs/guides/database/postgres/configuration#change-timezone) [Full list of timezones](https://supabase.com/docs/guides/database/postgres/configuration#full-list-of-timezones) [Search for a specific timezone](https://supabase.com/docs/guides/database/postgres/configuration#search-for-a-specific-timezone)