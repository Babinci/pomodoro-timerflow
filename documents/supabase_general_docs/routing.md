31 APR - 04 MAR / 7AM PT

Launch Week 14

03d

:

18h

:

21m

:

08s

[Claim ticket](https://supabase.com/launch-week)Dismiss

![](https://supabase.com/docs/_next/image?url=%2Fdocs%2Fimg%2Flaunchweek%2F14%2Fpromo-banner-bg.png&w=3840&q=100&dpl=dpl_9WgBm3X43HXGqPuPh4vSvQgRaZyZ)

Edge Functions

# Handling Routing in Functions

## How to handle custom routing within Edge Functions.

* * *

Usually, an Edge Function is written to perform a single action (e.g. write a record to the database). However, if your app's logic is split into multiple Edge Functions requests to each action may seem slower.
This is because each Edge Function needs to be booted before serving a request (known as cold starts). If an action is performed less frequently (e.g. deleting a record), there is a high-chance of that function experiencing a cold-start.

One way to reduce the cold starts and increase performance of your app is to combine multiple actions into a single Edge Function. This way only one instance of the Edge Function needs to be booted and it can handle multiple requests to different actions.
For example, we can use a single Edge Function to create a typical CRUD API (create, read, update, delete records).

To combine multiple endpoints into a single Edge Function, you can use web application frameworks such as [Express](https://expressjs.com/), [Oak](https://oakserver.github.io/oak/), or [Hono](https://hono.dev/).

Let's dive into some examples.

## Routing with frameworks [\#](https://supabase.com/docs/guides/functions/routing\#routing-with-frameworks)

Here's a simple hello world example using some popular web frameworks.

Create a new function called `hello-world` using Supabase CLI:

```flex

1
supabase functions new hello-world
```

Copy and paste the following code:

ExpressOakHonoDeno

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
import { Hono } from 'jsr:@hono/hono';const app = new Hono();app.post('/hello-world', async (c) => {  const { name } = await c.req.json();  return new Response(`Hello ${name}!`)});app.get('/hello-world', (c) => {  return new Response('Hello World!')});Deno.serve(app.fetch);
```

You will notice in the above example, we created two routes - `GET` and `POST`. The path for both routes are defined as `/hello-world`.
If you run a server outside of Edge Functions, you'd usually set the root path as `/` .
However, within Edge Functions, paths should always be prefixed with the function name (in this case `hello-world`).

You can deploy the function to Supabase via:

```flex

1
supabase functions deploy hello-world
```

Once the function is deployed, you can try to call the two endpoints using cURL (or Postman).

```flex

1
2
3
# https://supabase.com/docs/guides/functions/deploy#invoking-remote-functionscurl --request GET 'https://<project_ref>.supabase.co/functions/v1/hello-world' \  --header 'Authorization: Bearer ANON_KEY' \
```

This should print the response as `Hello World!`, meaning it was handled by the `GET` route.

Similarly, we can make a request to the `POST` route.

```flex

1
2
3
4
5
# https://supabase.com/docs/guides/functions/deploy#invoking-remote-functionscurl --request POST 'https://<project_ref>.supabase.co/functions/v1/hello-world' \  --header 'Authorization: Bearer ANON_KEY' \  --header 'Content-Type: application/json' \  --data '{ "name":"Foo" }'
```

We should see a response printing `Hello Foo!`.

## Using route parameters [\#](https://supabase.com/docs/guides/functions/routing\#using-route-parameters)

We can use route parameters to capture values at specific URL segments (e.g. `/tasks/:taskId/notes/:noteId`).

Here's an example Edge Function implemented using the Framework for managing tasks using route parameters.
Keep in mind paths must be prefixed by function name (i.e. `tasks` in this example). Route parameters can only be used after the function name prefix.

ExpressOakHonoDeno

## URL patterns API [\#](https://supabase.com/docs/guides/functions/routing\#url-patterns-api)

If you prefer not to use a web framework, you can directly use [URL Pattern API](https://developer.mozilla.org/en-US/docs/Web/API/URL_Pattern_API) within your Edge Functions to implement routing.
This is ideal for small apps with only couple of routes and you want to have a custom matching algorithm.

Here is an example Edge Function using URL Patterns API: [https://github.com/supabase/supabase/blob/master/examples/edge-functions/supabase/functions/restful-tasks/index.ts](https://github.com/supabase/supabase/blob/master/examples/edge-functions/supabase/functions/restful-tasks/index.ts)

### Is this helpful?

NoYes

### On this page

[Routing with frameworks](https://supabase.com/docs/guides/functions/routing#routing-with-frameworks) [Using route parameters](https://supabase.com/docs/guides/functions/routing#using-route-parameters) [URL patterns API](https://supabase.com/docs/guides/functions/routing#url-patterns-api)