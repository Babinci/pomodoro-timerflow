# "insufficient privilege" when accessing pg\_stat\_statements

Last edited: 1/16/2025

* * *

If you see the error "insufficient privilege" when accessing [pg\_stat\_statements](https://supabase.com/docs/guides/platform/performance#postgres-cumulative-statistics-system) or when accessing [Query Performance Report](https://supabase.com/dashboard/project/_/reports/query-performance), it means that the Postgres role does not have required permissions.

In this case, you can run the below command to allow the Postgres role to read all statistics from the system:

```flex

1
grant pg_read_all_stats to postgres;
```

1. We use first-party cookies to improve our services. [Learn more](https://supabase.com/privacy#8-cookies-and-similar-technologies-used-on-our-european-services)



   [Learn more](https://supabase.com/privacy#8-cookies-and-similar-technologies-used-on-our-european-services)•Privacy settings





   AcceptOpt outPrivacy settings