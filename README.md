
<div align="center">

# 🎓 Scholarship Eligibility and Fund Allocation Platform

### A Smart Platform for Scholarship Applications, Verification and Fund Management

<p>
  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python" />
  <img src="https://img.shields.io/badge/Flask-Web_Framework-black?logo=flask" />
  <img src="https://img.shields.io/badge/MySQL-Database-blue?logo=mysql" />
  <img src="https://img.shields.io/badge/HTML5-Frontend-orange?logo=html5" />
  <img src="https://img.shields.io/badge/CSS3-Styling-blue?logo=css3" />
</p>

</div>

---

## 📌 Overview

A web-based scholarship management platform that simplifies
student applications, document verification, eligibility
assessment and scholarship fund allocation.

## ✨ Features

- Student registration and authentication
- Email OTP verification
- Scholarship discovery and applications
- Academic and financial information management
- Supporting document uploads
- Application status tracking
- Admin scholarship management
- Document verification and application review
- Scholarship fund allocation

## 👨‍🎓 Student Module

Detailed student functionality.

## 🛡️ Admin Module

Detailed administrator functionality.

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Frontend | HTML, CSS |
| Database | MySQL |
| Authentication | Flask Sessions |
| Email | Gmail SMTP |
| Password Security | Werkzeug |

## 🏗️ Architecture

Student / Admin
       |
       v
Flask Web Application
       |
       v
Business Logic
       |
       v
MySQL Database

## 🔄 Application Workflow

1. Student registration
2. Student login
3. Scholarship discovery
4. Application submission
5. Document verification
6. Admin review
7. Approval or rejection
8. Fund allocation
9. Status tracking

## 🗄️ Database Design

| Table | Purpose |
|---|---|
| students | Student information |
| admins | Admin accounts |
| scholarships | Scholarship information |
| applications | Application records |
| documents | Uploaded documents |
| academic_details | Academic records |
| financial_details | Financial records |
| committee_reviews | Review records |
| fund_allocations | Allocation records |

## 🚀 Installation and Setup

```bash
git clone https://github.com/lalithya2910/scholarship-.git
cd scholarship-
python -m venv venv
```

Activate the environment and install dependencies:

```bash
pip install -r requirements.txt
```

Configure MySQL and the environment variables.

Run:

```bash
python app.py
```

Open:

http://127.0.0.1:5000/

## ⚙️ Environment Variables

Document your database, SMTP and Flask configuration.

## 📁 Project Structure

Document the actual repository folders and files.

## 🔐 Security

- Password hashing
- OTP verification
- Session-based authentication
- File upload validation
- Fund availability checks

## 👩‍💻 Developer

**Lalithya**

Individual Project | Sole Developer

## 🔮 Future Enhancements

- Automated eligibility assessment
- AI-based scholarship recommendations
- Advanced reporting and analytics

## 📌 Repository

https://github.com/lalithya2910/scholarship-

