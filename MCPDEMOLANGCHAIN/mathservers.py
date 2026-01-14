from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math")

@mcp.tool()
def add(x: int, y: int) -> int:
    """__Summary__
    Add two numbers"""
    
    return x + y

@mcp.tool()
def subtract(x: int, y: int) -> int:
    """
    __Summary__
    Subtract two numbers
    """
    return x - y

@mcp.tool()
def multiply(x: int, y: int) -> int:
    """
    __Summary__
    Multiply two numbers
    """
    return x * y

@mcp.tool()
def divide(x: int, y: int) -> int:
    """
    __Summary__
    Divide two numbers
    """
    return x / y

if __name__ == "__main__":
    mcp.run(transport="stdio")