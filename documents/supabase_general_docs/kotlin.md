Getting Started

# Use Supabase with Android Kotlin

## Learn how to create a Supabase project, add some sample data to your database, and query the data from an Android Kotlin app.

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

### Create an Android app with Android Studio

Open Android Studio > New > New Android Project.

3

### Install the Dependencies

Open `build.gradle.kts` (app) file and add the serialization plug, Ktor client, and Supabase client.

Replace the version placeholders `$kotlin_version` with the Kotlin version of the project, and `$supabase_version` and `$ktor_version` with the respective latest versions.

The latest supabase-kt version can be found [here](https://github.com/supabase-community/supabase-kt/releases) and Ktor version can be found [here](https://ktor.io/docs/welcome.html).

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
plugins {  ...  kotlin("plugin.serialization") version "$kotlin_version"}...dependencies {  ...  implementation(platform("io.github.jan-tennert.supabase:bom:$supabase_version"))  implementation("io.github.jan-tennert.supabase:postgrest-kt")  implementation("io.ktor:ktor-client-android:$ktor_version")}
```

4

### Add internet access permission

Add the following line to the `AndroidManifest.xml` file under the `manifest` tag and outside the `application` tag.

```flex

1
2
3
...<uses-permission android:name="android.permission.INTERNET" />...
```

5

### Initialize the Supabase client

You can create a Supabase client whenever you need to perform an API call.

For the sake of simplicity, we will create a client in the `MainActivity.kt` file at the top just below the imports.

Replace the `supabaseUrl` and `supabaseKey` with your own:

###### Project URL

No project found

To get your Project URL, [log in](https://supabase.com/dashboard).

###### Anon key

No project found

To get your Anon key, [log in](https://supabase.com/dashboard).

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
import ...val supabase = createSupabaseClient(    supabaseUrl = "https://xyzcompany.supabase.co",    supabaseKey = "your_public_anon_key"  ) {    install(Postgrest)}...
```

6

### Create a data model for instruments

Create a serializable data class to represent the data from the database.

Add the following below the `createSupabaseClient` function in the `MainActivity.kt` file.

```flex

1
2
3
4
5
@Serializabledata class Instrument(    val id: Int,    val name: String,)
```

7

### Query data from the app

Use `LaunchedEffect` to fetch data from the database and display it in a `LazyColumn`.

Replace the default `MainActivity` class with the following code.

Note that we are making a network request from our UI code. In production, you should probably use a `ViewModel` to separate the UI and data fetching logic.

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
class MainActivity : ComponentActivity() {    override fun onCreate(savedInstanceState: Bundle?) {        super.onCreate(savedInstanceState)        setContent {            SupabaseTutorialTheme {                // A surface container using the 'background' color from the theme                Surface(                    modifier = Modifier.fillMaxSize(),                    color = MaterialTheme.colorScheme.background                ) {                    InstrumentsList()                }            }        }    }}@Composablefun InstrumentsList() {    var instruments by remember { mutableStateOf<List<Instrument>>(listOf()) }    LaunchedEffect(Unit) {        withContext(Dispatchers.IO) {            instruments = supabase.from("instruments")                              .select().decodeList<Instrument>()        }    }    LazyColumn {        items(            instruments,            key = { instrument -> instrument.id },        ) { instrument ->            Text(                instrument.name,                modifier = Modifier.padding(8.dp),            )        }    }}
```

8

### Start the app

Run the app on an emulator or a physical device by clicking the `Run app` button in Android Studio.

1. We use first-party cookies to improve our services. [Learn more](https://supabase.com/privacy#8-cookies-and-similar-technologies-used-on-our-european-services)



   [Learn more](https://supabase.com/privacy#8-cookies-and-similar-technologies-used-on-our-european-services)•Privacy settings





   AcceptOpt outPrivacy settings