# Library Data Visualizer 

For City of Glendale, CA, Department of Libraries. 
Accesses the library database with Sierra REST API and generates a data report for each library branch in the city


-----

• MAKE SURE THE "Data Report" folder stays on the Desktop, and DO NOT move any files out of it

• Must be installed to run this program: 
Python(version 2 or higher), Plotly, Jinja2, Psycopg2

• Right-click run.ps1 and run with powershell

• Enter the query dates in the python file for the first prompt (verbatim), and enter in the replacement, which should be exactly
 ***ONE MONTH PRIOR TO THE DAY OF DATA REPORT RELEASE***

• Will replace the query date, run the python file, generate an HTML file as the data report, and open it in browser

• the HTML file will get saved to the Data Report folder, titled with the current date
(NOTE: if you run it twice in a day, the first file will get overriden)

----------------------------------------------------------------------------------------------------------------------------------
• NOTE: if the script is not running because of execution policy
	Open Powershell as an administrator and enter the following command:
	Set-ExecutionPolicy RemoteSigned

• Function: the Powershell script refreshes the dates in the Python file's SQL queries and executes the python file