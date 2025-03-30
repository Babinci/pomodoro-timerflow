31 APR - 04 MAR / 7AM PT

Launch Week 14

03d

:

18h

:

11m

:

14s

[Claim ticket](https://supabase.com/launch-week)Dismiss

![](https://supabase.com/docs/_next/image?url=%2Fdocs%2Fimg%2Flaunchweek%2F14%2Fpromo-banner-bg.png&w=3840&q=100&dpl=dpl_9WgBm3X43HXGqPuPh4vSvQgRaZyZ)

Edge Functions

# Handling Compressed Requests

## Handling Gzip compressed requests.

* * *

To decompress Gzip bodies, you can use `gunzipSync` from the `node:zlib` API to decompress and then read the body.

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
import { gunzipSync } from 'node:zlib'Deno.serve(async (req) => {  try {    // Check if the request body is gzip compressed    const contentEncoding = req.headers.get('content-encoding')    if (contentEncoding !== 'gzip') {      return new Response('Request body is not gzip compressed', {        status: 400,      })    }    // Read the compressed body    const compressedBody = await req.arrayBuffer()    // Decompress the body    const decompressedBody = gunzipSync(new Uint8Array(compressedBody))    // Convert the decompressed body to a string    const decompressedString = new TextDecoder().decode(decompressedBody)    const data = JSON.parse(decompressedString)    // Process the decompressed body as needed    console.log(`Received: ${JSON.stringify(data)}`)    return new Response('ok', {      headers: { 'Content-Type': 'text/plain' },    })  } catch (error) {    console.error('Error:', error)    return new Response('Error processing request', { status: 500 })  }})
```

Edge functions have a runtime memory limit of 150MB. Overly large compressed payloads may result in an out-of-memory error.

### Is this helpful?

NoYes