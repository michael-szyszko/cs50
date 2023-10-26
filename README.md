# Debt Calculator
#### Video Demo:  https://www.youtube.com/watch?v=5Z7m-qq6jb4


#### Description:

Debt Calculator is a debt payoff projection tool.

Users may input their debts represented by a debt amount (i.e., principal) with an annual percentage rate (APR) and a minimum payment that the issuer requires. The tool will provide a table that displays every debt and the remaining balance for every month.

Users can create a profile with a username and password. Users may then input debts into a form that will be used for debt payoff projections. Debts that the user inputs are persisted such that they may logout and log back in at a different time and view their originally input debt data. Users may toggle “Snow Ball”, and “Avalanche”, the two most popular methods for prioritizing debts, to view the length of expected time to payoff debt depending on which method is chosen.

To run the application from the CLI:
1) `flask run` from the project folder.
This will start the application which hosts a webserver and creates a database if it does not already exist.

Optional:

2) `npx tailwindcss -i ./static/styles.css -o ./static/output.css --watch` from the project folder.
This will execute package commands fromTailwind that generate the css. I.e., this is needed when making changes to styles or creating the output.css which styles the html pages.

#### Assumptions and limitations:

The Debt Calculator makes several assumptions and has several limitations that could be addressed in future implementations:
1) Interest is compounded monthly and calculated by: principal + (principal * (rate / 100.0) / 12). While debt calculations vary depending on the type of debt instrument,this is considered adequate for most debts and understanding in what month a debt can be expected to be paid off.
2) The debt does not take longer than 50 years to pay off. The debt calculator will generate a table of up to 50 years and display the remaining balances in the table. Generally debts are structured to be paid off in less than 50 years, even when making only minimum payments. While it is possible for debts to grow or not be paid off within 50 years even when making minimum payments, this calculator does not fully support such scenarios.
3) Penalties or other fees (e.g., late penalty) and additional one time payments made (e.g., making one extra payment in a particular month). The design of the system does make it extendable for such scenarios as the database stores start dates for debts. These additions would functionally upgrade this from a debt payoff projection tool that estimates when debt is expected to be paid off, to more debt payoff planning tool, that could track progress and update debts based on actual events.
4) Guest Users are not allowed. Currently the system requires a user to be authenticated to input debts and view debt payoff projection details. Future implementations could allow a guest mode that does not persist debt information of a user.
5) Debts cannot be modified. Update functionality was not implemented, but debts may be deleted and recreated. While the effort for update functionality is not great, there is some design complexity involved to integrate with the potential future functionality of upgrading the system to track progress of debt payoffs through one time payments or penalties.


#### Files:
app.py
This file contains the web server logic to server html pages to users and manage authentication and authorization. With the exception of the register page, all pages require an authenticated user with a valid session.

debt_calculator.db
SQL database created with SQLAlchemy that stores user information and debt information.

debt_calculator.py
This file contains all the logic to calculate and project debt payoffs using different methods of debt prioritizing (i.e., “snowball” and “avalanche”).

debt_db.py
This file contains the logic to create database tables if they do not exist and provides functions to debt_calculator.py and app.py to interact with the debt_calculator.db.

helpers.py
This file contains some functions to

Static folder, tailwind.config.js, package.json
These files and folders contain the logic and assets for html files and styling. Tailwind is a CSS framework that supports responsive design, which is why it was used.
