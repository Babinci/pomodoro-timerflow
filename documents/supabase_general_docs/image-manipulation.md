Edge Functions

# Image Manipulation

* * *

Supabase Storage has [out-of-the-box support](https://supabase.com/docs/guides/storage/serving/image-transformations?queryGroups=language&language=js) for the most common image transformations and optimizations you need.
If you need to do anything custom beyond what Supabase Storage provides, you can use Edge Functions to write custom image manipulation scripts.

In this example, we will use [`magick-wasm`](https://github.com/dlemstra/magick-wasm) to perform image manipulations. `magick-wasm` is the WebAssembly port of the popular ImageMagick library and supports processing over 100 file formats.

Edge Functions currently doesn't support image processing libraries such as `Sharp`, which depend on native libraries. Only WASM-based libraries are supported.

### Prerequisites [\#](https://supabase.com/docs/guides/functions/examples/image-manipulation\#prerequisites)

Make sure you have the latest version of the [Supabase CLI](https://supabase.com/docs/guides/cli#installation) installed.

### Create the Edge Function [\#](https://supabase.com/docs/guides/functions/examples/image-manipulation\#create-the-edge-function)

Create a new function locally:

```flex

1
supabase functions new image-blur
```

### Write the function [\#](https://supabase.com/docs/guides/functions/examples/image-manipulation\#write-the-function)

In this example, we are implementing a function allowing users to upload an image and get a blurred thumbnail.

Here's the implementation in `index.ts` file:

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
// This is an example showing how to use Magick WASM to do image manipulations in Edge Functions.//import {  ImageMagick,  initializeImageMagick,  MagickFormat,} from "npm:@imagemagick/magick-wasm@0.0.30";const wasmBytes = await Deno.readFile(  new URL(    "magick.wasm",    import.meta.resolve("npm:@imagemagick/magick-wasm@0.0.30"),  ),);await initializeImageMagick(  wasmBytes,);Deno.serve(async (req) => {  const formData = await req.formData();  const content = await formData.get("file").bytes();  let result = ImageMagick.read(    content,    (img): Uint8Array => {      // resize the image      img.resize(500, 300);      // add a blur of 60x5      img.blur(60, 5);      return img.write(        (data) => data,      );    },  );  return new Response(    result,    { headers: { "Content-Type": "image/png" } },  );});
```

[View source](https://github.com/supabase/supabase/blob/641940e5464f0f894b0cf5b427a85e1686b9259b/examples/edge-functions/supabase/functions/image-manipulation/index.ts)

### Test it locally [\#](https://supabase.com/docs/guides/functions/examples/image-manipulation\#test-it-locally)

You can test the function locally by running:

```flex

1
2
supabase startsupabase functions serve --no-verify-jwt
```

Then, make a request using `curl` or your favorite API testing tool.

```flex

1
2
3
curl --location '<http://localhost:54321/functions/v1/image-blur>' \\--form 'file=@"/path/to/image.png"'--output '/path/to/output.png'
```

If you open the `output.png` file you will find a transformed version of your original image.

### Deploy to your hosted project [\#](https://supabase.com/docs/guides/functions/examples/image-manipulation\#deploy-to-your-hosted-project)

Now, let's deploy the function to your Supabase project.

```flex

1
2
supabase linksupabase functions deploy image-blur
```

Hosted Edge Functions have [limits](https://supabase.com/docs/guides/functions/limits) on memory and CPU usage.

If you try to perform complex image processing or handle large images (> 5MB) your function may return a resource limit exceeded error.

### Is this helpful?

NoYes

### On this page

[Prerequisites](https://supabase.com/docs/guides/functions/examples/image-manipulation#prerequisites) [Create the Edge Function](https://supabase.com/docs/guides/functions/examples/image-manipulation#create-the-edge-function) [Write the function](https://supabase.com/docs/guides/functions/examples/image-manipulation#write-the-function) [Test it locally](https://supabase.com/docs/guides/functions/examples/image-manipulation#test-it-locally) [Deploy to your hosted project](https://supabase.com/docs/guides/functions/examples/image-manipulation#deploy-to-your-hosted-project)

1. We use first-party cookies to improve our services. [Learn more](https://supabase.com/privacy#8-cookies-and-similar-technologies-used-on-our-european-services)



   [Learn more](https://supabase.com/privacy#8-cookies-and-similar-technologies-used-on-our-european-services)•Privacy settings





   AcceptOpt outPrivacy settings