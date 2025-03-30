Edge Functions

# Handling Stripe Webhooks

* * *

Handling signed Stripe Webhooks with Edge Functions - YouTube

Supabase

47.5K subscribers

[Handling signed Stripe Webhooks with Edge Functions](https://www.youtube.com/watch?v=6OMVWiiycLs)

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

[Watch on YouTube](https://www.youtube.com/watch?v=6OMVWiiycLs "Watch on YouTube")

Handling signed Stripe Webhooks with Edge Functions. [View on GitHub](https://github.com/supabase/supabase/blob/master/examples/edge-functions/supabase/functions/stripe-webhooks/index.ts).

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
// Follow this setup guide to integrate the Deno language server with your editor:// https://deno.land/manual/getting_started/setup_your_environment// This enables autocomplete, go to definition, etc.// Import via bare specifier thanks to the import_map.json file.import Stripe from 'https://esm.sh/stripe@14?target=denonext'const stripe = new Stripe(Deno.env.get('STRIPE_API_KEY') as string, {  // This is needed to use the Fetch API rather than relying on the Node http  // package.  apiVersion: '2024-11-20'})// This is needed in order to use the Web Crypto API in Deno.const cryptoProvider = Stripe.createSubtleCryptoProvider()console.log('Hello from Stripe Webhook!')Deno.serve(async (request) => {  const signature = request.headers.get('Stripe-Signature')  // First step is to verify the event. The .text() method must be used as the  // verification relies on the raw request body rather than the parsed JSON.  const body = await request.text()  let receivedEvent  try {    receivedEvent = await stripe.webhooks.constructEventAsync(      body,      signature!,      Deno.env.get('STRIPE_WEBHOOK_SIGNING_SECRET')!,      undefined,      cryptoProvider    )  } catch (err) {    return new Response(err.message, { status: 400 })  }  console.log(`🔔 Event received: ${receivedEvent.id}`)  return new Response(JSON.stringify({ ok: true }), { status: 200 })});
```

[View source](https://github.com/supabase/supabase/blob/b28907814838b3866ab4806e361f0f5a01c9cf6b/examples/edge-functions/supabase/functions/stripe-webhooks/index.ts)

### Is this helpful?

NoYes

1. We use first-party cookies to improve our services. [Learn more](https://supabase.com/privacy#8-cookies-and-similar-technologies-used-on-our-european-services)



   [Learn more](https://supabase.com/privacy#8-cookies-and-similar-technologies-used-on-our-european-services)•Privacy settings





   AcceptOpt outPrivacy settings