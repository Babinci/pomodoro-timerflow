31 APR - 04 MAR / 7AM PT

Launch Week 14

03d

:

18h

:

17m

:

27s

[Claim ticket](https://supabase.com/launch-week)Dismiss

![](https://supabase.com/docs/_next/image?url=%2Fdocs%2Fimg%2Flaunchweek%2F14%2Fpromo-banner-bg.png&w=3840&q=100&dpl=dpl_9WgBm3X43HXGqPuPh4vSvQgRaZyZ)

# Check usage for monthly active users (MAU)

Last edited: 1/17/2025

* * *

You can see the usage in your [projects usage page](https://app.supabase.com/project/_/settings/billing/usage).

For MAU, we rely on the [Auth Server](https://github.com/supabase/auth) logs. MAU count is relative to your billing cycle and resets whenever your billing cycle resets. You can check your Auth logs in your [projects logs & analytics section](https://supabase.com/dashboard/project/_/logs/auth-logs).

We do a distinct count of all user ids in the billing cycle. An Auth event can be a login, token refresh, logout, ... If an authenticated user does any of this, we count it towards the MAU. A user is only counted once towards MAU in a billing cycle.

The log retention for you as a user (accessible time) depends on your plan. Free plan users can access the logs of the last day, Pro plan users 7 days, Team plan users 28 days, Enterprise users 90 days. Unless you're on an Enterprise plan, you won't be able to execute the query to determine MAU yourself, as you don't have access to the logs in the past 30ish days (depending on your billing cycle).