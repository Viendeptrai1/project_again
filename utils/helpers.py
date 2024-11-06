def handle_error(error_message):
    """Handle and log errors"""
    print(f"Error: {error_message}")
    # Add logging functionality here
    
def format_currency(value):
    """Format currency values"""
    return f"${value:,.2f}"
    
def calculate_percentage(value, total):
    """Calculate percentage"""
    return (value / total * 100) if total != 0 else 0
