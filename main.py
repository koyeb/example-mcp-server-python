from mcp.server.fastmcp import FastMCP
import os
import uvicorn

# Initialize FastMCP with JSON response enabled
mcp = FastMCP("Koyeb OpenAI Apps SDK Demo", json_response=True)

# Read the HTML widget file
with open("public/todo-widget.html", "r") as f:
    todo_html = f.read()

# In-memory todo storage
todos = []
next_id = 1

# Register the UI widget as a resource
@mcp.resource("ui://widget/todo.html")
def get_todo_widget() -> str:
    return todo_html

def reply_with_todos(message: str = "") -> dict:
    """Helper function to return todos in the format OpenAI expects"""
    content = [{"type": "text", "text": message}] if message else []
    return {
        "content": content,
        "structuredContent": {"tasks": todos}
    }

# Define a tool to add a todo
@mcp.tool()
def add_todo(title: str) -> dict:
    """Creates a todo item with the given title.
    
    Args:
        title: The title of the todo item
    """
    global next_id
    
    title = title.strip()
    if not title:
        return reply_with_todos("Missing title.")
    
    todo = {"id": f"todo-{next_id}", "title": title, "completed": False}
    next_id += 1
    todos.append(todo)
    
    return reply_with_todos(f'Added "{todo["title"]}".')

# Define a tool to complete a todo
@mcp.tool()
def complete_todo(id: str) -> dict:
    """Marks a todo as done by id.
    
    Args:
        id: The ID of the todo to complete
    """
    if not id:
        return reply_with_todos("Missing todo id.")
    
    todo = next((task for task in todos if task["id"] == id), None)
    if not todo:
        return reply_with_todos(f"Todo {id} was not found.")
    
    for task in todos:
        if task["id"] == id:
            task["completed"] = True
    
    return reply_with_todos(f'Completed "{todo["title"]}".')

# Create the FastMCP app
app = mcp.streamable_http_app()

port = int(os.environ.get("PORT", 8080))
print(f"Listening on port {port}")

uvicorn.run(app, host="0.0.0.0", port=port)
