from mcp.server.fastmcp import FastMCP
import os
import uvicorn

# Initialize FastMCP with JSON response enabled
mcp = FastMCP("Koyeb OpenAI Apps SDK Demo", json_response=True)

# Define a tool that generates a greeting message
@mcp.tool()
def greet_user(name: str, style="friendly") -> str:
    styles = {
        "friendly": f"Hello, {name}! It's wonderful to meet you!",
        "formal": f"Good day, {name}. It is a pleasure to make your acquaintance.",
        "casual": f"Hey {name}! What's up?",
    }
    return styles.get(style, styles['friendly'])

# Define a tool that counts occurrences of a letter in a given text
@mcp.tool()
def count_letter(text: str, letter: str) -> int:
    return text.lower().count(letter.lower())

# Create the FastMCP app
app = mcp.streamable_http_app()

port = int(os.environ.get("PORT", 8080))
print(f"Listening on port {port}")

uvicorn.run(app, host="0.0.0.0", port=port)
