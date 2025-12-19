# Sales Analytics & Profit Dashboard
Project Overview

This is a multi-user Django web application designed for store owners to analyze their sales data easily.
Store owners can register, login, upload sales data (CSV/Excel) and view sales, profit, and performance insights through a clean dashboard with graphs.
The system helps store owners make data-driven business decisions without manually analyzing Excel files.

Technologies Used

-Backend: Django (Python)

-Frontend: HTML, CSS, Bootstrap

-Data Analysis: Pandas, NumPy

-Visualization: Matplotlib / Plotly

-Database: SQLite

-File Handling: CSV, Excel (.xlsx)


How to Run the Project

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

How the System Works

1.User registers and logs in

2.User uploads sales data (CSV/Excel)

3.System processes data using Pandas

4.Dashboard displays sales, profit, and insights using graphs

5.Each user sees only their own store data

<img width="1920" height="1080" alt="Screenshot (219)" src="https://github.com/user-attachments/assets/df630436-f38b-4b7a-825a-be2a819f9b8a" />
<img width="1920" height="1080" alt="Screenshot (215)" src="https://github.com/user-attachments/assets/a1310ea4-334e-4a46-aac3-7aaaa2c82769" />
<img width="1920" height="1080" alt="Screenshot (216)" src="https://github.com/user-attachments/assets/e0c45fc7-f748-4653-93fa-acd3a6ba1c44" />
<img width="1920" height="1080" alt="Screenshot (216)" src="https://github.com/user-attachments/assets/1a971d80-2e7e-4d58-9ea9-0c8a86560c50" />
<img width="1920" height="1080" alt="Screenshot (221)" src="https://github.com/user-attachments/assets/4b2d67cb-4ce8-4b95-b644-8c24aef6d085" />
