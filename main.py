from mcp.server.fastmcp import FastMCP
import os
import uvicorn

# Initialize FastMCP with JSON response enabled
mcp = FastMCP("Koyeb OpenAI Apps SDK Demo", json_response=True)

# Read the HTML widget file
with open("public/todo-widget.html", "r") as f:
    todo_html = f.read()

# Register the UI widget as a resource
@mcp.resource("ui://widget/todo.html")
def get_todo_widget() -> str:
    return todo_html

# Define a tool to add a todo
@mcp.tool()
def add_todo(title: str) -> str:
    """Creates a todo item with the given title.
    
    Args:
        title: The title of the todo item
    """
    if not title or not title.strip():
        return "Error: Missing title."
    
    return f'Added "{title.strip()}".'

# Define a tool to complete a todo  
@mcp.tool()
def complete_todo(todo_id: str) -> str:
    """Marks a todo as done by id.
    
    Args:
        todo_id: The ID of the todo to complete
    """
    if not todo_id:
        return "Error: Missing todo id."
    
    return f'Completed todo {todo_id}.'

# Create the FastMCP app
app = mcp.streamable_http_app()

port = int(os.environ.get("PORT", 8080))
print(f"Listening on port {port}")

uvicorn.run(app, host="0.0.0.0", port=port)
