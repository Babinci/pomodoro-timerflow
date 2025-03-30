Storage

# Storage Helper Functions

## Learn the storage schema

* * *

Supabase Storage provides SQL helper functions which you can use to write RLS policies.

### `storage.filename()` [\#](https://supabase.com/docs/guides/storage/schema/helper-functions\#storagefilename)

Returns the name of a file. For example, if your file is stored in `public/subfolder/avatar.png` it would return: `'avatar.png'`

**Usage**

This example demonstrates how you would allow any user to download a file called `favicon.ico`:

```flex

1
2
3
4
5
6
7
create policy "Allow public downloads"on storage.objectsfor selectto publicusing (  storage.filename(name) = 'favicon.ico');
```

### `storage.foldername()` [\#](https://supabase.com/docs/guides/storage/schema/helper-functions\#storagefoldername)

Returns an array path, with all of the subfolders that a file belongs to. For example, if your file is stored in `public/subfolder/avatar.png` it would return: `[ 'public', 'subfolder' ]`

**Usage**

This example demonstrates how you would allow authenticated users to upload files to a folder called `private`:

```flex

1
2
3
4
5
6
7
create policy "Allow authenticated uploads"on storage.objectsfor insertto authenticatedwith check (  (storage.foldername(name))[1] = 'private');
```

### `storage.extension()` [\#](https://supabase.com/docs/guides/storage/schema/helper-functions\#storageextension)

Returns the extension of a file. For example, if your file is stored in `public/subfolder/avatar.png` it would return: `'png'`

**Usage**

This example demonstrates how you would allow restrict uploads to only PNG files inside a bucket called `cats`:

```flex

1
2
3
4
5
6
7
create policy "Only allow PNG uploads"on storage.objectsfor insertto authenticatedwith check (  bucket_id = 'cats' and storage.extension(name) = 'png');
```

### Is this helpful?

NoYes

### On this page

[storage.filename()](https://supabase.com/docs/guides/storage/schema/helper-functions#storagefilename) [storage.foldername()](https://supabase.com/docs/guides/storage/schema/helper-functions#storagefoldername) [storage.extension()](https://supabase.com/docs/guides/storage/schema/helper-functions#storageextension)

1. We use first-party cookies to improve our services. [Learn more](https://supabase.com/privacy#8-cookies-and-similar-technologies-used-on-our-european-services)



   [Learn more](https://supabase.com/privacy#8-cookies-and-similar-technologies-used-on-our-european-services)•Privacy settings





   AcceptOpt outPrivacy settings