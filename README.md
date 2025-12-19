# Sales Analytics & Profit Dashboard
*Project Overview

This is a multi-user Django web application designed for store owners to analyze their sales data easily.
Store owners can register, login, upload sales data (CSV/Excel) and view sales, profit, and performance insights through a clean dashboard with graphs.
The system helps store owners make data-driven business decisions without manually analyzing Excel files.

*Technologies Used

-Backend: Django (Python)
-Frontend: HTML, CSS, Bootstrap
-Data Analysis: Pandas, NumPy
-Visualization: Matplotlib / Plotly
-Database: SQLite
-File Handling: CSV, Excel (.xlsx)

*Expected Data Format (CSV / Excel)
order_date,product_name,category,cost_price,selling_price,quantity,payment_mode.

*Project Structure
ecommerce/
│── accounts/        # Authentication (login, register)
│── upload_data/     # CSV / Excel upload
│── analysis/        # Data processing using Pandas
│── dashboard/       # Charts & reports
│── ecommerce/       # Project settings
│── manage.py
│── db.sqlite3

*How to Run the Project

1.Create & Activate Virtual Environment
python -m venv venv
venv\Scripts\activate   # Windows

2.Install Dependencies
pip install django ,pandas, numpy, matplotlib ,openpyxl.

3.Apply Migrations
python manage.py makemigrations
python manage.py migrate

4.Run the Server
python manage.py runserver

5.Open in Browser
http://127.0.0.1:8000/

*How the System Works

1.User registers and logs in
2.User uploads sales data (CSV/Excel)
3.System processes data using Pandas
4.Dashboard displays sales, profit, and insights using graphs
5.Each user sees only their own store data
