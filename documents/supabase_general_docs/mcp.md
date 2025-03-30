Getting Started

# Model context protocol (MCP)

* * *

The [Model Context Protocol](https://modelcontextprotocol.io/introduction) (MCP) is a standard for connecting Large Language Models (LLMs) to external services.

This guide covers how to connect Supabase to the following AI tools using MCP:

- [Cursor](https://www.cursor.com/)
- [Windsurf](https://docs.codeium.com/windsurf) (Codium)
- [Cline](https://github.com/cline/cline) (VS Code extension)
- [Claude desktop](https://claude.ai/download)
- [Claude code](https://claude.ai/code)

Once connected, you can use natural language commands to run read-only database queries in the AI tool.

## Connect to Supabase using MCP [\#](https://supabase.com/docs/guides/getting-started/mcp\#connect-to-supabase-using-mcp)

Supabase uses the [Postgres MCP server](https://github.com/modelcontextprotocol/servers/tree/main/src/postgres) to provide MCP access to your database. The MCP server runs all queries as read-only transactions.

### Step 1: Find your database connection string [\#](https://supabase.com/docs/guides/getting-started/mcp\#step-1-find-your-database-connection-string)

To get started, you will need to retrieve your database connection string. These will differ depending on whether you are using a hosted or local instance of Supabase.

#### For a hosted Supabase instance [\#](https://supabase.com/docs/guides/getting-started/mcp\#for-a-hosted-supabase-instance)

When running a hosted instance of Supabase, you can find your connection string by:

1. Navigating to your project's [Connection settings](https://supabase.com/dashboard/project/_/settings/database?showConnect=true)
2. Copying the connection string found under **Session pooler**.

#### For a local Supabase instance [\#](https://supabase.com/docs/guides/getting-started/mcp\#for-a-local-supabase-instance)

When running a local instance of Supabase via the [CLI](https://supabase.com/docs/reference/cli/introduction), you can find your connection string by running:

```flex

1
supabase status
```

or if you are using `npx`:

```flex

1
npx supabase status
```

This will output a list of details about your local Supabase instance. Copy the `DB URL` field in the output.

### Step 2: Configure in your AI tool [\#](https://supabase.com/docs/guides/getting-started/mcp\#step-2-configure-in-your-ai-tool)

MCP compatible tools can connect to Supabase using the [Postgres MCP server](https://github.com/modelcontextprotocol/servers/tree/main/src/postgres). Below are instructions on to connect to the Postgres MCP server using popular AI tools:

#### Cursor [\#](https://supabase.com/docs/guides/getting-started/mcp\#cursor)

1. Open Cursor and create a `.cursor` directory in your project root if it doesn't exist.

2. Create a `.cursor/mcp.json` file if it doesn't exist and open it.

3. Add the following configuration:



macOSWindowsWindows (WSL)Linux







```flex


1
2
3
4
5
6
7
8
{  "mcpServers": {    "supabase": {      "command": "npx",      "args": ["-y", "@modelcontextprotocol/server-postgres", "<connection-string>"]    }  }}
```





Replace `<connection-string>` with your connection string.

4. Save the configuration file.

5. Open Cursor and navigate to **Settings/MCP**. You should see a green active status after the server is successfully connected.


#### Windsurf [\#](https://supabase.com/docs/guides/getting-started/mcp\#windsurf)

1. Open Windsurf and navigate to the Cascade assistant.

2. Tap on the hammer (MCP) icon, then **Configure** to open the configuration file.

3. Add the following configuration:



macOSWindowsWindows (WSL)Linux







```flex


1
2
3
4
5
6
7
8
{  "mcpServers": {    "supabase": {      "command": "npx",      "args": ["-y", "@modelcontextprotocol/server-postgres", "<connection-string>"]    }  }}
```





Replace `<connection-string>` with your connection string.

4. Save the configuration file and reload by tapping **Refresh** in the Cascade assistant.

5. You should see a green active status after the server is successfully connected.


#### Cline [\#](https://supabase.com/docs/guides/getting-started/mcp\#cline)

1. Open the Cline extension in VS Code and tap the **MCP Servers** icon.

2. Tap **Configure MCP Servers** to open the configuration file.

3. Add the following configuration:



macOSWindowsWindows (WSL)Linux







```flex


1
2
3
4
5
6
7
8
{  "mcpServers": {    "supabase": {      "command": "npx",      "args": ["-y", "@modelcontextprotocol/server-postgres", "<connection-string>"]    }  }}
```





Replace `<connection-string>` with your connection string.

4. Save the configuration file. Cline should automatically reload the configuration.

5. You should see a green active status after the server is successfully connected.


#### Claude desktop [\#](https://supabase.com/docs/guides/getting-started/mcp\#claude-desktop)

1. Open Claude desktop and navigate to **Settings**.

2. Under the **Developer** tab, tap **Edit Config** to open the configuration file.

3. Add the following configuration:



macOSWindowsWindows (WSL)Linux







```flex


1
2
3
4
5
6
7
8
{  "mcpServers": {    "supabase": {      "command": "npx",      "args": ["-y", "@modelcontextprotocol/server-postgres", "<connection-string>"]    }  }}
```





Replace `<connection-string>` with your connection string.

4. Save the configuration file and restart Claude desktop.

5. From the new chat screen, you should see a hammer (MCP) icon appear with the new MCP server available.


#### Claude code [\#](https://supabase.com/docs/guides/getting-started/mcp\#claude-code)

1. Create a `.mcp.json` file in your project root if it doesn't exist.

2. Add the following configuration:



macOSWindowsWindows (WSL)Linux







```flex


1
2
3
4
5
6
7
8
{  "mcpServers": {    "supabase": {      "command": "npx",      "args": ["-y", "@modelcontextprotocol/server-postgres", "<connection-string>"]    }  }}
```





Replace `<connection-string>` with your connection string.

3. Save the configuration file.

4. Restart Claude code to apply the new configuration.


## Next steps [\#](https://supabase.com/docs/guides/getting-started/mcp\#next-steps)

Your AI tool is now connected to Supabase using MCP. Try asking the AI tool to query your database using natural language commands.

### Is this helpful?

NoYes

### On this page

[Connect to Supabase using MCP](https://supabase.com/docs/guides/getting-started/mcp#connect-to-supabase-using-mcp) [Step 1: Find your database connection string](https://supabase.com/docs/guides/getting-started/mcp#step-1-find-your-database-connection-string) [Step 2: Configure in your AI tool](https://supabase.com/docs/guides/getting-started/mcp#step-2-configure-in-your-ai-tool) [Next steps](https://supabase.com/docs/guides/getting-started/mcp#next-steps)

1. We use first-party cookies to improve our services. [Learn more](https://supabase.com/privacy#8-cookies-and-similar-technologies-used-on-our-european-services)



   [Learn more](https://supabase.com/privacy#8-cookies-and-similar-technologies-used-on-our-european-services)•Privacy settings





   AcceptOpt outPrivacy settings