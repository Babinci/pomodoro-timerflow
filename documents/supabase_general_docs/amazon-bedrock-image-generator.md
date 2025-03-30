31 APR - 04 MAR / 7AM PT

Launch Week 14

03d

:

18h

:

16m

:

00s

[Claim ticket](https://supabase.com/launch-week)Dismiss

![](https://supabase.com/docs/_next/image?url=%2Fdocs%2Fimg%2Flaunchweek%2F14%2Fpromo-banner-bg.png&w=3840&q=100&dpl=dpl_9WgBm3X43HXGqPuPh4vSvQgRaZyZ)

Edge Functions

# Generate Images with Amazon Bedrock

* * *

[Amazon Bedrock](https://aws.amazon.com/bedrock) is a fully managed service that offers a choice of high-performing foundation models (FMs) from leading AI companies like AI21 Labs, Anthropic, Cohere, Meta, Mistral AI, Stability AI, and Amazon. Each model is accessible through a common API which implements a broad set of features to help build generative AI applications with security, privacy, and responsible AI in mind.

This guide will walk you through an example using the Amazon Bedrock JavaScript SDK in Supabase Edge Functions to generate images using the [Amazon Titan Image Generator G1](https://aws.amazon.com/blogs/machine-learning/use-amazon-titan-models-for-image-generation-editing-and-searching/) model.

## Setup [\#](https://supabase.com/docs/guides/functions/examples/amazon-bedrock-image-generator\#setup)

- In your AWS console, navigate to Amazon Bedrock and under "Request model access", select the Amazon Titan Image Generator G1 model.
- In your Supabase project, create a `.env` file in the `supabase` directory with the following contents:

```flex

1
2
3
4
5
6
7
8
AWS_DEFAULT_REGION="<your_region>"AWS_ACCESS_KEY_ID="<replace_your_own_credentials>"AWS_SECRET_ACCESS_KEY="<replace_your_own_credentials>"AWS_SESSION_TOKEN="<replace_your_own_credentials>"# Mocked config filesAWS_SHARED_CREDENTIALS_FILE="./aws/credentials"AWS_CONFIG_FILE="./aws/config"
```

### Configure Storage [\#](https://supabase.com/docs/guides/functions/examples/amazon-bedrock-image-generator\#configure-storage)

- \[locally\] Run `supabase start`
- Open Studio URL: [locally](http://127.0.0.1:54323/project/default/storage/buckets) \| [hosted](https://app.supabase.com/project/_/storage/buckets)
- Navigate to Storage
- Click "New bucket"
- Create a new public bucket called "images"

## Code [\#](https://supabase.com/docs/guides/functions/examples/amazon-bedrock-image-generator\#code)

Create a new function in your project:

```flex

1
supabase functions new amazon-bedrock
```

And add the code to the `index.ts` file:

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
// We need to mock the file system for the AWS SDK to work.import { prepareVirtualFile } from 'https://deno.land/x/mock_file@v1.1.2/mod.ts'import { BedrockRuntimeClient, InvokeModelCommand } from 'npm:@aws-sdk/client-bedrock-runtime'import { createClient } from 'npm:@supabase/supabase-js'import { decode } from 'npm:base64-arraybuffer'console.log('Hello from Amazon Bedrock!')Deno.serve(async (req) => {  prepareVirtualFile('./aws/config')  prepareVirtualFile('./aws/credentials')  const client = new BedrockRuntimeClient({    region: Deno.env.get('AWS_DEFAULT_REGION') ?? 'us-west-2',    credentials: {      accessKeyId: Deno.env.get('AWS_ACCESS_KEY_ID') ?? '',      secretAccessKey: Deno.env.get('AWS_SECRET_ACCESS_KEY') ?? '',      sessionToken: Deno.env.get('AWS_SESSION_TOKEN') ?? '',    },  })  const { prompt, seed } = await req.json()  console.log(prompt)  const input = {    contentType: 'application/json',    accept: '*/*',    modelId: 'amazon.titan-image-generator-v1',    body: JSON.stringify({      taskType: 'TEXT_IMAGE',      textToImageParams: { text: prompt },      imageGenerationConfig: {        numberOfImages: 1,        quality: 'standard',        cfgScale: 8.0,        height: 512,        width: 512,        seed: seed ?? 0,      },    }),  }  const command = new InvokeModelCommand(input)  const response = await client.send(command)  console.log(response)  if (response.$metadata.httpStatusCode === 200) {    const { body, $metadata } = response    const textDecoder = new TextDecoder('utf-8')    const jsonString = textDecoder.decode(body.buffer)    const parsedData = JSON.parse(jsonString)    console.log(parsedData)    const image = parsedData.images[0]    const supabaseClient = createClient(      // Supabase API URL - env var exported by default.      Deno.env.get('SUPABASE_URL')!,      // Supabase API ANON KEY - env var exported by default.      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!    )    const { data: upload, error: uploadError } = await supabaseClient.storage      .from('images')      .upload(`${$metadata.requestId ?? ''}.png`, decode(image), {        contentType: 'image/png',        cacheControl: '3600',        upsert: false,      })    if (!upload) {      return Response.json(uploadError)    }    const { data } = supabaseClient.storage.from('images').getPublicUrl(upload.path!)    return Response.json(data)  }  return Response.json(response)})
```

## Run the function locally [\#](https://supabase.com/docs/guides/functions/examples/amazon-bedrock-image-generator\#run-the-function-locally)

1. Run `supabase start` (see: [https://supabase.com/docs/reference/cli/supabase-start](https://supabase.com/docs/reference/cli/supabase-start))
2. Start with env: `supabase functions serve --env-file supabase/.env`
3. Make an HTTP request:

```flex

1
2
3
4
curl -i --location --request POST 'http://127.0.0.1:54321/functions/v1/amazon-bedrock' \    --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0' \    --header 'Content-Type: application/json' \    --data '{"prompt":"A beautiful picture of a bird"}'
```

4. Navigate back to your storage bucket. You might have to hit the refresh button to see the uploaded image.

## Deploy to your hosted project [\#](https://supabase.com/docs/guides/functions/examples/amazon-bedrock-image-generator\#deploy-to-your-hosted-project)

```flex

1
2
3
supabase linksupabase functions deploy amazon-bedrocksupabase secrets set --env-file supabase/.env
```

You've now deployed a serverless function that uses AI to generate and upload images to your Supabase storage bucket.

Watch video guide

![Video guide preview](https://supabase.com/docs/_next/image?url=https%3A%2F%2Fimg.youtube.com%2Fvi%2FKIwN2TmkTlg%2F0.jpg&w=3840&q=75&dpl=dpl_9WgBm3X43HXGqPuPh4vSvQgRaZyZ)

### Is this helpful?

NoYes

### On this page

[Setup](https://supabase.com/docs/guides/functions/examples/amazon-bedrock-image-generator#setup) [Configure Storage](https://supabase.com/docs/guides/functions/examples/amazon-bedrock-image-generator#configure-storage) [Code](https://supabase.com/docs/guides/functions/examples/amazon-bedrock-image-generator#code) [Run the function locally](https://supabase.com/docs/guides/functions/examples/amazon-bedrock-image-generator#run-the-function-locally) [Deploy to your hosted project](https://supabase.com/docs/guides/functions/examples/amazon-bedrock-image-generator#deploy-to-your-hosted-project)