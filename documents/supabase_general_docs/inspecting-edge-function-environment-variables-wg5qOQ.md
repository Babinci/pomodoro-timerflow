# Inspecting edge function environment variables

Last edited: 2/4/2025

* * *

Sometimes it can be informative to log values from your Edge Functions. This walks you through the process of logging environment variables for inspection, but it can be generalized for all logging.

**Steps:**

1. enable docker

2. Create a local Supabase project


```flex

1
npx supabase init
```

3. create a .env file in the `supabase` folder

```flex

1
echo "MY_NAME=Some_name" >> ./supabase/.env
```

4. deploy the newly added secret

```flex

1
npx supabase secrets set --env-file ./supabase/.env --project-ref <PROJECT REF>
```

5. Run the following CLI command to check secrets:

```flex

1
npx supabase secrets list
```

For security reasons, it is not advised to log secrets, but you can log a truncated version just for the reassurance that they're being updated:

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
//logs the function call and the secretsconsole.log('Hello from Functions!')//custom secretconsole.log('logging custom secret', Deno.env.get('MY_NAME'))// default secretsconsole.log('logging SUPABASE_URL:', Deno.env.get('SUPABASE_URL').slice(0, 15))Deno.serve(async (req) => {  const { name } = await req.json()  const data = {    message: `Hello ${name}!`,  }  return new Response(JSON.stringify(data), { headers: { 'Content-Type': 'application/json' } })})
```

After calling your function, you can check your [edge function logs](https://supabase.com/dashboard/project/_/functions/hello-world/logs?s=logging) to observe the logged values. It should look something like this:

> Note: search filters are case sensitive and must be present in the event message.

![image](https://supabase.com/docs/img/troubleshooting/a360b417-e0cc-4706-8df4-89af63dcdc70.png)

> Note: excessively long JSON logs may be truncated. If this occurs, use the [JSON.stringify()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/stringify) function to convert the JSON object into text. You can then copy and paste the log into a [JSON beautifier.](https://jsonformatter.org/)

1. We use first-party cookies to improve our services. [Learn more](https://supabase.com/privacy#8-cookies-and-similar-technologies-used-on-our-european-services)



   [Learn more](https://supabase.com/privacy#8-cookies-and-similar-technologies-used-on-our-european-services)•Privacy settings





   AcceptOpt outPrivacy settings