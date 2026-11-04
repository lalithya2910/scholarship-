🎓 Scholarship Eligibility and Fund Allocation Platform
1. Project Overview

The Scholarship Eligibility and Fund Allocation Platform is a web-based application designed to simplify and automate the scholarship application, eligibility verification, application review, and fund allocation process.

The main objective of this project is to provide a centralized platform where students can explore available scholarships, submit applications, upload supporting documents, and track their application status. Administrators can manage scholarships, define eligibility requirements, verify submitted documents, review applications, approve or reject applications, and allocate scholarship funds.

Traditional scholarship management often involves manual paperwork, time-consuming verification, difficulty tracking applications, and challenges in managing scholarship budgets. This platform addresses these problems through a digital application management system.

The application consists of two major modules:

Student Module: Allows students to register, log in, view scholarships, provide academic and financial details, submit applications, upload documents, and track application progress.
Admin Module: Allows administrators to manage scholarships, view student information, verify documents, review applications, make decisions, and allocate scholarship funds.

The system uses Python Flask for backend development and MySQL for database management.

2. Project Objectives
To digitize the scholarship application process.
To provide a centralized scholarship management platform.
To simplify student registration and scholarship applications.
To maintain student academic and financial information.
To enable secure document submission and verification.
To provide transparent application status tracking.
To help administrators manage scholarship opportunities.
To monitor available scholarship funds and allocations.
To reduce manual administrative work and paperwork.
3. Features and Functionalities
3.1 Student Module
S.No	Feature	Description
1	Student Registration	Allows new students to create accounts.
2	Student Login	Authenticates registered students.
3	Password Security	Uses Werkzeug password hashing.
4	Forgot Password	Allows students to recover forgotten passwords.
5	OTP Verification	Verifies students through email OTP.
6	OTP Expiration	OTP expires after five minutes.
7	Password Reset	Allows students to update forgotten passwords.
8	Student Dashboard	Displays scholarship and application information.
9	View Scholarships	Displays available scholarship opportunities.
10	Scholarship Details	Displays scholarship descriptions and eligibility requirements.
11	Academic Details	Collects student academic information.
12	Financial Details	Collects student financial information.
13	Scholarship Application	Allows students to submit applications.
14	Duplicate Application Check	Prevents duplicate scholarship applications.
15	Document Upload	Allows students to upload supporting documents.
16	File Validation	Validates uploaded document formats and size.
17	Application Tracking	Allows students to monitor application progress.
18	Application Status	Displays application decisions and allocation status.
3.2 Admin Module
S.No	Feature	Description
1	Admin Login	Provides administrator authentication.
2	Admin Dashboard	Displays scholarship management information.
3	Student Management	Allows administrators to view student records.
4	Scholarship Management	Provides scholarship administration functionality.
5	Add Scholarship	Allows administrators to create scholarships.
6	Edit Scholarship	Allows administrators to update scholarship details.
7	Eligibility Configuration	Defines scholarship eligibility requirements.
8	Required Documents	Configures documents required for applications.
9	View Applications	Displays student scholarship applications.
10	Application Review	Allows administrators to examine applications.
11	Document Verification	Enables verification of uploaded documents.
12	Application Approval	Allows administrators to approve applications.
13	Application Rejection	Allows administrators to reject applications.
14	Committee Reviews	Stores committee review information and comments.
15	Fund Allocation	Allocates scholarship funds to approved applications.
16	Fund Availability Check	Checks the available scholarship balance.
17	Allocation Limit Check	Prevents allocation beyond configured limits.
18	Allocation Monitoring	Maintains scholarship fund allocation records.
3.3 Additional Features
Secure password storage using Werkzeug.
Email-based OTP verification.
Five-minute OTP expiration.
Duplicate application prevention.
Application-specific document storage.
File upload validation.
Scholarship eligibility configuration.
Committee-based application review.
Scholarship fund availability validation.
Centralized MySQL database management.
4. Technology Stack
Technology	Purpose
Python	Main backend programming language.
Flask	Web application framework for routing and backend logic.
MySQL	Relational database management system.
HTML5	Structure of web pages.
CSS3	Styling and user interface design.
Werkzeug	Password hashing and security utilities.
mysql-connector-python	Python-to-MySQL database connectivity.
Gmail SMTP	Sending OTP verification emails.
Python Secrets	Secure random OTP generation.
python-dotenv	Environment variable configuration, if used by the application.
Git and GitHub	Version control and project hosting.
5. System Requirements
Software Requirements
Python 3.9 or later.
MySQL Server 8.0 or compatible version.
MySQL Workbench (optional).
Git.
Visual Studio Code or another code editor.
Modern web browser.
Hardware Requirements
Minimum 4 GB RAM.
Dual-core processor or higher.
Sufficient disk space for application files and uploaded documents.
Internet connection for email-based OTP functionality.
6. Project Directory Structure

The project follows this general structure:

text
scholarship-/
│
├── app.py
│   └── Main Flask application
│
├── database.py
│   └── Database connectivity and operations
│
├── database.sql
│   └── Database schema and initial data
│
├── mail.py
│   └── Email and OTP functionality
│
├── requirements.txt
│   └── Python dependencies
│
├── templates/
│   ├── Student HTML templates
│   └── Admin HTML templates
│
├── static/
│   └── css/
│       └── Stylesheets
│
├── scholarship_documents/
│   └── Uploaded scholarship documents
│
├── .gitignore
│
└── README.md

7. Installation and Setup Instructions

Follow these steps to download, configure, and run the application locally.

Step 1: Clone the Repository

Open your terminal or command prompt and execute:

bash
git clone https://github.com/lalithya2910/scholarship-.git

Step 2: Navigate to the Project Directory
bash
cd scholarship-

Step 3: Create a Python Virtual Environment
bash
python -m venv venv


Activate the virtual environment.

Windows:

bash
venv\Scripts\activate


Linux/macOS:

bash
source venv/bin/activate

Step 4: Install Required Dependencies
bash
pip install -r requirements.txt

Step 5: Configure MySQL Database
Install and start MySQL Server.
Open MySQL Workbench or MySQL Command Line.
Create the database if it is not already created by the SQL script.
sql
CREATE DATABASE scholarship;

Import the database schema.

Using MySQL command line:

bash
mysql -u root -p scholarship < database.sql


Alternatively, execute the SQL statements in database.sql using MySQL Workbench.

Ensure that all tables are created successfully before starting the application.

Step 6: Configure Environment Variables

Create a .env file in the root directory.

Example configuration:

env
# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=scholarship

# Email Configuration
SMTP_EMAIL=your_email@gmail.com
SMTP_PASSWORD=your_gmail_app_password

# Flask Configuration
SECRET_KEY=generate_a_secure_random_secret


Important configuration notes:

Replace the database username and password with your actual MySQL credentials.
Use a Gmail App Password for SMTP authentication when required.
Generate a strong random Flask secret key.
Never upload your .env file to GitHub.
Ensure the environment variable names match those actually read by your application.
The current backend should be updated to read its Flask secret key from the environment rather than relying on a hardcoded value.
Step 7: Run the Application

Execute:

bash
python app.py


After successful startup, open your browser and navigate to:

text
http://127.0.0.1:5000/


The scholarship platform should now be accessible locally.

8. Environment Variables

The following table describes the recommended configuration variables.

Variable	Description	Example
DB_HOST	MySQL server hostname	localhost
DB_PORT	MySQL server port	3306
DB_USER	MySQL username	root
DB_PASSWORD	MySQL password	your_password
DB_NAME	Database name	scholarship
SMTP_EMAIL	Sender email address	your_email@gmail.com
SMTP_PASSWORD	Gmail App Password	your_app_password
SECRET_KEY	Flask session signing secret	Secure random value

Security recommendations:

Do not commit credentials to GitHub.
Add .env to .gitignore.
Do not expose student documents or personal information.
Use HTTPS and secure session-cookie settings in production.
Replace development settings before deployment.
9. Database Design and Notes

The application uses MySQL as its relational database.

The database stores student accounts, academic information, financial information, scholarship details, applications, supporting documents, committee reviews, and fund allocations.

Main Database Tables
S.No	Table Name	Description
1	students	Stores student account and personal information.
2	admins	Stores administrator account information.
3	academic_details	Stores academic information of students.
4	financial_details	Stores financial information of students.
5	scholarships	Stores scholarship details and eligibility requirements.
6	applications	Stores scholarship applications submitted by students.
7	documents	Stores uploaded document records.
8	scholarship_required_documents	Stores required document configurations for scholarships.
9	committee_reviews	Stores committee review records and comments.
10	fund_allocations	Stores scholarship fund allocation details.
Database Operations

The application uses database operations for:

Student registration and authentication.
Retrieving scholarship information.
Inserting academic and financial information.
Creating scholarship applications.
Checking duplicate applications.
Storing document metadata.
Managing administrator records.
Recording committee reviews.
Updating application decisions.
Recording scholarship fund allocations.
Checking available scholarship funds.

The database schema and initial data are maintained in database.sql.

10. Application Routes and API Notes

The project uses Flask server-rendered web routes to handle user interactions and application workflows.

It is not currently documented as a separate REST API service.

The following table provides an overview of the main application routes to check in the Flask implementation.

Route / Functionality	Purpose
/register	Student registration.
/login	Student login.
/dashboard	Student dashboard.
/scholarships	View available scholarships.
/scholarship_details/<id>	View scholarship details.
/apply_scholarship/<id>	Submit a scholarship application.
/application_status	Track application status.
/forgot_password	Start password recovery.
/verify_otp	Verify email OTP.
/reset_password	Reset account password.
/admin_login	Administrator login.
/admin_dashboard	Administrator dashboard.

Note: These are route references for documentation purposes. Verify the exact route names, HTTP methods, and parameters against app.py before treating this table as a complete API specification.

11. Document Upload and Storage

The application supports uploading supporting documents for scholarship applications.

Supported formats:

PDF
JPG
JPEG
PNG

Maximum file size:

10 MB per document.

Uploaded documents are maintained in application-specific folders inside the scholarship_documents/ directory.

Document information is associated with application records in the database.

12. Application Workflow

The complete scholarship management process follows these stages:

Student registers on the platform.
Student logs into their account.
Student explores available scholarships.
Student checks eligibility requirements.
Student provides academic and financial information.
Student uploads required supporting documents.
Student submits the scholarship application.
Administrator views the submitted application.
Administrator verifies the uploaded documents.
Committee reviews the application.
Administrator approves or rejects the application.
Approved applications proceed to scholarship fund allocation.
The system checks available funds and allocation limits.
Student tracks the application and allocation status.
13. Security and Validation

The application incorporates several security and validation mechanisms:

Password hashing through Werkzeug.
Session-based user authentication.
OTP-based email verification.
OTP expiration after five minutes.
Duplicate application checks.
File extension validation.
File size restrictions.
Scholarship fund availability checks.
Application-specific document organization.

Further production hardening should include environment-based secrets, CSRF protection, strict upload validation, authorization checks, and secure session configuration.

14. Team Member Contributions

This project was developed as a scholarship management application.

The following table should be updated with the actual team members and their responsibilities.

Team Member	Role	Contributions
Lalithya	Project Development	Flask backend development, database integration, student and admin workflows, and overall application implementation.
Member 2	Frontend Development	HTML templates, CSS styling, and user interface implementation.
Member 3	Database and Testing	Database design, SQL operations, application testing, and validation.

Note: If this is an individual project, retain only your name and actual contributions. Do not list members who did not participate.

15. Future Enhancements

The following improvements can be considered for future versions:

Automated eligibility assessment.
AI-based scholarship recommendations.
Automated document verification.
SMS and email application notifications.
Scholarship approval certificate generation.
Advanced analytics and reporting.
Online scholarship disbursement integration.
Detailed administrator activity logs.
Improved application security.
Cloud-based document storage.
16. Expected Project Outcomes

The Scholarship Eligibility and Fund Allocation Platform aims to provide:

A centralized scholarship application system.
Easier access to scholarship opportunities.
Efficient student information management.
Organized document submission and verification.
Transparent application tracking.
Simplified administrator workflows.
Better scholarship budget monitoring.
Reduced manual administrative effort.
17. GitHub Repository

Project Repository:

https://github.com/lalithya2910/scholarship-

The repository contains the project source code, database scripts, dependency information, and documentation.

18. Conclusion

The Scholarship Eligibility and Fund Allocation Platform provides a digital solution for managing the complete scholarship application lifecycle.

By integrating student registration, scholarship discovery, academic and financial information management, document verification, committee review, and fund allocation, the application simplifies scholarship administration.

The combination of Python Flask, MySQL, HTML, and CSS provides the foundation for a centralized, manageable, and extensible scholarship management system.

The project demonstrates the practical application of web development, database management, authentication, file handling, and administrative workflow automation.
