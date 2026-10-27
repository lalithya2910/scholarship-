USE scholarship;

CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(15),
    password VARCHAR(255) NOT NULL,
    date_of_birth DATE,
    gender VARCHAR(20),
    category VARCHAR(50),
    address TEXT,
    college VARCHAR(150),
    course VARCHAR(100),
    year INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE admins (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE academic_details (
    academic_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    previous_exam VARCHAR(100),
    percentage DECIMAL(5,2),
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);

CREATE TABLE financial_details (
    financial_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    annual_income DECIMAL(12,2) NOT NULL,
    family_members INT,
    parent_occupation VARCHAR(100),
    income_certificate_no VARCHAR(100),
    financial_status ENUM(
        'Pending',
        'Approved',
        'Rejected'
    ) DEFAULT 'Pending',
    FOREIGN KEY (student_id)
        REFERENCES students(student_id)
);
CREATE TABLE documents (
    document_id INT AUTO_INCREMENT PRIMARY KEY,
    application_id INT NOT NULL,
    document_type VARCHAR(100) NOT NULL,
    document_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    verification_status ENUM(
        'Pending',
        'Verified',
        'Rejected'
    ) DEFAULT 'Pending',
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (application_id)
        REFERENCES applications(application_id)
);
CREATE TABLE scholarships (
    scholarship_id INT AUTO_INCREMENT PRIMARY KEY,
    scholarship_name VARCHAR(150) NOT NULL,
    description TEXT,
    minimum_percentage DECIMAL(5,2) DEFAULT 0.00,
    maximum_income DECIMAL(12,2),
    category VARCHAR(100) DEFAULT 'All',
    available_amount DECIMAL(12,2) NOT NULL,
    max_amount_per_student DECIMAL(12,2),
    deadline DATE NOT NULL,
    status ENUM(
        'Active',
        'Expired',
        'Closed'
    ) DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE applications (
    application_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    scholarship_id INT NOT NULL,
    application_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM(
        'Pending',
        'Approved',
        'Rejected',
        'Allocated'
    ) DEFAULT 'Pending',
    eligibility_status ENUM(
        'Pending',
        'Eligible',
        'Ineligible'
    ) DEFAULT 'Pending',
    priority_score DECIMAL(6,2) DEFAULT 0.00,
    rank_position INT,
    committee_comment TEXT,
    allocated_amount DECIMAL(12,2) DEFAULT 0.00,

    FOREIGN KEY (student_id)
        REFERENCES students(student_id),

    FOREIGN KEY (scholarship_id)
        REFERENCES scholarships(scholarship_id)
);
CREATE TABLE scholarship_required_documents (
    requirement_id INT AUTO_INCREMENT PRIMARY KEY,
    scholarship_id INT NOT NULL,
    document_name VARCHAR(150) NOT NULL,
    FOREIGN KEY (scholarship_id)
        REFERENCES scholarships(scholarship_id)
        ON DELETE CASCADE
);
CREATE TABLE committee_reviews (
    review_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    application_id INT NOT NULL,
    reviewer_id INT NOT NULL,
    review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    decision ENUM('Approved', 'Rejected', 'Needs Verification') NOT NULL,
    comments TEXT,
    FOREIGN KEY (application_id) REFERENCES applications(application_id),
    FOREIGN KEY (reviewer_id) REFERENCES admins(admin_id)
);
CREATE TABLE fund_allocations (
    allocation_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    application_id INT NOT NULL UNIQUE,
    allocated_amount DECIMAL(12,2) NOT NULL,
    allocation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    payment_status ENUM(
        'Pending',
        'Processing',
        'Transferred',
        'Failed'
    ) DEFAULT 'Pending',
    transaction_id VARCHAR(100),
    FOREIGN KEY (application_id)
        REFERENCES applications(application_id)
);

INSERT INTO scholarships
(scholarship_id, scholarship_name, description, minimum_percentage,
 maximum_income, category, available_amount, max_amount_per_student,
 deadline, status)
VALUES
(1, 'Reliance Foundation Undergraduate Scholarship',
'Provides financial assistance to undergraduate students pursuing higher education. Applicants must have at least 60% marks and annual family income not exceeding Rs. 15000000. Required documents include Class 12 marksheet and family income certificate.',
60.00, 15000000.00, 'All', 1000000.00, 200000.00, '2026-12-31', 'Active'),

(2, 'AICTE Pragati Scholarship for Girls',
'Supports eligible female students pursuing technical education. Applicants must satisfy the applicable academic requirements and annual family income limit of Rs. 800000. Required documents include academic marksheet, income certificate and AICTE college allotment letter.',
60.00, 800000.00, 'Female Only', 950000.00, 50000.00, '2026-12-31', 'Active'),

(3, 'Central Sector Scheme of Scholarship (CSSS)',
'Provides financial assistance to meritorious students pursuing higher education. For this project, the sample eligibility criteria include at least 80% marks and annual family income not exceeding Rs. 450000. Required documents include Class 12 marksheet and income certificate.',
80.00, 450000.00, 'All', 1000000.00, 20000.00, '2026-12-31', 'Active'),

(4, 'Sitaram Jindal Foundation Scholarship',
'Provides financial assistance to eligible students to continue their education. The sample project criteria require at least 55% marks for girls or 60% for boys, with annual family income not exceeding Rs. 400000. Required documents include previous examination marksheet and college bonafide certificate.',
55.00, 400000.00, 'All', 1000000.00, 50000.00, '2026-12-31', 'Active'),

(5, 'State ePASS Scholarship',
'Supports eligible students from specified social categories with educational expenses. Applicants must satisfy applicable state residence, family income and other eligibility requirements. Eligible categories for this sample project are SC, ST, BC and EBC. Required documents include caste certificate and income certificate or ration card.',
60.00, 200000.00, 'SC/ST/BC/EBC', 950000.00, 50000.00, '2026-12-31', 'Active');

INSERT INTO scholarship_required_documents
    (scholarship_id, document_name)
VALUES
    (1, 'Class 12 Marksheet'),
    (1, 'Income Certificate'),
    (2, 'Academic Marksheet'),
    (2, 'Income Certificate'),
    (2, 'AICTE College Allotment Letter'),
    (3, 'Class 12 Marksheet'),
    (3, 'Income Certificate'),
    (4, 'Previous Examination Marksheet'),
    (4, 'College Bonafide Certificate'),
    (5, 'Caste Certificate'),
    (5, 'Income Certificate or Ration Card');
