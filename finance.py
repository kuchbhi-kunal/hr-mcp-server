from mcp.server.fastmcp import FastMCP
from typing import Dict, Any, List

# ----------------------------------------------------------------------
# Finance Data Store
# ----------------------------------------------------------------------

finance_data: Dict[str, Dict[str, Any]] = {
    "Engineering": {
        "monthly_budget": 200000,
        "expenses": [
            {"employee": "Kunal", "amount": 5000, "category": "Equipment", "approved": True},
            {"employee": "Rohit", "amount": 2000, "category": "Snacks", "approved": False}
        ]
    },
    "Sales": {
        "monthly_budget": 150000,
        "expenses": [
            {"employee": "Anya", "amount": 8000, "category": "Travel", "approved": True}
        ]
    },
    "Marketing": {
        "monthly_budget": 100000,
        "expenses": []
    }
}

mcp = FastMCP("SheltonFinance")

@mcp.tool()
def log_expense(employee_name: str, department: str, amount: int, category: str) -> str:
    """
    Log a new expense under a department.
    """
    if department not in finance_data:
        return f"Department '{department}' not found."

    expense_entry = {"employee": employee_name, "amount": amount, "category": category, "approved": False}
    finance_data[department]["expenses"].append(expense_entry)

    return f"Expense logged: ₹{amount} by {employee_name} under {category} in {department}. Awaiting approval."

@mcp.tool()
def approve_expense(department: str, employee_name: str, amount: int) -> str:
    """
    Approve a specific expense for an employee.
    """
    if department not in finance_data:
        return "Department not found."

    for expense in finance_data[department]["expenses"]:
        if expense["employee"] == employee_name and expense["amount"] == amount:
            expense["approved"] = True
            return f"Approved expense of ₹{amount} for {employee_name} in {department}."

    return "Expense not found."

@mcp.tool()
def get_department_budget(department: str) -> str:
    """
    Get the current budget and total expenses for a department.
    """
    data = finance_data.get(department)
    if not data:
        return "Department not found."

    total_expenses = sum(exp["amount"] for exp in data["expenses"])
    remaining = data["monthly_budget"] - total_expenses

    return (
        f"💰 Department: {department}\n"
        f"Budget: ₹{data['monthly_budget']}\n"
        f"Total Expenses: ₹{total_expenses}\n"
        f"Remaining: ₹{remaining}"
    )

@mcp.tool()
def get_unapproved_expenses() -> str:
    """
    List all expenses pending approval across departments.
    """
    pending = []
    for dept, data in finance_data.items():
        for exp in data["expenses"]:
            if not exp["approved"]:
                pending.append(f"{exp['employee']} - ₹{exp['amount']} ({exp['category']}) in {dept}")

    if not pending:
        return "No unapproved expenses pending."
    return "Pending Approvals:\n" + "\n".join(pending)

@mcp.tool()
def generate_financial_summary() -> str:
    """
    Generate a high-level monthly summary across all departments.
    """
    summary_lines = []
    for dept, data in finance_data.items():
        total_expenses = sum(exp["amount"] for exp in data["expenses"])
        remaining = data["monthly_budget"] - total_expenses
        summary_lines.append(f"{dept}: Spent ₹{total_expenses}, Remaining ₹{remaining}")

    summary = "\n".join(summary_lines)
    return f"📊 Monthly Finance Summary:\n{summary}"

@mcp.tool()
def get_employee_expenses(employee_name: str) -> str:
    """
    Retrieve all expenses logged by an employee across departments.
    """
    records = []
    for dept, data in finance_data.items():
        for exp in data["expenses"]:
            if exp["employee"] == employee_name:
                status = "Approved ✅" if exp["approved"] else "Pending ⏳"
                records.append(f"{dept}: ₹{exp['amount']} ({exp['category']}) - {status}")

    if not records:
        return f"No expenses found for {employee_name}."
    return f"Expenses for {employee_name}:\n" + "\n".join(records)


@mcp.tool()
def what_is_your_name() -> str:
    """Return assistant's name"""
    return "My name is SheltonFinance."

@mcp.tool()
def who_are_you() -> str:
    """Describe role"""
    return "I’m the Finance Assistant — I track budgets, expenses, and approvals."

@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Personalized greeting"""
    return f"Hello {name}! Ready to manage some expenses or check your department budget?"

@mcp.tool()
def wish_happy_new_fiscal_year() -> str:
    """Celebrate the start of a new fiscal year."""
    art = """
    💸🎉 Happy New Fiscal Year! 🎉💸
    ------------------------------
    Here's to balanced books,
    growing revenue, and smart spending!
    🧾📈✨
    """
    return art


if __name__ == "__main__":
    mcp.run()
