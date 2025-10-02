from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Any

# Modified employee_leaves to include more HR-relevant fields
employee_leaves: Dict[str, Dict[str, Any]] = {
    "Kunal": {
        "balance": 18,
        "history": ["2024-12-25", "2025-01-01"],
        "department": "Engineering",
        "manager": "Anya",
        "sick_leave_policy": "3-day max without doctor's note"
    },
    "Rohit": {
        "balance": 20,
        "history": [],
        "department": "Sales",
        "manager": "Brian",
        "sick_leave_policy": "2-day max without doctor's note"
    }
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

# ----------------------------------------------------------------------
## New HR Functions
# ----------------------------------------------------------------------

@mcp.tool()
def get_all_employees() -> str:
    """Return a list of all employees managed by the system."""
    names = list(employee_leaves.keys())
    return "The current employees are: " + ", ".join(names)

@mcp.tool()
def check_employee_data(employee_name: str) -> str:
    """
    Retrieve key departmental and managerial data for an employee.
    """
    data = employee_leaves.get(employee_name)
    if data:
        department = data.get("department", "N/A")
        manager = data.get("manager", "N/A")
        return f"{employee_name} is in the {department} department and reports to {manager}."
    return "Employee not found."

@mcp.tool()
def process_sick_leave_with_policy(employee_name: str, num_days: int) -> str:
    """
    Apply sick leave and return the employee's specific sick leave policy.
    This function simulates a policy check during sick leave application.
    """
    data = employee_leaves.get(employee_name)
    if not data:
        return "Employee not found."

    policy = data.get("sick_leave_policy", "No specific policy on file.")

    # A more sophisticated application would involve date tracking, but for this example:
    if data['balance'] < num_days:
        return f"Insufficient leave balance for sick leave. Requested {num_days} day(s) but only have {data['balance']}. Policy: {policy}"

    data['balance'] -= num_days
    # Note: Sick leave dates would typically be added to history, but we skip that here for brevity.

    return f"Sick leave applied for {num_days} day(s). New balance: {data['balance']}. **Sick Leave Policy:** {policy}"

# ----------------------------------------------------------------------

@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}! How can I assist you with leave management today?"

@mcp.tool()
def wish_happy_diwali() -> str:
    """Wish Happy Diwali with a simple rangoli ASCII art."""
    rangoli = """
        * * * * *
      * *
    * @     @    *
  * @   #   #   @   *
* @   #   0   0   #   @ *
  * @   #   #   @   *
    * @     @    *
      * *
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