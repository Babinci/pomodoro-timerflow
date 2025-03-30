Getting Started

# Use Supabase with SolidJS

## Learn how to create a Supabase project, add some sample data to your database, and query the data from a SolidJS app.

* * *

1

### Create a Supabase project

Go to [database.new](https://database.new/) and create a new Supabase project.

When your project is up and running, go to the [Table Editor](https://supabase.com/dashboard/project/_/editor), create a new table and insert some data.

Alternatively, you can run the following snippet in your project's [SQL Editor](https://supabase.com/dashboard/project/_/sql/new). This will create a `instruments` table with some sample data.

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
-- Create the tablecreate table instruments (  id bigint primary key generated always as identity,  name text not null);-- Insert some sample data into the tableinsert into instruments (name)values  ('violin'),  ('viola'),  ('cello');alter table instruments enable row level security;
```

Make the data in your table publicly readable by adding an RLS policy:

```flex

1
2
3
4
create policy "public can read instruments"on public.instrumentsfor select to anonusing (true);
```

2

### Create a SolidJS app

Create a SolidJS app using the `degit` command.

```flex

1
npx degit solidjs/templates/js my-app
```

3

### Install the Supabase client library

The fastest way to get started is to use the `supabase-js` client library which provides a convenient interface for working with Supabase from a SolidJS app.

Navigate to the SolidJS app and install `supabase-js`.

```flex

1
cd my-app && npm install @supabase/supabase-js
```

4

### Query data from the app

In `App.jsx`, create a Supabase client using your project URL and public API (anon) key:

###### Project URL

No project found

To get your Project URL, [log in](https://supabase.com/dashboard).

###### Anon key

No project found

To get your Anon key, [log in](https://supabase.com/dashboard).

Add a `getInstruments` function to fetch the data and display the query result to the page.

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
import { createClient } from "@supabase/supabase-js";  import { createResource, For } from "solid-js";  const supabase = createClient('https://<project>.supabase.co', '<your-anon-key>');  async function getInstruments() {    const { data } = await supabase.from("instruments").select();    return data;  }  function App() {    const [instruments] = createResource(getInstruments);    return (      <ul>        <For each={instruments()}>{(instrument) => <li>{instrument.name}</li>}</For>      </ul>    );  }  export default App;
```

5

### Start the app

Start the app and go to [http://localhost:3000](http://localhost:3000/) in a browser and you should see the list of instruments.

```flex

1
npm run dev
```

1. We use first-party cookies to improve our services. [Learn more](https://supabase.com/privacy#8-cookies-and-similar-technologies-used-on-our-european-services)



   [Learn more](https://supabase.com/privacy#8-cookies-and-similar-technologies-used-on-our-european-services)•Privacy settings





   AcceptOpt outPrivacy settings