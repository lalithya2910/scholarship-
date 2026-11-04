
# Scholarship Eligibility and Fund Allocation Platform

## 1. Project Overview

The **Scholarship Eligibility and Fund Allocation Platform** is a web-based application developed to simplify and manage the scholarship application and fund allocation process.

The system provides a centralized platform where students can register, explore available scholarships, submit applications, enter academic and financial details, and upload required documents.

Administrators can manage scholarships, review student applications, verify submitted documents, approve or reject applications, and allocate scholarship funds manually.

The main objective is to improve transparency, reduce manual work, and make scholarship management more efficient.


## 2. Features

The **Scholarship Eligibility and Fund Allocation Platform** provides separate functionalities for students and administrators. It simplifies the scholarship application process, helps administrators manage applications, and supports transparent scholarship fund allocation.

### 2.1 Student Module

The Student Module allows students to register, explore available scholarships, submit applications, and track their application progress.

1. **Student Registration and Secure Login:** Students can create an account by providing their required personal details. Registered students can securely log in using their email address and password to access their dashboard.

2. **View Available Scholarships:** Students can view the scholarships published by the administrator. The platform displays important information such as scholarship name, eligibility conditions, scholarship amount, application deadline, and availability.

3. **Check Scholarship Eligibility Requirements:** Students can check the eligibility criteria before applying. These criteria may include minimum academic percentage, maximum family income, category requirements, and other scholarship-specific conditions.

4. **Apply for Scholarships:** Students can select a suitable scholarship and submit their application through the platform. The system stores the submitted application details in the database for further administrative review.

5. **Submit Academic Information:** Students can provide their academic details, such as qualification, institution name, course, year of study, and academic percentage or marks. These details help administrators evaluate the application.

6. **Submit Financial Information:** Students can enter their family income and other required financial details. This information helps administrators understand the student's financial background while reviewing the application.

7. **Upload Required Supporting Documents:** Students can upload the necessary documents, such as academic certificates, income certificates, and other supporting documents. These documents are stored and made available for administrator verification.

8. **Track Application Status:** Students can monitor the progress of their submitted applications through their dashboard. They can check whether an application is pending, approved, rejected, or allocated.

9. **View Approval and Fund Allocation Details:** Once the administrator approves an application and allocates funds, students can view the approval status and allocated scholarship amount through their account.

10. **Forgot Password and OTP-Based Password Reset:** If students forget their password, they can request a password reset using their registered email address. The system sends a One-Time Password (OTP) for verification before allowing them to create a new password.

### 2.2 Admin Module

The Admin Module provides administrators with the facilities required to manage scholarships, monitor student applications, verify documents, and allocate scholarship funds.

1. **Secure Admin Login:** Administrators can access the administration section using their authorized login credentials. This ensures that scholarship management activities are restricted to authorized users.

2. **Admin Dashboard with Application Statistics:** The admin dashboard provides an overview of platform activities through statistical cards. It displays information such as the total number of students, scholarships, applications, pending reviews, eligible applications, approved applications, and allocated funds.

3. **Add New Scholarships:** Administrators can create and publish new scholarship opportunities by entering details such as scholarship name, description, minimum academic percentage, maximum family income, category, available amount, maximum amount per student, and application deadline.

4. **Edit Existing Scholarships:** Administrators can update the details of existing scholarships whenever changes are required. This helps maintain accurate scholarship information and eligibility conditions.

5. **Delete Scholarships:** Administrators can remove scholarships that are no longer required or available. This helps keep the scholarship list updated.

6. **View Registered Students:** Administrators can view the details of students registered on the platform. This helps them access student information whenever required for application verification.

7. **Review Scholarship Applications:** Administrators can view the applications submitted by students and examine the academic and financial information provided in each application before making a decision.

8. **Verify Uploaded Student Documents:** Administrators can access the documents uploaded by students and check whether the submitted certificates and supporting documents are valid and appropriate. Based on verification, documents can be marked as verified or rejected.

9. **Approve or Reject Applications:** After reviewing the application details and supporting documents, administrators can make the final decision. Eligible applications can be approved, while applications that do not satisfy the requirements can be rejected.

10. **Manually Allocate Scholarship Funds:** Administrators can manually enter and allocate scholarship amounts to approved applications. The allocation is performed based on the available scholarship funds and the maximum amount permitted per student.

11. **Track Available and Allocated Scholarship Funds:** The platform maintains scholarship fund information. After a successful allocation, the allocated amount is recorded and the available scholarship balance is updated in the database. This helps administrators monitor the remaining funds.

### 2.3 General Features

General features support the overall security, data management, and proper functioning of the platform.

1. **Role-Based Access Control:** The platform provides separate access for students and administrators. Students can access student-related functionalities, while administrators can manage scholarships and applications.

2. **MySQL Database Integration:** MySQL is used to store and manage important application data, including student details, scholarship information, academic records, financial details, uploaded document paths, application statuses, and fund allocation records.

3. **Secure Password Hashing:** User passwords are stored in hashed form instead of plain text using Werkzeug password hashing functions. This helps protect user login credentials.

4. **Email-Based OTP Verification:** The platform uses email-based OTP verification for password reset. This adds an additional verification step before a user can change their password.

5. **Document Upload Management:** Students can upload required supporting documents through the application process. The system manages uploaded files and stores their corresponding file paths for administrator access and verification.

6. **Application Status Management:** The system maintains application statuses such as Pending, Approved, Rejected, and Allocated. These statuses help students and administrators understand the current stage of each application.

7. **Scholarship Fund Management:** The platform maintains available scholarship amounts and records manual allocations. The available balance is reduced when funds are successfully allocated to approved applications.

### Overall Outcome

These features provide a centralized platform where students can apply for scholarships and track their applications, while administrators can manage scholarship opportunities, verify applications, make approval decisions, and allocate funds efficiently.

## 3. Technology Stack

| Category | Technologies |
|---|---|
| Frontend | HTML, CSS, Bootstrap 5, JavaScript |
| Backend | Python, Flask |
| Database | MySQL |
| Database Connector | mysql-connector-python |
| Authentication | Flask Sessions, Werkzeug Password Hashing |
| Email Service | Python Email / SMTP |
| Development Tools | Visual Studio Code, Git, GitHub |


## 4. Project Workflow

The Scholarship Eligibility and Fund Allocation Platform follows two major workflows: Student Scholarship Application and Admin Scholarship Management.

### Workflow Diagram

```mermaid
flowchart TD
    A([Start]) --> B[Student Registration]
    B --> C[Student Login]
    C --> D[View Available Scholarships]
    D --> E[Apply for Scholarship]
    E --> F[Submit Academic Details]
    F --> G[Submit Financial Details]
    G --> H[Upload Required Documents]

    I([Admin Login]) --> J[Manage Scholarships]
    J --> K[Add / Edit / Delete Scholarships]
    K --> L[Review Applications]
    H --> L

    L --> M[Verify Uploaded Documents]
    M --> N{Admin Decision}
    N -->|Approved| O[Manual Fund Allocation]
    N -->|Rejected| P[Application Rejected]
    O --> Q[Update Available Funds]
    P --> R[Student Checks Application Status]
    Q --> R
    R --> S([End])
```

### Workflow Description

**Student Workflow:**
1. Student registers and logs into the platform.
2. Views available scholarships and eligibility requirements.
3. Selects and applies for a suitable scholarship.
4. Submits academic and financial details.
5. Uploads the required supporting documents.

**Admin Workflow:**
1. Administrator logs into the admin panel.
2. Adds new scholarships, edits existing scholarship details, or deletes scholarships.
3. Reviews submitted student applications.
4. Verifies uploaded supporting documents.
5. Approves or rejects applications.
6. Manually allocates scholarship funds to approved applications.
7. Updates the available scholarship funds after successful allocation.

**Final Step:**

Students can log in to check their application status and view their allocated scholarship amount, if applicable.


## 5. Project Setup and Installation

### Prerequisites

- Python 3.10 or above
- MySQL Server
- Git
- Visual Studio Code (recommended)

### Step 1: Clone the Repository

```bash
git clone https://github.com/lalithya2910/scholarship-
```

### Step 2: Navigate to the Project Directory

```bash
cd scholarship-
```

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 4: Activate the Virtual Environment

For Windows:

```bash
venv\Scripts\activate
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Configure the Database

1. Start your MySQL Server.
2. Create a database named `scholarship`.
3. Import the provided SQL database file.
4. Configure the database connection details in the `.env` file.

### Step 7: Run the Application

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000/
```

## 6. Environment Variables

Create a `.env` file in the project root directory and configure the following variables:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=scholarship

SECRET_KEY=your_secret_key

MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_email_app_password
```

**Note:** Replace the example values with your actual configuration. Never upload your `.env` file or expose database credentials and email passwords on GitHub.

## 7. API and Database Notes

### Database

The application uses MySQL to store and manage student, scholarship, application, academic, financial, document, and fund allocation information.

Major database tables include:

- `students` – Stores student registration details.
- `admins` – Stores administrator login details.
- `scholarships` – Stores scholarship information and funding limits.
- `applications` – Stores student scholarship applications and their statuses.
- `academic_details` – Stores academic information.
- `financial_details` – Stores family income and financial information.
- `documents` – Stores uploaded document references and verification status.
- `scholarship_required_documents` – Stores required documents for scholarships.
- `fund_allocations` – Stores scholarship fund allocation records.
- `bank_details` – Stores student bank account-related information.

### Application Processing

- Flask routes handle student and admin requests.
- MySQL queries perform database operations.
- Student and scholarship information is stored in relational tables.
- Application status is updated based on administrator decisions.
- Fund allocation records are maintained in the database.
- Available scholarship funds are updated after successful allocation.

The application primarily uses Flask server-side routes and does not depend on a separate REST API service.

## 8. Team Member Contributions

### Individual Project Development

**Team Member:** Lalithya Vanacharla  
**Role:** Full Stack Developer

This project was independently designed and developed by Lalithya Vanacharla. I was responsible for the complete development lifecycle, including requirement analysis, system design, frontend development, backend implementation, database integration, testing, debugging, and project documentation.

### Key Responsibilities

**1. Requirement Analysis and Planning**

- Identified the challenges in traditional scholarship application and fund management processes.
- Analyzed the requirements of students and administrators.
- Planned the application workflow and identified the major system modules.
- Designed the overall functionality to simplify scholarship application processing and fund allocation.

**2. Frontend Development**

- Designed and developed user interfaces using HTML, CSS, Bootstrap 5, and JavaScript.
- Created responsive and user-friendly pages for student and administrator modules.
- Developed registration, login, scholarship listing, application forms, and dashboard interfaces.
- Implemented navigation and application status displays to improve the user experience.

**3. Backend Development**

- Developed the application backend using Python and the Flask framework.
- Implemented student registration, authentication, and session management.
- Developed scholarship application processing functionality.
- Implemented academic and financial information submission.
- Integrated document upload and application tracking functionality.
- Developed administrator functionalities for managing scholarships and reviewing applications.

**4. Database Design and Integration**

- Designed and managed the MySQL relational database.
- Created and integrated database tables for students, administrators, scholarships, applications, academic details, financial details, documents, and fund allocations.
- Implemented database operations for inserting, retrieving, updating, and deleting records.
- Integrated Flask with MySQL using `mysql-connector-python`.
- Managed scholarship fund availability and allocation records.

**5. Scholarship Management and Administration**

- Implemented scholarship creation, modification, and deletion functionality.
- Developed the application review process for administrators.
- Implemented document verification functionality.
- Developed application approval and rejection features.
- Implemented manual scholarship fund allocation with funding limit validation.
- Integrated dashboard statistics to monitor students, scholarships, applications, and allocated funds.

**6. Security and Authentication**

- Implemented role-based access for students and administrators.
- Used password hashing for secure password storage.
- Implemented email-based OTP verification for password reset.
- Used Flask sessions to manage authenticated users.
- Configured environment variables to protect sensitive application credentials.

**7. Testing and Debugging**

- Tested student registration, login, and scholarship application workflows.
- Verified database connectivity and data consistency.
- Tested document upload and verification functionality.
- Checked application approval, rejection, and fund allocation processes.
- Identified and resolved errors during development.
- Validated application functionality through different user scenarios.

**8. Documentation and Version Control**

- Prepared project documentation and technical descriptions.
- Maintained source code using Git and GitHub.
- Organized project files and dependencies.
- Created README documentation with setup instructions and configuration details.
- Managed the project repository for submission and future maintenance.

### Development Outcome

Successfully developed a web-based Scholarship Eligibility and Fund Allocation Platform that provides a centralized system for managing scholarship applications, verifying student documents, reviewing applications, and allocating scholarship funds. The project demonstrates practical implementation of full-stack web development, database management, authentication, and application workflow automation.

## 9. Future Scope

- Automated scholarship eligibility verification.
- Applicant priority scoring and ranking.
- Online scholarship payment integration.
- Advanced analytics and report generation.
- SMS notifications for application updates.
- Mobile application support.

## 10. Conclusion

The Scholarship Eligibility and Fund Allocation Platform provides an organized and transparent approach to managing scholarship applications. It reduces administrative workload, simplifies document verification, and helps administrators manage scholarship approvals and fund allocation efficiently.

## 11. Repository

GitHub: [Scholarship Eligibility and Fund Allocation Platform](https://github.com/lalithya2910/scholarship-)
