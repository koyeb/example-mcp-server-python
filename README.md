# MCP Server for OpenAI Apps SDK

A Model Context Protocol (MCP) server built with FastMCP, designed to be deployed on Koyeb and integrated with the OpenAI Apps SDK.

## Overview

This MCP server demonstrates how to create AI-accessible tools and prompts that can be used by OpenAI's GPT models through the Apps SDK. The server runs as an HTTP service and exposes MCP capabilities via a streamable HTTP transport.

## Features

### Tools
- **count_letter**: Counts occurrences of a specific letter in a given text string (case-insensitive)

### Prompts
- **greet_user**: Generates prompt templates for creating greetings in different styles (friendly, formal, casual)

## Prerequisites

- Python 3.12+
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
   pip install -r requirements.txt
   ```

3. **Run the server**
   ```bash
   python main.py
   ```

   The server will start on `http://0.0.0.0:8080` by default.

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

- `PORT`: The port the server listens on (default: 8080)

## Integration with OpenAI Apps SDK

Once deployed on Koyeb, you'll receive a public URL. To use this MCP server with the OpenAI Apps SDK:

1. **Get your Koyeb deployment URL** (e.g., `https://your-app.koyeb.app`)

2. **Important**: The MCP endpoint is at `/mcp`, so your full URL will be:
   ```
   https://your-app.koyeb.app/mcp
   ```

3. **Configure in OpenAI Apps SDK**:
   ```python
   # Example configuration
   mcp_server_url = "https://your-app.koyeb.app/mcp"
   ```

4. The OpenAI model will now be able to:
   - Call the `count_letter` tool to analyze text
   - Use the `greet_user` prompt template to generate appropriate greetings

## Project Structure

```
.
├── main.py           # FastMCP server implementation
├── Dockerfile        # Container configuration
├── requirements.txt  # Python dependencies
└── README.md        # This file
```

## How It Works

1. **FastMCP** creates an MCP server with tools and prompts
2. **Streamable HTTP Transport** exposes the MCP protocol over HTTP at the `/mcp` endpoint
3. **Uvicorn** serves the ASGI application
4. **OpenAI Apps SDK** connects to the server and makes tools/prompts available to GPT models

## Adding New Tools

To add a new tool, use the `@mcp.tool()` decorator:

```python
@mcp.tool()
def your_tool_name(param1: str, param2: int) -> str:
    """Description of what your tool does"""
    # Your implementation here
    return result
```

## Adding New Prompts

To add a new prompt template, use the `@mcp.prompt()` decorator:

```python
@mcp.prompt()
def your_prompt_name(param: str) -> str:
    """Description of the prompt"""
    return f"Instructions for the AI based on {param}"
```

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

## Resources

- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Koyeb Documentation](https://www.koyeb.com/docs)
- [OpenAI Apps SDK](https://platform.openai.com/docs)

## License

MIT
