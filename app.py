from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, session, send_file, abort
)
from pathlib import Path
from uuid import uuid4
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from database import get_db_connection
from mail import generate_otp, send_email
from datetime import datetime, timedelta,date

app = Flask(__name__)
app.secret_key = "scholarship_secret_key"

# Upload folder configuration
UPLOAD_FOLDER = Path(app.root_path) / "scholarship_documents"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {"pdf", "jpg", "jpeg", "png"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
  # Change this to a secure random key in production

@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        connection = None
        cursor = None

        try:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)

            cursor.execute(
                "SELECT * FROM students WHERE email = %s",
                (email,)
            )

            student = cursor.fetchone()

            if student and check_password_hash(student["password"], password):

                session.clear()
                session["student_id"] = student["student_id"]
                session["student_name"] = student["name"]

                flash("Login successful!", "success")

                return redirect(url_for("dashboard"))

            else:
                flash("Invalid email or password.", "error")

        except Exception as e:
            print("Login error:", e)
            flash("Something went wrong. Please try again.", "error")

        finally:
            if cursor:
                cursor.close()

            if connection:
                connection.close()

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        # Get form data
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        date_of_birth = request.form.get("date_of_birth") or None
        gender = request.form.get("gender") or None
        category = request.form.get("category") or None
        address = request.form.get("address") or None
        college = request.form.get("college") or None
        course = request.form.get("course") or None
        year = request.form.get("year") or None

        # Check password confirmation
        if password != confirm_password:
            flash("Passwords do not match!", "error")
            return redirect(url_for("register"))

        # Check password length
        if len(password) < 8:
            flash("Password must contain at least 8 characters.", "error")
            return redirect(url_for("register"))

        connection = None
        cursor = None

        try:
            # Connect to database
            connection = get_db_connection()
            cursor = connection.cursor()

            # Check whether email already exists
            cursor.execute(
                "SELECT student_id FROM students WHERE email = %s",
                (email,)
            )

            existing_student = cursor.fetchone()

            if existing_student:
                flash("Email already registered. Please login.", "error")
                return redirect(url_for("login"))

            # Hash password
            hashed_password = generate_password_hash(password)

            # Insert student details
            query = """
                INSERT INTO students
                (
                    name, email, phone, password, date_of_birth,
                    gender, category, address, college, course, year
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            values = (
                name, email, phone, hashed_password, date_of_birth,
                gender, category, address, college, course, year
            )

            cursor.execute(query, values)
            connection.commit()

            flash("Registration successful! Please login.", "success")
            return redirect(url_for("login"))

        except Exception as e:
            if connection:
                connection.rollback()

            print("Registration error:", e)
            flash("Registration failed. Please try again.", "error")

        finally:
            if cursor:
                cursor.close()

            if connection:
                connection.close()

    return render_template("register.html")

@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():

    if request.method == "POST":

        email = request.form.get("email", "").strip()

        connection = None
        cursor = None

        try:
            # Connect to database
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)

            # Get student details using email
            cursor.execute(
                "SELECT student_id, name, email FROM students WHERE email = %s",
                (email,)
            )

            student = cursor.fetchone()

            if student:

                # Generate OTP using your existing mail.py function
                otp = generate_otp()

                # Send OTP to the student's email
                email_sent = send_email(
                    student["email"],
                    student["name"],
                    otp
                )

                if email_sent:

                    # Store email and OTP in Flask session
                    session["reset_email"] = student["email"]
                    session["reset_otp"] = otp

                    # Clear previous OTP verification status
                    session.pop("otp_verified", None)

                    flash(
                        "OTP sent successfully to your registered email!",
                        "success"
                    )

                    return redirect(url_for("verify_otp"))

                else:
                    flash(
                        "Unable to send OTP. Please check your email configuration.",
                        "error"
                    )

            else:
                flash(
                    "Email address not found. Please enter your registered email.",
                    "error"
                )

        except Exception as e:

            print("Forgot password error:", e)

            flash(
                "Something went wrong. Please try again.",
                "error"
            )

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()

    return render_template("forgot_password.html")



@app.route("/reset_password", methods=["GET", "POST"])
def reset_password():

    # Check whether OTP verification was completed
    if not session.get("otp_verified") or not session.get("reset_email"):
        flash("Please verify your OTP first.", "error")
        return redirect(url_for("forgot_password"))

    if request.method == "POST":

        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # Check whether passwords match
        if password != confirm_password:
            flash("Passwords do not match!", "error")
            return render_template("reset_password.html")

        # Check password length
        if len(password) < 8:
            flash("Password must contain at least 8 characters.", "error")
            return render_template("reset_password.html")

        connection = None
        cursor = None

        try:
            email = session["reset_email"]

            # Hash the new password
            hashed_password = generate_password_hash(password)

            connection = get_db_connection()
            cursor = connection.cursor()

            # Update the student's password
            cursor.execute(
                "UPDATE students SET password = %s WHERE email = %s",
                (hashed_password, email)
            )

            if cursor.rowcount == 0:
                connection.rollback()
                flash("Unable to update password. Please try again.", "error")
                return render_template("reset_password.html")

            connection.commit()

            # Clear password-reset session data
            session.pop("reset_email", None)
            session.pop("reset_otp", None)
            session.pop("otp_verified", None)

            flash("Password reset successful! Please login.", "success")
            return redirect(url_for("login"))

        except Exception as e:
            if connection:
                connection.rollback()

            print("Reset password error:", e)
            flash("Something went wrong. Please try again.", "error")

        finally:
            if cursor:
                cursor.close()

            if connection:
                connection.close()

    return render_template("reset_password.html")

@app.route("/verify_otp", methods=["GET", "POST"])
def verify_otp():

    if not session.get("reset_email") or not session.get("reset_otp"):
        flash("Please request an OTP first.", "error")
        return redirect(url_for("forgot_password"))

    if request.method == "POST":

        entered_otp = request.form.get("otp", "").strip()
        stored_otp = str(session.get("reset_otp", ""))

        # Temporary debugging
        print("Entered OTP:", repr(entered_otp))
        print("Stored OTP:", repr(stored_otp))

        if entered_otp == stored_otp:

            session["otp_verified"] = True
            session.pop("reset_otp", None)

            flash(
                "OTP verified successfully! Reset your password.",
                "success"
            )

            return redirect(url_for("reset_password"))

        else:
            flash("Invalid OTP. Please try again.", "error")

    return render_template("verify_otp.html")

# ---------------- STUDENT DASHBOARD ----------------

@app.route('/dashboard')
def dashboard():

    # Check whether student is logged in
    if 'student_id' not in session:
        return redirect(url_for('login'))

    student_id = session['student_id']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get logged-in student details
    cursor.execute(
        "SELECT * FROM students WHERE student_id = %s",
        (student_id,)
    )
    student = cursor.fetchone()

    # Total applications
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM applications
        WHERE student_id = %s
    """, (student_id,))

    total_applications = cursor.fetchone()['total']

    # Pending applications
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM applications
        WHERE student_id = %s AND status = 'Pending'
    """, (student_id,))

    pending_applications = cursor.fetchone()['total']

    # Approved applications
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM applications
        WHERE student_id = %s AND status = 'Approved'
    """, (student_id,))

    approved_applications = cursor.fetchone()['total']
    # Approved applications
    cursor.execute("""
            SELECT COUNT(*) AS total
            FROM applications
            WHERE student_id = %s AND status = 'Allocated'
        """, (student_id,))
    
    allocated_applications = cursor.fetchone()['total']

    # Rejected applications
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM applications
        WHERE student_id = %s AND status = 'Rejected'
    """, (student_id,))

    rejected_applications = cursor.fetchone()['total']
 


    # Get recent applications of this student
    cursor.execute("""
        SELECT
            a.application_id,
            a.application_date,
            a.status,
            a.eligibility_status,
            s.scholarship_name
        FROM applications a
        JOIN scholarships s
            ON a.scholarship_id = s.scholarship_id
        WHERE a.student_id = %s
        ORDER BY a.application_date DESC
        LIMIT 5
    """, (student_id,))

    recent_applications = cursor.fetchall()

    cursor.close()
    conn.close()

    # Student not found
    if student is None:
        session.clear()
        return redirect(url_for('login'))

    return render_template(
        'dashboard.html',
        student=student,
        total_applications=total_applications,
        pending_applications=pending_applications,
        approved_applications=approved_applications,
        allocated_applications=allocated_applications,
        rejected_applications=rejected_applications,
        recent_applications=recent_applications
    )

@app.route('/scholarships')
def scholarships():

    # Check whether student is logged in
    if 'student_id' not in session:
        return redirect(url_for('login'))

    # Connect to database
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch all active scholarships
    cursor.execute("""
        SELECT *
        FROM scholarships
        WHERE status = 'Active'
        ORDER BY scholarship_id
    """)

    scholarship_list = cursor.fetchall()

    # Close database connection
    cursor.close()
    conn.close()

    # Send scholarship data to HTML page
    return render_template(
        'scholarships.html',
        scholarships=scholarship_list
    )


@app.route('/scholarship_details/<int:scholarship_id>')
def scholarship_details(scholarship_id):

    if 'student_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM scholarships WHERE scholarship_id = %s",
        (scholarship_id,)
    )

    scholarship = cursor.fetchone()

    cursor.close()
    conn.close()

    if scholarship is None:
        return "Scholarship not found", 404

    return render_template(
        'scholarship_details.html',
        scholarship=scholarship
    )


# ---------------- APPLICATION STATUS ----------------


@app.route('/application_status')
def application_status():

    if 'student_id' not in session:
        return redirect(url_for('login'))

    student_id = session['student_id']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                a.application_id,
                a.application_date,
                a.status,
                a.eligibility_status,
                s.scholarship_name,
                CASE
                    WHEN a.status IN ('Approved','Allocated')
                    THEN fa.allocated_amount
                    ELSE NULL
                END AS allocated_amount
            FROM applications a
            JOIN scholarships s
                ON a.scholarship_id = s.scholarship_id
            LEFT JOIN fund_allocations fa
                ON a.application_id = fa.application_id
            WHERE a.student_id = %s
            ORDER BY a.application_date DESC
        """, (student_id,))

        applications = cursor.fetchall()

    finally:
        cursor.close()
        conn.close()

    return render_template(
        'application_status.html',
        applications=applications
    )



@app.route('/apply_scholarship/<int:scholarship_id>',
           methods=['GET', 'POST'])
def apply_scholarship(scholarship_id):

    if 'student_id' not in session:
        flash('Please login first.', 'error')
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    saved_files = []
    scholarship = None
    required_documents = []

    try:
        # Get scholarship details
        cursor.execute("""
            SELECT *
            FROM scholarships
            WHERE scholarship_id = %s
              AND status = 'Active'
        """, (scholarship_id,))

        scholarship = cursor.fetchone()

        if not scholarship:
            return "Scholarship not found or inactive", 404

        # Fetch required documents from database
        cursor.execute("""
            SELECT document_name
            FROM scholarship_required_documents
            WHERE scholarship_id = %s
            ORDER BY requirement_id
        """, (scholarship_id,))

        required_documents = [
            row['document_name']
            for row in cursor.fetchall()
        ]

        if request.method == 'POST':

            # Academic details
            previous_exam = request.form.get(
                'previous_exam', ''
            ).strip()

            percentage = request.form.get(
                'percentage', ''
            ).strip()

            # Financial details
            family_income = request.form.get(
                'family_income', ''
            ).strip()

            family_members = request.form.get(
                'family_members', ''
            ).strip()

            parent_occupation = request.form.get(
                'parent_occupation', ''
            ).strip()

            income_certificate_no = request.form.get(
                'income_certificate_no', ''
            ).strip() or None

            # Personal details
            gender = request.form.get('gender', '')
            category = request.form.get('category', '')

            if not previous_exam or not parent_occupation:
                raise ValueError(
                    'Please fill in all required details.'
                )

            if not percentage or not family_income or not family_members:
                raise ValueError(
                    'Please complete academic and financial details.'
                )

            try:
                percentage = float(percentage)
                family_income = float(family_income)
                family_members = int(family_members)
            except ValueError:
                raise ValueError(
                    'Enter valid academic and financial values.'
                )

            if not 0 <= percentage <= 100:
                raise ValueError(
                    'Percentage must be between 0 and 100.'
                )

            if family_income < 0 or family_members < 1:
                raise ValueError(
                    'Enter valid family income and family members.'
                )

            if gender not in ('Male', 'Female', 'Other'):
                raise ValueError(
                    'Please select a valid gender.'
                )

            if category not in ('OC', 'SC', 'ST', 'BC', 'EBC'):
                raise ValueError(
                    'Please select a valid category.'
                )

            if request.form.get('declaration') != 'on':
                raise ValueError(
                    'Please accept the declaration.'
                )

            student_id = session['student_id']

            # Prevent duplicate application
            cursor.execute("""
                SELECT application_id
                FROM applications
                WHERE student_id = %s
                  AND scholarship_id = %s
            """, (student_id, scholarship_id))

            if cursor.fetchone():
                raise ValueError(
                    'You have already applied for this scholarship.'
                )

            # Validate uploaded documents
            uploaded_documents = []

            for i, document_type in enumerate(required_documents):
                uploaded_file = request.files.get(
                    f'document_{i}'
                )

                if not uploaded_file or not uploaded_file.filename:
                    raise ValueError(
                        f'Please upload: {document_type}'
                    )

                original_name = secure_filename(
                    uploaded_file.filename
                )

                if not original_name or '.' not in original_name:
                    raise ValueError(
                        f'Invalid filename for: {document_type}'
                    )

                extension = original_name.rsplit(
                    '.', 1
                )[1].lower()

                if extension not in ALLOWED_EXTENSIONS:
                    raise ValueError(
                        'Only PDF, JPG, JPEG and PNG files are allowed.'
                    )

                # Check file size
                uploaded_file.stream.seek(0, 2)
                file_size = uploaded_file.stream.tell()
                uploaded_file.stream.seek(0)

                if file_size == 0:
                    raise ValueError(
                        f'The selected file is empty: {document_type}'
                    )

                if file_size > MAX_FILE_SIZE:
                    raise ValueError(
                        'Each document must be 10 MB or smaller.'
                    )

                uploaded_documents.append((
                    document_type,
                    original_name,
                    uploaded_file,
                    extension
                ))

            # Save personal details
            cursor.execute("""
                UPDATE students
                SET gender = %s, category = %s
                WHERE student_id = %s
            """, (gender, category, student_id))

            # Save academic details
            cursor.execute("""
                INSERT INTO academic_details
                    (student_id, previous_exam, percentage)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    previous_exam = %s,
                    percentage = %s
            """, (
                student_id, previous_exam, percentage,
                previous_exam, percentage
            ))

            # Save financial details
            cursor.execute("""
                INSERT INTO financial_details
                    (student_id, annual_income, family_members,
                     parent_occupation, income_certificate_no)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    annual_income = %s,
                    family_members = %s,
                    parent_occupation = %s,
                    income_certificate_no = %s
            """, (
                student_id, family_income, family_members,
                parent_occupation, income_certificate_no,
                family_income, family_members,
                parent_occupation, income_certificate_no
            ))

            # Create application
            cursor.execute("""
                INSERT INTO applications
                    (student_id, scholarship_id, status,
                     eligibility_status, priority_score)
                VALUES (%s, %s, 'Pending', 'Pending', 0)
            """, (student_id, scholarship_id))

            application_id = cursor.lastrowid

            # Save documents in the application folder
            application_folder = UPLOAD_FOLDER / str(application_id)
            application_folder.mkdir(
                parents=True, exist_ok=True
            )

            for document_type, original_name, uploaded_file, extension in uploaded_documents:

                stored_name = f"{uuid4().hex}.{extension}"
                disk_path = application_folder / stored_name

                uploaded_file.save(str(disk_path))
                saved_files.append(disk_path)

                # Save document information in database
                cursor.execute("""
                    INSERT INTO documents
                        (application_id, document_type, document_name,
                         file_path, verification_status)
                    VALUES (%s, %s, %s, %s, 'Pending')
                """, (
                    application_id,
                    document_type,
                    original_name,
                    str(disk_path.resolve())
                ))

            conn.commit()

            flash(
                'Application submitted successfully!',
                'success'
            )

            return redirect(
                url_for('application_status')
            )

    except ValueError as error:
        conn.rollback()

        for path in saved_files:
            try:
                path.unlink(missing_ok=True)
            except OSError:
                app.logger.exception(
                    'Could not remove uploaded file'
                )

        flash(str(error), 'danger')

    except Exception:
        conn.rollback()

        for path in saved_files:
            try:
                path.unlink(missing_ok=True)
            except OSError:
                app.logger.exception(
                    'Could not remove uploaded file'
                )

        app.logger.exception(
            'Scholarship application submission failed'
        )

        flash(
            'Application could not be submitted. '
            'Please check the database columns and try again.',
            'danger'
        )

    finally:
        cursor.close()
        conn.close()

    return render_template(
        'apply_scholarship.html',
        scholarship=scholarship,
        required_documents=required_documents
    )

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute(
                "SELECT * FROM admins WHERE email = %s",
                (email,)
            )
            admin = cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

        if admin and check_password_hash(admin['password'], password):
            session['admin_id'] = admin['admin_id']
            session['admin_name'] = admin['name']

            flash('Admin login successful!', 'success')
            return redirect(url_for('admin_dashboard'))

        flash('Invalid email or password!', 'danger')

    return render_template('admin_login.html')




@app.route('/admin_dashboard')
def admin_dashboard():

    # Check admin login
    if 'admin_id' not in session:
        flash('Please login as admin.', 'error')
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Total students
    cursor.execute("SELECT COUNT(*) AS total FROM students")
    total_students = cursor.fetchone()['total']

    # Total scholarships
    cursor.execute("SELECT COUNT(*) AS total FROM scholarships")
    total_scholarships = cursor.fetchone()['total']

    # Total applications
    cursor.execute("SELECT COUNT(*) AS total FROM applications")
    total_applications = cursor.fetchone()['total']

    # Pending reviews
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM applications
        WHERE status = 'Pending'
    """)
    pending_reviews = cursor.fetchone()['total']

    # Eligible applications
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM applications
        WHERE eligibility_status = 'Eligible'
    """)
    eligible_applications = cursor.fetchone()['total']

    # Approved applications
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM applications
        WHERE status = 'Approved'
    """)
    approved_applications = cursor.fetchone()['total']

    # Total funds allocated
    cursor.execute("""
        SELECT COALESCE(SUM(allocated_amount), 0) AS total
        FROM applications
        WHERE status = 'Allocated'
    """)
    total_funds_allocated = cursor.fetchone()['total']

    # Recent applications
    cursor.execute("""
        SELECT
            a.application_id,
            s.name,
            sc.scholarship_name,
            a.status
        FROM applications a
        JOIN students s
            ON a.student_id = s.student_id
        JOIN scholarships sc
            ON a.scholarship_id = sc.scholarship_id
        ORDER BY a.application_date DESC
        
    """)
    recent_applications = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'admin_dashboard.html',
        total_students=total_students,
        total_scholarships=total_scholarships,
        total_applications=total_applications,
        pending_reviews=pending_reviews,
        eligible_applications=eligible_applications,
        approved_applications=approved_applications,
        total_funds_allocated=total_funds_allocated,
        recent_applications=recent_applications
    )


@app.route('/manage_scholarship', methods=['GET', 'POST'])
def manage_scholarship():

    if 'admin_id' not in session:
        flash('Please login as admin.', 'error')
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        conn = None
        cursor = None

        try:
            scholarship_name = request.form.get(
                'scholarship_name', ''
            ).strip()

            description = request.form.get(
                'description', ''
            ).strip()

            minimum_percentage = float(
                request.form.get('minimum_percentage') or 0
            )

            maximum_income_input = request.form.get(
                'maximum_income', ''
            ).strip()

            category = request.form.get('category', 'All')

            available_amount = float(
                request.form.get('available_amount') or 0
            )

            max_amount_input = request.form.get(
                'max_amount_per_student', ''
            ).strip()

            deadline_input = request.form.get('deadline', '')

            # New scholarships are always Active
            status = 'Active'

            required_documents = request.form.getlist(
                'required_documents'
            )

            # Validate input
            if not scholarship_name:
                flash('Scholarship name is required.', 'error')
                return redirect(url_for('manage_scholarship'))

            if not 0 <= minimum_percentage <= 100:
                flash(
                    'Minimum percentage must be between 0 and 100.',
                    'error'
                )
                return redirect(url_for('manage_scholarship'))

            maximum_income = (
                float(maximum_income_input)
                if maximum_income_input else None
            )

            max_amount_per_student = (
                float(max_amount_input)
                if max_amount_input else None
            )

            if maximum_income is not None and maximum_income < 0:
                flash('Annual income cannot be negative.', 'error')
                return redirect(url_for('manage_scholarship'))

            if available_amount <= 0:
                flash(
                    'Available amount must be greater than zero.',
                    'error'
                )
                return redirect(url_for('manage_scholarship'))

            if max_amount_per_student is not None:
                if max_amount_per_student < 0:
                    flash(
                        'Maximum amount cannot be negative.',
                        'error'
                    )
                    return redirect(url_for('manage_scholarship'))

                if max_amount_per_student > available_amount:
                    flash(
                        'Maximum amount per student cannot exceed '
                        'the total available amount.',
                        'error'
                    )
                    return redirect(url_for('manage_scholarship'))

            if not deadline_input:
                flash('Please select a deadline.', 'error')
                return redirect(url_for('manage_scholarship'))

            deadline = date.fromisoformat(deadline_input)

            if deadline < date.today():
                flash('Deadline cannot be in the past.', 'error')
                return redirect(url_for('manage_scholarship'))

            if not required_documents:
                flash(
                    'Please select at least one required document.',
                    'error'
                )
                return redirect(url_for('manage_scholarship'))

            # Connect to database
            conn = get_db_connection()
            cursor = conn.cursor()

            # Insert scholarship
            cursor.execute("""
                INSERT INTO scholarships (
                    scholarship_name,
                    description,
                    minimum_percentage,
                    maximum_income,
                    category,
                    available_amount,
                    max_amount_per_student,
                    deadline,
                    status
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                scholarship_name,
                description or None,
                minimum_percentage,
                maximum_income,
                category,
                available_amount,
                max_amount_per_student,
                deadline,
                status
            ))

            scholarship_id = cursor.lastrowid

            # Save selected documents for this scholarship
            cursor.executemany("""
                INSERT INTO scholarship_required_documents (
                    scholarship_id,
                    document_name
                )
                VALUES (%s, %s)
            """, [
                (scholarship_id, document)
                for document in required_documents
            ])

            conn.commit()

            flash(
                'Scholarship and required documents created successfully!',
                'success'
            )

            return redirect(url_for('manage_scholarship'))

        except ValueError:
            if conn:
                conn.rollback()

            flash(
                'Please enter valid numeric values and deadline.',
                'error'
            )

        except Exception as e:
            if conn:
                conn.rollback()

            print("Scholarship error:", e)

            flash(
                'Unable to create scholarship. Please check the details.',
                'error'
            )

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # Fetch scholarships and update expired statuses
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        update_expired_scholarships(cursor)
        conn.commit()

        cursor.execute("""
            SELECT *
            FROM scholarships
            ORDER BY created_at DESC
        """)

        scholarships = cursor.fetchall()

    finally:
        cursor.close()
        conn.close()

    return render_template(
        'manage_scholarship.html',
        scholarships=scholarships,
        today=date.today()
    )

@app.route(
    '/change_scholarship_status/<int:scholarship_id>/<action>',
    methods=['POST']
)
def change_scholarship_status(scholarship_id, action):

    if 'admin_id' not in session:
        flash('Please login as admin.', 'error')
        return redirect(url_for('admin_login'))

    if action not in ('close', 'reopen'):
        flash('Invalid action.', 'error')
        return redirect(url_for('manage_scholarship'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Update expired scholarships first
        update_expired_scholarships(cursor)

        cursor.execute("""
            SELECT deadline, status
            FROM scholarships
            WHERE scholarship_id = %s
        """, (scholarship_id,))

        scholarship = cursor.fetchone()

        if not scholarship:
            flash('Scholarship not found.', 'error')

        elif scholarship['deadline'] < date.today():
            conn.commit()
            flash('Expired scholarship cannot be reopened or closed.', 'error')

        elif action == 'close':
            if scholarship['status'] != 'Active':
                flash('Only active scholarships can be closed.', 'error')
            else:
                cursor.execute("""
                    UPDATE scholarships
                    SET status = 'Closed'
                    WHERE scholarship_id = %s
                """, (scholarship_id,))

                conn.commit()
                flash('Applications closed successfully.', 'success')

        elif action == 'reopen':
            if scholarship['status'] != 'Closed':
                flash('Only closed scholarships can be reopened.', 'error')
            else:
                cursor.execute("""
                    UPDATE scholarships
                    SET status = 'Active'
                    WHERE scholarship_id = %s
                """, (scholarship_id,))

                conn.commit()
                flash('Applications reopened successfully.', 'success')

    except Exception as e:
        conn.rollback()
        print("Scholarship status error:", e)
        flash('Unable to update scholarship status.', 'error')

    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('manage_scholarship'))


def update_expired_scholarships(cursor):
    cursor.execute("""
        UPDATE scholarships
        SET status = 'Expired'
        WHERE deadline < %s
          AND status IN ('Active', 'Closed')
    """, (date.today(),))


@app.route('/edit_scholarship/<int:scholarship_id>', methods=['GET', 'POST'])
def edit_scholarship(scholarship_id):

    if 'admin_id' not in session:
        flash('Please login as admin first.', 'error')
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)

    try:
        # Fetch scholarship details
        cursor.execute("""
            SELECT *
            FROM scholarships
            WHERE scholarship_id = %s
        """, (scholarship_id,))

        scholarship = cursor.fetchone()

        if not scholarship:
            flash('Scholarship not found.', 'error')
            return redirect(url_for('manage_scholarships'))

        # Fetch all available document types
        cursor.execute("""
            SELECT DISTINCT document_name
            FROM scholarship_required_documents
            ORDER BY document_name
        """)
        all_documents = cursor.fetchall()

        # Fetch documents selected for this scholarship
        cursor.execute("""
            SELECT document_name
            FROM scholarship_required_documents
            WHERE scholarship_id = %s
        """, (scholarship_id,))

        selected_rows = cursor.fetchall()
        selected_documents = [
            row['document_name'] for row in selected_rows
        ]

        if request.method == 'POST':

            scholarship_name = request.form.get(
                'scholarship_name', ''
            ).strip()

            description = request.form.get(
                'description', ''
            ).strip()

            category = request.form.get('category', '').strip()
            deadline = request.form.get('deadline', '').strip()
            status = request.form.get('status', '').strip()

            required_documents = request.form.getlist(
                'required_documents'
            )

            try:
                minimum_percentage = float(
                    request.form.get('minimum_percentage', '')
                )
                maximum_income = float(
                    request.form.get('maximum_income', '')
                )
                available_amount = float(
                    request.form.get('available_amount', '')
                )
                max_amount_per_student = float(
                    request.form.get('max_amount_per_student', '')
                )

                from datetime import date

                deadline_date = date.fromisoformat(deadline)

                if not scholarship_name or not category:
                    raise ValueError(
                        'Scholarship name and category are required.'
                    )

                if not 0 <= minimum_percentage <= 100:
                    raise ValueError(
                        'Minimum percentage must be between 0 and 100.'
                    )

                if min(
                    maximum_income,
                    available_amount,
                    max_amount_per_student
                ) < 0:
                    raise ValueError(
                        'Income and amounts cannot be negative.'
                    )

                if max_amount_per_student > available_amount:
                    raise ValueError(
                        'Maximum amount per student cannot exceed available funds.'
                    )

                if status not in ['Active', 'Closed', 'Expired']:
                    raise ValueError('Invalid scholarship status.')

                # Prevent document names not offered by the form
                valid_document_names = {
                    row['document_name'] for row in all_documents
                }

                if not set(required_documents).issubset(
                    valid_document_names
                ):
                    raise ValueError('Invalid required document selected.')

            except (ValueError, TypeError):
                conn.rollback()
                flash(
                    'Please enter valid values in all fields.',
                    'error'
                )
                return render_template(
                    'edit_scholarship.html',
                    scholarship=scholarship,
                    all_documents=all_documents,
                    selected_documents=selected_documents
                )

            try:
                # Update scholarship information
                cursor.execute("""
                    UPDATE scholarships
                    SET scholarship_name = %s,
                        description = %s,
                        minimum_percentage = %s,
                        maximum_income = %s,
                        category = %s,
                        available_amount = %s,
                        max_amount_per_student = %s,
                        deadline = %s,
                        status = %s
                    WHERE scholarship_id = %s
                """, (
                    scholarship_name,
                    description,
                    minimum_percentage,
                    maximum_income,
                    category,
                    available_amount,
                    max_amount_per_student,
                    deadline_date,
                    status,
                    scholarship_id
                ))

                # Replace this scholarship's required document list
                cursor.execute("""
                    DELETE FROM scholarship_required_documents
                    WHERE scholarship_id = %s
                """, (scholarship_id,))

                for document_name in dict.fromkeys(required_documents):
                    cursor.execute("""
                        INSERT INTO scholarship_required_documents
                            (scholarship_id, document_name)
                        VALUES (%s, %s)
                    """, (scholarship_id, document_name))

                conn.commit()

                flash(
                    'Scholarship details updated successfully!',
                    'success'
                )
                return redirect(url_for('manage_scholarship'))

            except Exception as e:
                conn.rollback()
                print('Scholarship update error:', e)
                flash(
                    'Unable to update scholarship details.',
                    'error'
                )

        return render_template(
            'edit_scholarship.html',
            scholarship=scholarship,
            all_documents=all_documents,
            selected_documents=selected_documents
        )

    except Exception as e:
        conn.rollback()
        print('Edit scholarship error:', e)
        flash('Unable to load scholarship details.', 'error')
        return redirect(url_for('manage_scholarships'))

    finally:
        cursor.close()
        conn.close()




@app.route('/application_review/<int:application_id>', methods=['GET', 'POST'])
def application_review(application_id):

    # Check admin login
    if 'admin_id' not in session:
        flash('Please login as admin first.', 'error')
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)

    try:
        # Get application and related details
        cursor.execute("""
            SELECT
                ap.*,
                st.name,
                st.email,
                st.phone,
                st.gender,
                st.category AS student_category,
                st.college,
                st.course,
                st.year,

                ac.previous_exam,
                ac.percentage,
                

                fd.annual_income,
                fd.parent_occupation,

                sh.scholarship_name,
                sh.description,
                sh.minimum_percentage,
                sh.maximum_income,
                sh.category AS scholarship_category,
                sh.deadline,
                sh.available_amount,
                sh.max_amount_per_student

            FROM applications ap

            JOIN students st
                ON ap.student_id = st.student_id

            JOIN scholarships sh
                ON ap.scholarship_id = sh.scholarship_id

            LEFT JOIN academic_details ac
                ON ap.student_id = ac.student_id

            LEFT JOIN financial_details fd
                ON ap.student_id = fd.student_id

            WHERE ap.application_id = %s
        """, (application_id,))

        application = cursor.fetchone()

        if not application:
            flash('Application not found.', 'error')
            return redirect(url_for('admin_dashboard'))

        # Prevent reviewing already processed applications
        if application['status'] != 'Pending':
            flash(
                'This application has already been reviewed.',
                'error'
            )
            return redirect(url_for('admin_dashboard'))

        # Get uploaded documents
        cursor.execute("""
            SELECT
                document_id,
                document_type,
                document_name,
                file_path,
                verification_status
            FROM documents
            WHERE application_id = %s
        """, (application_id,))

        documents = cursor.fetchall()

        # ----------------------------------
        # DOCUMENT VERIFICATION
        # ----------------------------------
        if (
            request.method == 'POST'
            and request.form.get('action') == 'verify_document'
        ):

            document_id = request.form.get('document_id')
            verification_status = request.form.get(
                'verification_status', ''
            )

            if verification_status not in [
                'Pending', 'Verified', 'Rejected'
            ]:
                flash(
                    'Please select a valid document status.',
                    'error'
                )

            elif not document_id or not document_id.isdigit():
                flash('Invalid document ID.', 'error')

            else:
                cursor.execute("""
                    UPDATE documents
                    SET verification_status = %s
                    WHERE document_id = %s
                      AND application_id = %s
                """, (
                    verification_status,
                    int(document_id),
                    application_id
                ))

                if cursor.rowcount == 1:
                    conn.commit()
                    flash(
                        'Document verification status updated!',
                        'success'
                    )
                else:
                    conn.rollback()
                    flash('Document not found.', 'error')

            return redirect(url_for(
                'application_review',
                application_id=application_id
            ))

        # ----------------------------------
        # FINAL APPLICATION REVIEW
        # ----------------------------------
        if request.method == 'POST':

            decision = request.form.get('decision', '')
            comment = request.form.get(
                'committee_comment', ''
            ).strip()

            # Match decisions with committee_reviews ENUM
            valid_decisions = [
                'Approved',
                'Rejected',
                'Needs Verification'
            ]

            if decision not in valid_decisions:
                flash('Please select a valid decision.', 'error')

            elif not comment:
                flash(
                    'Please enter committee comments.',
                    'error'
                )

            else:
                # Fetch latest document statuses
                cursor.execute("""
                    SELECT verification_status
                    FROM documents
                    WHERE application_id = %s
                """, (application_id,))

                current_documents = cursor.fetchall()

                all_documents_verified = (
                    len(current_documents) > 0
                    and all(
                        doc['verification_status'] == 'Verified'
                        for doc in current_documents
                    )
                )

                # Approval requires all documents verified
                if (
                    decision == 'Approved'
                    and not all_documents_verified
                ):
                    flash(
                        'Please verify all documents before '
                        'approving the application.',
                        'error'
                    )

                    return redirect(url_for(
                        'application_review',
                        application_id=application_id
                    ))

                # Map committee decision to application status
                if decision == 'Approved':
                    application_status = 'Approved'
                    eligibility = 'Eligible'

                elif decision == 'Rejected':
                    application_status = 'Rejected'
                    eligibility = 'Ineligible'

                else:
                    application_status = 'Pending'
                    eligibility = 'Pending'

                try:
                    # Save committee review history
                    cursor.execute("""
                        INSERT INTO committee_reviews
                            (
                                application_id,
                                reviewer_id,
                                decision,
                                comments
                            )
                        VALUES (%s, %s, %s, %s)
                    """, (
                        application_id,
                        session['admin_id'],
                        decision,
                        comment
                    ))

                    # Update application record
                    cursor.execute("""
                        UPDATE applications
                        SET status = %s,
                            eligibility_status = %s,
                            committee_comment = %s
                        WHERE application_id = %s
                          AND status = 'Pending'
                    """, (
                        application_status,
                        eligibility,
                        comment,
                        application_id
                    ))

                    if cursor.rowcount == 1:
                        conn.commit()
                        flash(
                            'Application review saved successfully!',
                            'success'
                        )
                    else:
                        conn.rollback()
                        flash(
                            'Application has already been updated.',
                            'error'
                        )

                except Exception as e:
                    conn.rollback()
                    print('Committee Review Error:', e)

                    flash(
                        'Unable to save the committee review.',
                        'error'
                    )

                return redirect(url_for('admin_dashboard'))

        # Display review page
        return render_template(
            'application_review.html',
            application=application,
            documents=documents
        )

    except Exception as e:
        conn.rollback()
        print('Application Review Error:', e)

        flash(
            'Unable to process the application review.',
            'error'
        )

        return redirect(url_for('admin_dashboard'))

    finally:
        cursor.close()
        conn.close()


@app.route('/view_document/<int:document_id>')
def view_document(document_id):

    # 1. Admin login check
    if 'admin_id' not in session:
        flash('Please login as admin first.', 'error')
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)

    try:
        # 2. Fetch document details and status
        cursor.execute("""
            SELECT document_id, application_id,
                   file_path, document_name,
                   verification_status
            FROM documents
            WHERE document_id = %s
        """, (document_id,))

        document = cursor.fetchone()

        if not document:
            abort(404)

        # 3. Get actual file path
        file_path = Path(document['file_path']).resolve()

        upload_folder = (
            Path(app.root_path) / 'scholarship_documents'
        ).resolve()

        # 4. Restrict access to uploaded document folder
        if not file_path.is_relative_to(upload_folder):
            abort(403)

        # 5. Check file existence
        if not file_path.is_file():
            abort(404)

        # 6. Automatically update Pending to Verified
        # Do not overwrite an existing Rejected status
        if document['verification_status'] == 'Pending':

            # Verify the related application is still Pending
            cursor.execute("""
                SELECT status
                FROM applications
                WHERE application_id = %s
            """, (document['application_id'],))

            application_record = cursor.fetchone()

            if (
                application_record
                and application_record['status'] == 'Pending'
            ):
                cursor.execute("""
                    UPDATE documents
                    SET verification_status = 'Verified'
                    WHERE document_id = %s
                      AND verification_status = 'Pending'
                """, (document_id,))

                conn.commit()

        # 7. Send document to admin
        return send_file(
            file_path,
            as_attachment=False,
            download_name=Path(
                document['document_name']
            ).name
        )

    except Exception as e:
        conn.rollback()
        print('View Document Error:', e)
        raise

    finally:
        cursor.close()
        conn.close()

@app.route('/delete_scholarship/<int:scholarship_id>', methods=['POST'])
def delete_scholarship(scholarship_id):

    if 'admin_id' not in session:
        flash('Please login as admin first.', 'error')
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)

    try:
        cursor.execute("""
            SELECT scholarship_id
            FROM scholarships
            WHERE scholarship_id = %s
        """, (scholarship_id,))

        scholarship = cursor.fetchone()

        if not scholarship:
            flash('Scholarship not found.', 'error')
            return redirect(url_for('manage_scholarship'))

        # Prevent deleting scholarships with existing applications
        cursor.execute("""
            SELECT application_id
            FROM applications
            WHERE scholarship_id = %s
            LIMIT 1
        """, (scholarship_id,))

        if cursor.fetchone():
            flash(
                'This scholarship has applications and cannot be deleted.',
                'error'
            )
            return redirect(url_for('manage_scholarship'))

        # Delete associated required document records
        cursor.execute("""
            DELETE FROM scholarship_required_documents
            WHERE scholarship_id = %s
        """, (scholarship_id,))

        # Delete scholarship
        cursor.execute("""
            DELETE FROM scholarships
            WHERE scholarship_id = %s
        """, (scholarship_id,))

        conn.commit()
        flash('Scholarship deleted successfully!', 'success')

    except Exception as e:
        conn.rollback()
        print('Delete Scholarship Error:', e)
        flash('Unable to delete scholarship.', 'error')

    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('manage_scholarship'))        


@app.route('/fund_allocation', methods=['GET', 'POST'])
def fund_allocation():

    if 'admin_id' not in session:
        flash('Please login as admin first.', 'error')
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:

        if request.method == 'POST':

            application_id = request.form.get(
                'application_id', type=int
            )
            allocated_amount = request.form.get(
                'allocated_amount', type=float
            )

            if (
                not application_id
                or allocated_amount is None
                or allocated_amount <= 0
            ):
                flash('Please enter a valid amount.', 'error')
                return redirect(url_for('fund_allocation'))

            # Get application and scholarship details
            cursor.execute("""
                SELECT
                    a.application_id,
                    a.status,
                    a.allocated_amount AS existing_amount,
                    a.scholarship_id,
                    s.available_amount,
                    s.max_amount_per_student
                FROM applications a
                JOIN scholarships s
                    ON a.scholarship_id = s.scholarship_id
                WHERE a.application_id = %s
                FOR UPDATE
            """, (application_id,))

            application = cursor.fetchone()

            if not application:
                conn.rollback()
                flash('Application not found.', 'error')
                return redirect(url_for('fund_allocation'))

            # Only approved applications can receive allocation
            if application['status'] != 'Approved':
                conn.rollback()
                flash(
                    'Only approved applications can receive funds.',
                    'error'
                )
                return redirect(url_for('fund_allocation'))

            # Prevent duplicate allocations
            if (
                application['existing_amount'] is not None
                and float(application['existing_amount']) > 0
            ):
                conn.rollback()
                flash(
                    'An amount is already recorded for this application.',
                    'error'
                )
                return redirect(url_for('fund_allocation'))

            available_amount = float(application['available_amount'])
            max_amount = application['max_amount_per_student']

            if allocated_amount > available_amount:
                conn.rollback()
                flash('Insufficient scholarship funds.', 'error')
                return redirect(url_for('fund_allocation'))

            if (
                max_amount is not None
                and allocated_amount > float(max_amount)
            ):
                conn.rollback()
                flash(
                    'Amount exceeds the maximum per-student limit.',
                    'error'
                )
                return redirect(url_for('fund_allocation'))

            # Save allocation record
            cursor.execute("""
                INSERT INTO fund_allocations
                    (application_id, allocated_amount, payment_status)
                VALUES (%s, %s, 'Pending')
            """, (application_id, allocated_amount))

            # Update application status and amount
            cursor.execute("""
                UPDATE applications
                SET status = 'Allocated',
                    allocated_amount = %s
                WHERE application_id = %s
                  AND status = 'Approved'
            """, (allocated_amount, application_id))

            if cursor.rowcount != 1:
                conn.rollback()
                flash('Allocation failed. Please try again.', 'error')
                return redirect(url_for('fund_allocation'))

            # Reduce remaining scholarship funds
            cursor.execute("""
                UPDATE scholarships
                SET available_amount = available_amount - %s
                WHERE scholarship_id = %s
                  AND available_amount >= %s
            """, (
                allocated_amount,
                application['scholarship_id'],
                allocated_amount
            ))

            if cursor.rowcount != 1:
                conn.rollback()
                flash('Insufficient funds. Allocation cancelled.', 'error')
                return redirect(url_for('fund_allocation'))

            conn.commit()

            flash('Funds allocated successfully.', 'success')
            return redirect(url_for('fund_allocation'))

        # Display approved applications awaiting allocation
        cursor.execute("""
            SELECT
                a.application_id,
                st.name AS student_name,
                s.scholarship_name,
                s.available_amount,
                s.max_amount_per_student
            FROM applications a
            JOIN students st
                ON a.student_id = st.student_id
            JOIN scholarships s
                ON a.scholarship_id = s.scholarship_id
            LEFT JOIN fund_allocations fa
                ON a.application_id = fa.application_id
            WHERE a.status = 'Approved'
              AND fa.allocation_id IS NULL
            ORDER BY a.application_id DESC
        """)

        applications = cursor.fetchall()

        return render_template(
            'fund_allocation.html',
            applications=applications
        )

    except Exception:
        conn.rollback()
        app.logger.exception('Fund allocation failed')
        flash('An error occurred during fund allocation.', 'error')
        return redirect(url_for('fund_allocation'))

    finally:
        cursor.close()
        conn.close()


@app.route("/logout")
def logout():

    session.clear()

    flash("Logged out successfully!", "success")

    return redirect(url_for("index"))






if __name__ == '__main__':
    app.run(debug=True)
