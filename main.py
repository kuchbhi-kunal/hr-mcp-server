from mcp.server.fastmcp import FastMCP
from typing import List

employee_leaves = {
    "Kunal": {"balance": 18, "history": ["2024-12-25", "2025-01-01"]},
    "Rohit": {"balance": 20, "history": []}
}

mcp = FastMCP("Shelton")

@mcp.tool()
def get_leave_balance(employee_name: str) -> str:
    """Check how many leave days are left for the employee by name"""
    data = employee_leaves.get(employee_name)
    if data:
        return f"{employee_name} has {data['balance']} leave days remaining."
    return "Employee not found."

@mcp.tool()
def apply_leave(employee_name: str, leave_dates: List[str]) -> str:
    """
    Apply leave for specific dates (e.g., ["2025-04-17", "2025-05-01"])
    """
    if employee_name not in employee_leaves:
        return "Employee not found."

    requested_days = len(leave_dates)
    available_balance = employee_leaves[employee_name]["balance"]

    if available_balance < requested_days:
        return f"Insufficient leave balance. You requested {requested_days} day(s) but have only {available_balance}."

    employee_leaves[employee_name]["balance"] -= requested_days
    employee_leaves[employee_name]["history"].extend(leave_dates)

    return f"Leave applied for {requested_days} day(s). Remaining balance: {employee_leaves[employee_name]['balance']}."

@mcp.tool()
def get_leave_history(employee_name: str) -> str:
    """Get leave history for the employee"""
    data = employee_leaves.get(employee_name)
    if data:
        history = ', '.join(data['history']) if data['history'] else "No leaves taken."
        return f"Leave history for {employee_name}: {history}"
    return "Employee not found."

@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}! How can I assist you with leave management today?"

@mcp.tool()
def wish_happy_diwali() -> str:
    rangoli = """
        * * * * *
      *           *
    *    @     @    *
  *   @   #   #   @   *
* @   #   0   0   #   @ *
  *   @   #   #   @   *
    *    @     @    *
      *           *
        * * * * *

    """
    return rangoli

@mcp.tool()
def what_is_your_name() -> str:
    """Return the name of this assistant"""
    return "My name is Shelton."

@mcp.tool()
def are_you_hr() -> str:
    """Respond to role inquiry"""
    return "No, I am not an HR. I am the Chief of Staff."

if __name__ == "__main__":
    mcp.run()
