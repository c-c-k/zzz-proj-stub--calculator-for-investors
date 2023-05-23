from string import Template

ERROR_NOT_IMPLEMENTED = "Not implemented!"
ERROR_INVALID_OPTION = "Invalid option!"
ERROR_COMPANY_NOT_FOUND = "Company not found!"
INFO_WELCOME = "Welcome to the Investor Program!"
INFO_GOODBYE = "Have a nice day!"
INFO_ENTER_OPTION = "Enter an option:"
INFO_DB_CREATED = "Database created successfully!"
INFO_COMPANY_READ_HEADER = Template("${ticker} ${name}")
INFO_COMPANY_READ_STATISTIC = Template("${stat_name} = ${stat_value}")
INFO_COMPANY_CREATED = "Company created successfully!"
INFO_COMPANY_UPDATED = "Company updated successfully!"
INFO_COMPANY_DELETED = "Company deleted successfully!"
INFO_COMPANY_LIST = "COMPANY LIST"
INFO_COMPANY_LIST_ENTRY = Template("${ticker} ${name} ${sector}")
MENU_MAIN = """
MAIN MENU
0 Exit
1 CRUD operations
2 Show top ten companies by criteria"""
MENU_CRUD = """
CRUD MENU
0 Back
1 Create a company
2 Read a company
3 Update a company
4 Delete a company
5 List all companies"""
MENU_TOP_TEN = """
TOP TEN MENU
0 Back
1 List by ND/EBITDA
2 List by ROE
3 List by ROA"""
PROMPT_ENTER_DATA = Template("Enter ${label} (in the format '${example}'):")
PROMPT_ENTER_COMPANY_NAME = "Enter company name:"
PROMPT_ENTER_COMPANY_NUMBER = "Enter company number:"
