from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Demo", json_response=True)

@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b

@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    return f"Hello, {name}!"

@mcp.prompt()
def greet_user(name: str, style="friendly") -> str:
    styles = {
        "friendly": "Please write a warm, friendly greeting",
        "formal": "Please write a formal, professional greeting",
        "casual": "Please write a casual, relaxed greeting",
    }
    return f"{styles.get(style, styles['friendly'])} for someone named {name}."

if __name__ == "__main__":
    import os
    import sys
    
    # Set host and port as command-line arguments that uvicorn will use
    host = os.environ.get("HOST", "0.0.0.0")
    port = os.environ.get("PORT", "8080")
    
    # Patch sys.argv to pass host and port to uvicorn
    sys.argv.extend(["--host", host, "--port", port])
    
    mcp.run(transport="streamable-http")
