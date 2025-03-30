Auth

# Use Supabase Auth with React Native

## Learn how to use Supabase Auth with React Native

* * *

1

### Create a new Supabase project

[Launch a new project](https://supabase.com/dashboard) in the Supabase Dashboard.

Your new database has a table for storing your users. You can see that this table is currently empty by running some SQL in the [SQL Editor](https://supabase.com/dashboard/project/_/sql).

```flex

1
select * from auth.users;
```

2

### Create a React app

Create a React app using the `create-expo-app` command.

```flex

1
npx create-expo-app -t expo-template-blank-typescript my-app
```

3

### Install the Supabase client library

Install `supabase-js` and the required dependencies.

```flex

1
cd my-app && npx expo install @supabase/supabase-js @react-native-async-storage/async-storage @rneui/themed react-native-url-polyfill
```

4

### Set up your login component

Create a helper file `lib/supabase.ts` that exports a Supabase client using your [Project URL and public API (anon) key](https://supabase.com/dashboard/project/_/settings/api).

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
import { AppState } from 'react-native'import 'react-native-url-polyfill/auto'import AsyncStorage from '@react-native-async-storage/async-storage'import { createClient } from '@supabase/supabase-js'const supabaseUrl = YOUR_REACT_NATIVE_SUPABASE_URLconst supabaseAnonKey = YOUR_REACT_NATIVE_SUPABASE_ANON_KEYexport const supabase = createClient(supabaseUrl, supabaseAnonKey, {  auth: {    storage: AsyncStorage,    autoRefreshToken: true,    persistSession: true,    detectSessionInUrl: false,  },})// Tells Supabase Auth to continuously refresh the session automatically// if the app is in the foreground. When this is added, you will continue// to receive `onAuthStateChange` events with the `TOKEN_REFRESHED` or// `SIGNED_OUT` event if the user's session is terminated. This should// only be registered once.AppState.addEventListener('change', (state) => {  if (state === 'active') {    supabase.auth.startAutoRefresh()  } else {    supabase.auth.stopAutoRefresh()  }})
```

5

### Create a login component

Let's set up a React Native component to manage logins and sign ups.

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
79
80
81
82
83
import React, { useState } from 'react'import { Alert, StyleSheet, View } from 'react-native'import { supabase } from '../lib/supabase'import { Button, Input } from '@rneui/themed'export default function Auth() {  const [email, setEmail] = useState('')  const [password, setPassword] = useState('')  const [loading, setLoading] = useState(false)  async function signInWithEmail() {    setLoading(true)    const { error } = await supabase.auth.signInWithPassword({      email: email,      password: password,    })    if (error) Alert.alert(error.message)    setLoading(false)  }  async function signUpWithEmail() {    setLoading(true)    const {      data: { session },      error,    } = await supabase.auth.signUp({      email: email,      password: password,    })    if (error) Alert.alert(error.message)    if (!session) Alert.alert('Please check your inbox for email verification!')    setLoading(false)  }  return (    <View style={styles.container}>      <View style={[styles.verticallySpaced, styles.mt20]}>        <Input          label="Email"          leftIcon={{ type: 'font-awesome', name: 'envelope' }}          onChangeText={(text) => setEmail(text)}          value={email}          placeholder="email@address.com"          autoCapitalize={'none'}        />      </View>      <View style={styles.verticallySpaced}>        <Input          label="Password"          leftIcon={{ type: 'font-awesome', name: 'lock' }}          onChangeText={(text) => setPassword(text)}          value={password}          secureTextEntry={true}          placeholder="Password"          autoCapitalize={'none'}        />      </View>      <View style={[styles.verticallySpaced, styles.mt20]}>        <Button title="Sign in" disabled={loading} onPress={() => signInWithEmail()} />      </View>      <View style={styles.verticallySpaced}>        <Button title="Sign up" disabled={loading} onPress={() => signUpWithEmail()} />      </View>    </View>  )}const styles = StyleSheet.create({  container: {    marginTop: 40,    padding: 12,  },  verticallySpaced: {    paddingTop: 4,    paddingBottom: 4,    alignSelf: 'stretch',  },  mt20: {    marginTop: 20,  },})
```

6

### Add the Auth component to your app

Add the `Auth` component to your `App.tsx` file. If the user is logged in, print the user id to the screen.

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
import 'react-native-url-polyfill/auto'import { useState, useEffect } from 'react'import { supabase } from './lib/supabase'import Auth from './components/Auth'import { View, Text } from 'react-native'import { Session } from '@supabase/supabase-js'export default function App() {  const [session, setSession] = useState<Session | null>(null)  useEffect(() => {    supabase.auth.getSession().then(({ data: { session } }) => {      setSession(session)    })    supabase.auth.onAuthStateChange((_event, session) => {      setSession(session)    })  }, [])  return (    <View>      <Auth />      {session && session.user && <Text>{session.user.id}</Text>}    </View>  )}
```

7

### Start the app

Start the app, and follow the instructions in the terminal.

```flex

1
npm start
```

1. We use first-party cookies to improve our services. [Learn more](https://supabase.com/privacy#8-cookies-and-similar-technologies-used-on-our-european-services)



   [Learn more](https://supabase.com/privacy#8-cookies-and-similar-technologies-used-on-our-european-services)•Privacy settings





   AcceptOpt outPrivacy settings