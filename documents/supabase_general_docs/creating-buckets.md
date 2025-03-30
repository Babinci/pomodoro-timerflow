31 APR - 04 MAR / 7AM PT

Launch Week 14

03d

:

18h

:

09m

:

58s

[Claim ticket](https://supabase.com/launch-week)Dismiss

![](https://supabase.com/docs/_next/image?url=%2Fdocs%2Fimg%2Flaunchweek%2F14%2Fpromo-banner-bg.png&w=3840&q=100&dpl=dpl_9WgBm3X43HXGqPuPh4vSvQgRaZyZ)

Storage

# Creating Buckets

* * *

You can create a bucket using the Supabase Dashboard. Since storage is interoperable with your Postgres database, you can also use SQL or our client libraries.
Here we create a bucket called "avatars":

JavaScriptDashboardSQLDartSwiftPython

```flex

1
2
3
4
5
// Use the JS library to create a bucket.const { data, error } = await supabase.storage.createBucket('avatars', {  public: true, // default: false})
```

[Reference.](https://supabase.com/docs/reference/javascript/storage-createbucket)

## Restricting uploads [\#](https://supabase.com/docs/guides/storage/buckets/creating-buckets\#restricting-uploads)

When creating a bucket you can add additional configurations to restrict the type or size of files you want this bucket to contain.
For example, imagine you want to allow your users to upload only images to the `avatars` bucket and the size must not be greater than 1MB.

You can achieve the following by providing: `allowedMimeTypes` and `maxFileSize`

```flex

1
2
3
4
5
6
7
// Use the JS library to create a bucket.const { data, error } = await supabase.storage.createBucket('avatars', {  public: true,  allowedMimeTypes: ['image/*'],  fileSizeLimit: '1MB',})
```

If an upload request doesn't meet the above restrictions it will be rejected.

For more information check [File Limits](https://supabase.com/docs/guides/storage/uploads/file-limits) Section.

### Is this helpful?

NoYes

### On this page

[Restricting uploads](https://supabase.com/docs/guides/storage/buckets/creating-buckets#restricting-uploads)