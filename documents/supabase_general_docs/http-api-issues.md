# Diagnose HTTP API issues

Last edited: 2/3/2025

* * *

Symptoms of HTTP API issues include:

- HTTP timeouts
- 5xx response codes
- High response times

### Under-provisioned resources [\#](https://supabase.com/docs/guides/troubleshooting/http-api-issues\#under-provisioned-resources)

The most common class of issues that causes HTTP timeouts and 5xx response codes is the under-provisioning of resources for your project. This can cause your project to be unable to service the traffic it is receiving.

Each Supabase project is provisioned with [segregated compute resources](https://supabase.com/docs/guides/platform/compute-add-ons). This allows the project to serve unlimited requests, as long as they can be handled using the resources that have been provisioned. Complex queries, or queries that process larger amounts of data, will require higher amounts of resources. As such, the amount of resources that can handle a high volume of simple queries (or queries involving small amounts of data), will likely be unable to handle a similar volume of complex queries.

You can view the resource utilization of your Supabase Project using the [reports in the Dashboard](https://supabase.com/dashboard/project/_/reports/database).

Some common solutions for this issue are:

- [Upgrading](https://supabase.com/dashboard/project/_/settings/compute-and-disk) to a [larger compute add-on](https://supabase.com/docs/guides/platform/compute-add-ons) in order to serve higher volumes of traffic.
- [Optimizing the queries](https://supabase.com/docs/guides/platform/performance#examining-query-performance) being executed.
- [Using fewer Postgres connections](https://supabase.com/docs/guides/platform/performance#configuring-clients-to-use-fewer-connections) can reduce the amount of resources needed on the project.
- [Restarting](https://supabase.com/dashboard/project/_/settings/general) the project. This only temporarily solves the issue by terminating any ongoing workloads that might be tying up your compute resources.
  - All databases of the project, including [Read replicas](https://supabase.com/docs/guides/platform/read-replicas), will be restarted.
  - If you only want to restart a specific Read Replica, you can do so from the [Infrastructure Settings page](https://supabase.com/dashboard/project/_/settings/infrastructure).

If your [Disk IO budget](https://supabase.com/docs/guides/platform/compute-add-ons#disk-io) has been drained, you will need to either wait for it to be replenished the next day, or upgrade to a larger compute add-on to increase the budget available to your project.

## Unable to connect to your Supabase project [\#](https://supabase.com/docs/guides/troubleshooting/http-api-issues\#unable-to-connect-to-your-supabase-project)

Symptom: You're unable to connect to your Postgres database directly, but can open the Project in the [Supabase Dashboard](https://supabase.com/dashboard/project/_/).

### Too many open connections [\#](https://supabase.com/docs/guides/troubleshooting/http-api-issues\#too-many-open-connections)

Errors about too many open connections can be _temporarily_ resolved by [restarting the database](https://supabase.com/dashboard/project/_/settings/general). However, this won't solve the underlying issue for a permanent solution.

- If you're receiving a `No more connections allowed (max_client_conn)` error:
  - Configure your applications and services to [use fewer connections](https://supabase.com/docs/guides/platform/performance#configuring-clients-to-use-fewer-connections).
  - [Upgrade](https://supabase.com/dashboard/project/_/settings/compute-and-disk) to a [larger compute add-on](https://supabase.com/docs/guides/platform/compute-add-ons) to increase the number of available connections.
- If you're receiving a `sorry, too many clients already` or `remaining connection slots are reserved for non-replication superuser connections` error message in addition to the above suggestions, switch to using the [connection pooler](https://supabase.com/docs/guides/database/connecting-to-postgres#connection-pool) instead.

### Connection refused [\#](https://supabase.com/docs/guides/troubleshooting/http-api-issues\#connection-refused)

If you receive a `connection refused` error after a few initial failed connection attempts, your client has likely been temporarily blocked in order to protect the database from brute-force attacks. You can wait 30 minutes before trying again with the correct password, or you can [contact support](https://supabase.com/dashboard/support/new) with your client's IP address to manually unblock you.

If you're also unable to open the project using the [Supabase Dashboard](https://supabase.com/dashboard/project/_/), review the solutions for [under-provisioned projects](https://supabase.com/docs/guides/troubleshooting/http-api-issues#under-provisioned-resources).

1. We use first-party cookies to improve our services. [Learn more](https://supabase.com/privacy#8-cookies-and-similar-technologies-used-on-our-european-services)



   [Learn more](https://supabase.com/privacy#8-cookies-and-similar-technologies-used-on-our-european-services)•Privacy settings





   AcceptOpt outPrivacy settings