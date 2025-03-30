31 APR - 04 MAR / 7AM PT

Launch Week 14

03d

:

18h

:

20m

:

57s

[Claim ticket](https://supabase.com/launch-week)Dismiss

![](https://supabase.com/docs/_next/image?url=%2Fdocs%2Fimg%2Flaunchweek%2F14%2Fpromo-banner-bg.png&w=3840&q=100&dpl=dpl_9WgBm3X43HXGqPuPh4vSvQgRaZyZ)

Edge Functions

# Building a Discord Bot

* * *

Discord Bots with Edge Functions - YouTube

Supabase

47.5K subscribers

[Discord Bots with Edge Functions](https://www.youtube.com/watch?v=J24Bvo_m7DM)

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

[Watch on YouTube](https://www.youtube.com/watch?v=J24Bvo_m7DM "Watch on YouTube")

## Create an application on Discord Developer portal [\#](https://supabase.com/docs/guides/functions/examples/discord-bot\#create-an-application-on-discord-developer-portal)

1. Go to [https://discord.com/developers/applications](https://discord.com/developers/applications) (login using your discord account if required).
2. Click on **New Application** button available at left side of your profile picture.
3. Name your application and click on **Create**.
4. Go to **Bot** section, click on **Add Bot**, and finally on **Yes, do it!** to confirm.

A new application is created which will hold our Slash Command. Don't close the tab as we need information from this application page throughout our development.

Before we can write some code, we need to curl a discord endpoint to register a Slash Command in our app.

Fill `DISCORD_BOT_TOKEN` with the token available in the **Bot** section and `CLIENT_ID` with the ID available on the **General Information** section of the page and run the command on your terminal.

```flex

1
2
3
4
5
6
7
BOT_TOKEN='replace_me_with_bot_token'CLIENT_ID='replace_me_with_client_id'curl -X POST \-H 'Content-Type: application/json' \-H "Authorization: Bot $BOT_TOKEN" \-d '{"name":"hello","description":"Greet a person","options":[{"name":"name","description":"The name of the person","type":3,"required":true}]}' \"https://discord.com/api/v8/applications/$CLIENT_ID/commands"
```

This will register a Slash Command named `hello` that accepts a parameter named `name` of type string.

## Code [\#](https://supabase.com/docs/guides/functions/examples/discord-bot\#code)

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
// Sift is a small routing library that abstracts away details like starting a// listener on a port, and provides a simple function (serve) that has an API// to invoke a function for a specific path.import { json, serve, validateRequest } from 'https://deno.land/x/sift@0.6.0/mod.ts'// TweetNaCl is a cryptography library that we use to verify requests// from Discord.import nacl from 'https://cdn.skypack.dev/tweetnacl@v1.0.3?dts'enum DiscordCommandType {  Ping = 1,  ApplicationCommand = 2,}// For all requests to "/" endpoint, we want to invoke home() handler.serve({  '/discord-bot': home,})// The main logic of the Discord Slash Command is defined in this function.async function home(request: Request) {  // validateRequest() ensures that a request is of POST method and  // has the following headers.  const { error } = await validateRequest(request, {    POST: {      headers: ['X-Signature-Ed25519', 'X-Signature-Timestamp'],    },  })  if (error) {    return json({ error: error.message }, { status: error.status })  }  // verifySignature() verifies if the request is coming from Discord.  // When the request's signature is not valid, we return a 401 and this is  // important as Discord sends invalid requests to test our verification.  const { valid, body } = await verifySignature(request)  if (!valid) {    return json(      { error: 'Invalid request' },      {        status: 401,      }    )  }  const { type = 0, data = { options: [] } } = JSON.parse(body)  // Discord performs Ping interactions to test our application.  // Type 1 in a request implies a Ping interaction.  if (type === DiscordCommandType.Ping) {    return json({      type: 1, // Type 1 in a response is a Pong interaction response type.    })  }  // Type 2 in a request is an ApplicationCommand interaction.  // It implies that a user has issued a command.  if (type === DiscordCommandType.ApplicationCommand) {    const { value } = data.options.find(      (option: { name: string; value: string }) => option.name === 'name'    )    return json({      // Type 4 responds with the below message retaining the user's      // input at the top.      type: 4,      data: {        content: `Hello, ${value}!`,      },    })  }  // We will return a bad request error as a valid Discord request  // shouldn't reach here.  return json({ error: 'bad request' }, { status: 400 })}/** Verify whether the request is coming from Discord. */async function verifySignature(request: Request): Promise<{ valid: boolean; body: string }> {  const PUBLIC_KEY = Deno.env.get('DISCORD_PUBLIC_KEY')!  // Discord sends these headers with every request.  const signature = request.headers.get('X-Signature-Ed25519')!  const timestamp = request.headers.get('X-Signature-Timestamp')!  const body = await request.text()  const valid = nacl.sign.detached.verify(    new TextEncoder().encode(timestamp + body),    hexToUint8Array(signature),    hexToUint8Array(PUBLIC_KEY)  )  return { valid, body }}/** Converts a hexadecimal string to Uint8Array. */function hexToUint8Array(hex: string) {  return new Uint8Array(hex.match(/.{1,2}/g)!.map((val) => parseInt(val, 16)))}
```

## Deploy the slash command handler [\#](https://supabase.com/docs/guides/functions/examples/discord-bot\#deploy-the-slash-command-handler)

```flex

1
2
supabase functions deploy discord-bot --no-verify-jwtsupabase secrets set DISCORD_PUBLIC_KEY=your_public_key
```

Navigate to your Function details in the Supabase Dashboard to get your Endpoint URL.

### Configure Discord application to use our URL as interactions endpoint URL [\#](https://supabase.com/docs/guides/functions/examples/discord-bot\#configure-discord-application-to-use-our-url-as-interactions-endpoint-url)

1. Go back to your application (Greeter) page on Discord Developer Portal
2. Fill **INTERACTIONS ENDPOINT URL** field with the URL and click on **Save Changes**.

The application is now ready. Let's proceed to the next section to install it.

## Install the slash command on your Discord server [\#](https://supabase.com/docs/guides/functions/examples/discord-bot\#install-the-slash-command-on-your-discord-server)

So to use the `hello` Slash Command, we need to install our Greeter application on our Discord server. Here are the steps:

1. Go to **OAuth2** section of the Discord application page on Discord Developer Portal
2. Select `applications.commands` scope and click on the **Copy** button below.
3. Now paste and visit the URL on your browser. Select your server and click on **Authorize**.

Open Discord, type `/Promise` and press **Enter**.

## Run locally [\#](https://supabase.com/docs/guides/functions/examples/discord-bot\#run-locally)

```flex

1
2
supabase functions serve discord-bot --no-verify-jwt --env-file ./supabase/.env.localngrok http 54321
```

### Is this helpful?

NoYes

### On this page

[Create an application on Discord Developer portal](https://supabase.com/docs/guides/functions/examples/discord-bot#create-an-application-on-discord-developer-portal) [Code](https://supabase.com/docs/guides/functions/examples/discord-bot#code) [Deploy the slash command handler](https://supabase.com/docs/guides/functions/examples/discord-bot#deploy-the-slash-command-handler) [Configure Discord application to use our URL as interactions endpoint URL](https://supabase.com/docs/guides/functions/examples/discord-bot#configure-discord-application-to-use-our-url-as-interactions-endpoint-url) [Install the slash command on your Discord server](https://supabase.com/docs/guides/functions/examples/discord-bot#install-the-slash-command-on-your-discord-server) [Run locally](https://supabase.com/docs/guides/functions/examples/discord-bot#run-locally)