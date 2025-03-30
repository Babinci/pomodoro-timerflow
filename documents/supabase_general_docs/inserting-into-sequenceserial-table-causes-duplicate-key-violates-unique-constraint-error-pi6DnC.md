# Inserting into Sequence/Serial Table Causes "duplicate key violates unique constraint" Error

Last edited: 1/16/2025

* * *

If you are receiving the below error for an auto-incremented table:

> ERROR: duplicate key violates unique constraint

it likely means that the table's sequence has somehow become out of sync, likely because of a mass import process (or something along those lines).

Call it a "bug by design", but it seems that you have to manually reset the a primary key index after restoring from a dump file.

You can run the following commands on your instance to see if your sequence is out-of-sync:

```flex

1
2
3
SELECT MAX(<sequenced_column>) FROM <table_name>;SELECT nextval(pg_get_serial_sequence('<public.table_name>', '<sequenced_column_name>'));
```

If the values are off by more than 1, you need to resynchronize your sequence.

Back up your PG database by restarting in the [General Settings](https://supabase.com/dashboard/project/_/settings/general) (just in case). When you restore your database, you will have a backup saved. Alternatively, you can also just download your properties table instead as a backup.

Then you can run this:

```flex

1
SELECT SETVAL('public.<table_name>_<column_nam>_seq', (SELECT MAX(<column_name>) FROM <table_name>)+1);
```

That will set the sequence to the next available value that's higher than any existing primary key in the sequence.

1. We use first-party cookies to improve our services. [Learn more](https://supabase.com/privacy#8-cookies-and-similar-technologies-used-on-our-european-services)



   [Learn more](https://supabase.com/privacy#8-cookies-and-similar-technologies-used-on-our-european-services)•Privacy settings





   AcceptOpt outPrivacy settings