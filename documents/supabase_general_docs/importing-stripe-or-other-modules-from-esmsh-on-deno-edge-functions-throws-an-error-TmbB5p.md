31 APR - 04 MAR / 7AM PT

Launch Week 14

03d

:

18h

:

17m

:

48s

[Claim ticket](https://supabase.com/launch-week)Dismiss

![](https://supabase.com/docs/_next/image?url=%2Fdocs%2Fimg%2Flaunchweek%2F14%2Fpromo-banner-bg.png&w=3840&q=100&dpl=dpl_9WgBm3X43HXGqPuPh4vSvQgRaZyZ)

# Importing Stripe or other modules from esm.sh on Deno Edge Functions throws an error

Last edited: 1/17/2025

* * *

Try adding `?target=deno` to the import path of the module. For Stripe, the updated import would be:

```flex

1
import Stripe from "https://esm.sh/stripe@11.2.0?target=deno";
```