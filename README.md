# MCP Server for OpenAI Apps SDK

A Model Context Protocol (MCP) server built with the official MCP SDK, designed to be deployed on Koyeb and integrated with the OpenAI Apps SDK.

## Overview

This MCP server demonstrates how to create AI-accessible tools and widgets that can be used by OpenAI's GPT models through the Apps SDK. The server runs as an HTTP service and exposes MCP capabilities via a streamable HTTP transport.

## Features

### Resources
- **UI Widget**: An HTML interface that displays the todo list in ChatGPT (`ui://widget/todo.html`)

### Tools
- **add_todo**: Creates a new todo item with the given title
- **complete_todo**: Marks a todo item as completed by its ID

## Prerequisites

- Node.js 20+
- Docker (for containerized deployment)
- A [Koyeb](https://www.koyeb.com/) account
- OpenAI Apps SDK access

## Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd example-mcp-server
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Run the server**
   ```bash
   node server.js
   ```

   The server will start on `http://0.0.0.0:8787` by default (or port 8080 in production).

## Deployment on Koyeb

### Option 1: Deploy from GitHub

1. Push your code to a GitHub repository
2. Go to [Koyeb Dashboard](https://app.koyeb.com/)
3. Click "Create Service"
4. Select "GitHub" as the deployment method
5. Choose your repository
6. Koyeb will automatically detect the Dockerfile and deploy

### Option 2: Deploy with Docker

```bash
# Build the Docker image
docker build -t mcp-server .

# Run locally to test
docker run -p 8080:8080 -e PORT=8080 mcp-server
```

### Environment Variables

- `PORT`: The port the server listens on (default: 8787 locally, 8080 in production)

## Integration with OpenAI Apps SDK

Once deployed on Koyeb, you'll receive a public URL. To use this MCP server with the OpenAI Apps SDK:

1. **Get your Koyeb deployment URL** (e.g., `https://your-app.koyeb.app`)

2. **Important**: The MCP endpoint is at `/mcp`, so your full URL will be:
   ```
   https://your-app.koyeb.app/mcp
   ```

3. **Configure in OpenAI Apps SDK**:
   - Add the server URL to your ChatGPT settings
   - The server will appear as "todo-app" in the MCP servers list

4. The OpenAI model will now be able to:
   - Add todos to your list
   - Mark todos as completed
   - Display an interactive widget showing all todos

## Project Structure

```
.
├── server.js            # MCP server implementation with Node.js
├── public/
│   └── todo-widget.html # Web component for ChatGPT UI
├── Dockerfile           # Container configuration for Node.js
├── package.json         # Node.js dependencies
└── README.md           # This file
```

## How It Works

1. **MCP SDK** creates an MCP server with tools and a UI resource
2. **UI Widget** (HTML file) gets served as a resource and rendered in ChatGPT's iframe
3. **StreamableHTTPServerTransport** exposes the MCP protocol over HTTP at the `/mcp` endpoint
4. **Node.js HTTP Server** serves the application
5. **OpenAI Apps SDK** connects to the server, displays the UI, and makes tools available to GPT models
6. When a tool is called, the result is passed to the widget via `window.openai.toolOutput`

## Adding New Tools

To add a new tool, use `server.registerTool()`:

```javascript
server.registerTool(
  "tool_name",
  {
    title: "Tool Title",
    description: "Description of what your tool does",
    inputSchema: {
      param: z.string().min(1),
    },
    _meta: {
      "openai/outputTemplate": "ui://widget/your-widget.html",
      "openai/toolInvocation/invoking": "Running tool",
      "openai/toolInvocation/invoked": "Tool completed",
    },
  },
  async (args) => {
    // Your implementation here
    return {
      content: [{ type: "text", text: "Result message" }],
      structuredContent: { /* data for widget */ },
    };
  }
);
```

## Updating the UI Widget

Edit `public/todo-widget.html` to customize how tool results are displayed in ChatGPT. The widget receives tool output via `window.openai.toolOutput` and can listen for updates using the `openai:set_globals` event.

## Troubleshooting

### Health Checks Failing
- Ensure the server binds to `0.0.0.0` (not `127.0.0.1`)
- Verify the `PORT` environment variable is set correctly

### 404 Errors
- Make sure you're connecting to `/mcp` endpoint, not just the root URL
- Example: `https://your-app.koyeb.app/mcp` (not `https://your-app.koyeb.app/`)

### Connection Refused
- Check that Koyeb deployment is healthy
- Verify the service is listening on the correct port

### Widget Not Updating
- Check browser console for errors
- Verify that `structuredContent` is being returned from tool handlers
- Ensure the widget is reading from `window.openai.toolOutput`

## Resources

- [Model Context Protocol SDK](https://github.com/modelcontextprotocol/sdk)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Koyeb Documentation](https://www.koyeb.com/docs)
- [OpenAI Apps SDK](https://platform.openai.com/docs)

## License

MIT
