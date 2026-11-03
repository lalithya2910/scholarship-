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

INSERT INTO students
(student_id, name, email, phone, password, date_of_birth,
 gender, category, address, college, course, year)
VALUES
(1, 'Lalithya Vanacharla', 'vanacharlalalithya@gmail.com', '9010101010',
'scrypt:32768:8:1$AE53cwP05MXxuu6e$42cf11fe95a506dc824b720938e162628784b45a47260ed1bfb26874a211a89e5755e328db1c51353cc7a1b128467ec3b2eb927e41bdc6f99713af5a249b5502',
'2026-10-15', 'Female', 'ST', 'kaikaram', 'SRKR ENGINEERING COLLEGE', 'IT', 4),

(2, 'Vanacharla', 'admin@scholarship.com', '9292929292',
'scrypt:32768:8:1$gBwEAeCNyH09ZrB0$63476d52c81a837d3495b3e652ab1450a8f4d01fcd5302974e2c19c3ee2d59f60d901db5540ecc148d7073e88856cb1a72ca15bf7e0f4a590bab8f02c08a96ce',
'2026-10-16', 'Female', 'SC', 'kai', 'SRKR ENGINEERING COLLEGE', 'IT', 2),

(3, 'Vana', 'lalithya@gmail.com', '9010101010',
'scrypt:32768:8:1$nWEYgKXM9oV62NAd$ca5281948668035abf7f043094ba82554f4046961fae6bcf7fb5fea65f265477a54313e5ac39e6e565f1759eb93232e8c33a0deb708f105b9563e7f4fde42125',
'2026-10-28', 'Female', 'OBC', 'kaikaram', 'SRKR ENGINEERING COLLEGE', 'IT', 3),

(4, 'Likhitha Vanacharla', 'likhitha@scholarship.com', '9292929292',
'scrypt:32768:8:1$QhEkYU8Tg5WIW5Vn$3e87dfeed5ac50fe90db7e828a25339e2903d3fce027f0e41c0d2a1917b7dbc44067cdde9def6f5bcebce012e5b92b9be5a12547a83c326d8600e5373e7418eb',
'2026-10-26', 'Female', 'ST', 'kerela', 'SRKR ENGINEERING COLLEGE', 'IT', 2),

(5, 'vanacharla lalithya', 'lalithyavanacharla29@gmail.com', '9292929292',
'scrypt:32768:8:1$gG9xVlLj4aXBdPHH$2da8e9ddbb1dc85abb6be065c79375368e3405204e2f691e09c97c60dfcd2cc3be6dce7193f46adeed9dd2f9c9506e130cef1c222c50459c27b260a773c5527f',
'2026-10-19', 'Female', 'ST', 'kashmir', 'SRKR ENGINEERING COLLEGE', 'IT', 3),

(6, 'keerthi', 'keerthi@gmail.com', '9010101010',
'scrypt:32768:8:1$bFgGtpfnSo0ejOhJ$06fa8b569e9c5f2a24aad622c70b654bb0e5e3bc6452950b1050cf1cb6c2ae6b397637227f8a9b37be420edc6289598219c9119e75b796eb3a5d1fed452c2a9c',
'2000-02-12', 'Female', 'SC', 'tadepalligudem', 'vasavi', 'ece', 4);

INSERT INTO admins
(admin_id, name, email, password, created_at)
VALUES
(
    1,
    'lalithya',
    'vanacharlalalithya@gmail.com',
    'scrypt:32768:8:1$tFChGzDVP6vSDl9Y$5c86b810ee00679004cb9eb63f0a42b09089a8e48f82d0843e1a582006cc38cbc68d04c0d8a06a96fbb3ee96f6166d65043e7de2a0c6037a6f854ae7bc285478',
    '2026-10-10 01:08:42'
);
