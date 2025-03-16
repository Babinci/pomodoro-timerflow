Installing it locally:


(venv) wojtek@wojtek-Latitude-E6420:~/It_Projects/pomodoro-timerflow$ npm install supabase --save-dev

added 66 packages in 7s

18 packages are looking for funding
  run `npm fund` for details


  (venv) wojtek@wojtek-Latitude-E6420:~/It_Projects/pomodoro-timerflow$ npx supabase init
Generate VS Code settings for Deno? [y/N] y
Generated VS Code settings in .vscode/settings.json. Please install the recommended extension!
Finished supabase init.


installed extension:
Deno
denoland
deno.land
989,548
(51)
A language server client for Deno.

then- started supabase

npx supabase start- it should be running on  http://localhost:54323

(venv) wojtek@wojtek-Latitude-E6420:~/It_Projects/pomodoro-timerflow$ npx supabase start
15.8.1.049: Pulling from supabase/postgres

Started supabase local development setup.


Notes from Supabase:
Local development#
Local development with Supabase allows you to work on your projects in a self-contained environment on your local machine. Working locally has several advantages:

Faster development: You can make changes and see results instantly without waiting for remote deployments.
Offline work: You can continue development even without an internet connection.
Cost-effective: Local development is free and doesn't consume your project's quota.
Enhanced privacy: Sensitive data remains on your local machine during development.
Easy testing: You can experiment with different configurations and features without affecting your production environment.
To get started with local development, you'll need to install the Supabase CLI and Docker. The Supabase CLI allows you to start and manage your local Supabase stack, while Docker is used to run the necessary services.

Once set up, you can initialize a new Supabase project, start the local stack, and begin developing your application using local Supabase services. This includes access to a local Postgres database, Auth, Storage, and other Supabase features.


tried cli
(venv) wojtek@wojtek-Latitude-E6420:~/It_Projects/pomodoro-timerflow$ npx supabase help
Supabase CLI 2.19.7


status: https://supabase.cypher-arena.com/ working, as well as locally  curl http://localhost:54323


will use this:

https://github.com/supabase/supabase-py


next steps:
- i need to create database for project, handle migrations/ connect mcp server