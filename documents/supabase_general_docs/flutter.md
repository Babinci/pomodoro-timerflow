31 APR - 04 MAR / 7AM PT

Launch Week 14

03d

:

18h

:

17m

:

02s

[Claim ticket](https://supabase.com/launch-week)Dismiss

![](https://supabase.com/docs/_next/image?url=%2Fdocs%2Fimg%2Flaunchweek%2F14%2Fpromo-banner-bg.png&w=3840&q=100&dpl=dpl_9WgBm3X43HXGqPuPh4vSvQgRaZyZ)

Getting Started

# Use Supabase with Flutter

## Learn how to create a Supabase project, add some sample data to your database, and query the data from a Flutter app.

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

### Create a Flutter app

Create a Flutter app using the `flutter create` command. You can skip this step if you already have a working app.

```flex

1
flutter create my_app
```

3

### Install the Supabase client library

The fastest way to get started is to use the [`supabase_flutter`](https://pub.dev/packages/supabase_flutter) client library which provides a convenient interface for working with Supabase from a Flutter app.

Open the `pubspec.yaml` file inside your Flutter app and add `supabase_flutter` as a dependency.

```flex

1
supabase_flutter: ^2.0.0
```

4

### Initialize the Supabase client

Open `lib/main.dart` and edit the main function to initialize Supabase using your project URL and public API (anon) key:

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
10
11
import 'package:supabase_flutter/supabase_flutter.dart';Future<void> main() async {  WidgetsFlutterBinding.ensureInitialized();  await Supabase.initialize(    url: 'YOUR_SUPABASE_URL',    anonKey: 'YOUR_SUPABASE_ANON_KEY',  );  runApp(MyApp());}
```

5

### Query data from the app

Use a `FutureBuilder` to fetch the data when the home page loads and display the query result in a `ListView`.

Replace the default `MyApp` and `MyHomePage` classes with the following code.

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
class MyApp extends StatelessWidget {  const MyApp({super.key});  @override  Widget build(BuildContext context) {    return const MaterialApp(      title: 'Instruments',      home: HomePage(),    );  }}class HomePage extends StatefulWidget {  const HomePage({super.key});  @override  State<HomePage> createState() => _HomePageState();}class _HomePageState extends State<HomePage> {  final _future = Supabase.instance.client      .from('instruments')      .select();  @override  Widget build(BuildContext context) {    return Scaffold(      body: FutureBuilder(        future: _future,        builder: (context, snapshot) {          if (!snapshot.hasData) {            return const Center(child: CircularProgressIndicator());          }          final instruments = snapshot.data!;          return ListView.builder(            itemCount: instruments.length,            itemBuilder: ((context, index) {              final instrument = instruments[index];              return ListTile(                title: Text(instrument['name']),              );            }),          );        },      ),    );  }}
```

6

### Start the app

Run your app on a platform of your choosing! By default an app should launch in your web browser.

Note that `supabase_flutter` is compatible with web, iOS, Android, macOS, and Windows apps.
Running the app on macOS requires additional configuration to [set the entitlements](https://docs.flutter.dev/development/platform-integration/macos/building#setting-up-entitlements).

```flex

1
flutter run
```

## Setup deep links [\#](https://supabase.com/docs/guides/getting-started/quickstarts/flutter\#setup-deep-links)

Many sign in methods require deep links to redirect the user back to your app after authentication. Read more about setting deep links up for all platforms (including web) in the [Flutter Mobile Guide](https://supabase.com/docs/guides/getting-started/tutorials/with-flutter#setup-deep-links).

## Going to production [\#](https://supabase.com/docs/guides/getting-started/quickstarts/flutter\#going-to-production)

### Android [\#](https://supabase.com/docs/guides/getting-started/quickstarts/flutter\#android)

In production, your Android app needs explicit permission to use the internet connection on the user's device which is required to communicate with Supabase APIs.
To do this, add the following line to the `android/app/src/main/AndroidManifest.xml` file.

```flex

1
2
3
4
5
<manifest xmlns:android="http://schemas.android.com/apk/res/android">  <!-- Required to fetch data from the internet. -->  <uses-permission android:name="android.permission.INTERNET" />  <!-- ... --></manifest>
```