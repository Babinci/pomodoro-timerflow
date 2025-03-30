31 APR - 04 MAR / 7AM PT

Launch Week 14

03d

:

18h

:

12m

:

13s

[Claim ticket](https://supabase.com/launch-week)Dismiss

![](https://supabase.com/docs/_next/image?url=%2Fdocs%2Fimg%2Flaunchweek%2F14%2Fpromo-banner-bg.png&w=3840&q=100&dpl=dpl_9WgBm3X43HXGqPuPh4vSvQgRaZyZ)

Edge Functions

# Limits

## Limits applied Edge Functions in Supabase's hosted platform.

* * *

## Runtime limits [\#](https://supabase.com/docs/guides/functions/limits\#runtime-limits)

- Maximum Memory: 256MB
- Maximum Duration (Wall clock limit):
This is the duration an Edge Function worker will stay active. During this period, a worker can serve multiple requests or process background tasks.
  - Free plan: 150s
  - Paid plans: 400s
- Maximum CPU Time: 2s (Amount of actual time spent on the CPU per request - does not include async I/O.)
- Request idle timeout: 150s (If an Edge Function doesn't send a response before the timeout, 504 Gateway Timeout will be returned)
- Maximum Function Size: 20MB (After bundling using CLI)
- Maximum log message length: 10,000 characters
- Log event threshold: 100 events per 10 seconds

## Other limits & restrictions [\#](https://supabase.com/docs/guides/functions/limits\#other-limits--restrictions)

- Outgoing connections to ports `25` and `587` are not allowed.
- Serving of HTML content is only supported with [custom domains](https://supabase.com/docs/reference/cli/supabase-domains) (Otherwise `GET` requests that return `text/html` will be rewritten to `text/plain`).
- Web Worker API (or Node `vm` API) are not available.
- Node Libraries that require multithreading are not supported. Examples: [`libvips`](https://github.com/libvips/libvips), [sharp](https://github.com/lovell/sharp).

### Is this helpful?

NoYes

### On this page

[Runtime limits](https://supabase.com/docs/guides/functions/limits#runtime-limits) [Other limits & restrictions](https://supabase.com/docs/guides/functions/limits#other-limits--restrictions)