from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv
from datetime import datetime, timezone
from flask_migrate import Migrate

# Load environment variables from the .env file
load_dotenv()
# Initialize Flask app and database
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')


# Get database credentials from environment variables
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

# Configure the SQLAlchemy URI using the environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db)

# User Model
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)

# StudentDetails table
class StudentDetails(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key to user table
    dob = db.Column(db.Date, nullable=False)
    father_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    contact_number = db.Column(db.String(15), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    date_of_admission = db.Column(db.Date, nullable=False)
    course = db.Column(db.String(100), nullable=False)
    year_of_study = db.Column(db.Integer, nullable=False)
    student_status = db.Column(db.String(50), nullable=False)
    emergency_contact_number = db.Column(db.String(15), nullable=False)
    nationality = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    zip_code = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))


# Function to create users when the app starts
def create_users():
    # Check if the admin and student users already exist in the database
    admin_user = User.query.filter_by(email="admin@test.com").first()
    student_user = User.query.filter_by(email="student@test.com").first()
    
    if not admin_user:
        # Hardcode admin user with plain text password
        hashed_password = generate_password_hash("admin123")
        admin_user = User(username="admin", email="admin@test.com", password=hashed_password, role="admin")
        db.session.add(admin_user)
    
    if not student_user:
        # Hardcode student user with plain text password
        hashed_password = generate_password_hash("student123")
        student_user = User(username="student", email="student@test.com", password=hashed_password, role="student")
        db.session.add(student_user)

    db.session.commit()

# Before request to ensure users are created
@app.before_request
def before_request():
    # Run the create_users function only once before handling any request
    if not hasattr(app, 'users_created'):
        create_users()
        app.users_created = True  # Mark that users have been created

# Home route
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        role = request.form['role']
        if role == 'admin':
            return redirect(url_for('admin_login'))
        elif role == 'student':
            return redirect(url_for('student_login'))
    
    return render_template('home.html')  # Show home page with role selection

# Admin Login Route
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if 'role' in session and session['role'] == 'student':
        flash("Students cannot access the admin login page.", "danger")
        return redirect(url_for('student_dashboard'))  # Redirect to student dashboard if student is logged in

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Query for an admin user
        user = User.query.filter_by(email=email, role='admin').first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            flash("Login successful! Welcome, Admin.", "success")
            return redirect(url_for('admin_dashboard'))  # Redirect to admin dashboard
        else:
            flash("Invalid email or password.", "danger")
            return redirect(url_for('admin_login'))  # Redirect back to login page

    return render_template('admin_login.html')

# Student Login Route
@app.route('/student/login', methods=['GET', 'POST'])
def student_login():
    # Check if the user is already logged in as admin
    if 'role' in session and session['role'] == 'admin':
        flash("Admins cannot access the student login page.", "danger")
        return redirect(url_for('admin_dashboard'))  # Redirect to admin dashboard if admin is logged in

    # Handle POST request for login
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Debugging: Log the email being submitted
        print(f"Attempting to log in with email: {email}")
        
        # Query for a student user with the given email
        user = User.query.filter_by(email=email, role='student').first()
        
        # Debugging: Check if user is found
        if user:
            print(f"Found user: {user.username}, Role: {user.role}")
            print(f"Stored Password Hash: {user.password}")  # Debugging: Log stored password hash
            print(f"Provided Password: {password}")  # Debugging: Log provided password
        else:
            print("No user found with the given email and role.")
        
        # Check if user exists and password matches
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            flash("Login successful! Welcome, Student.", "success")
            print(f"Session Info: {session}")  # Debugging session info
            return redirect(url_for('student_dashboard'))  # Redirect to student dashboard
        else:
            print("Invalid email or password.")
            flash("Invalid email or password.", "danger")
            return redirect(url_for('student_login'))  # Redirect back to login page

    # Render the student login page if GET request
    return render_template('student_login.html')

# Admin Dashboard
@app.route('/admin/dashboard')
def admin_dashboard():
    if 'role' not in session or session['role'] != 'admin':
        flash("You must be an admin to access this page.", "danger")
        return redirect(url_for('admin_login'))  # Redirect to admin login if the user is not an admin

    # Get all student profiles from the database
    students = User.query.filter_by(role='student').all()

    return render_template('admin_dashboard.html', students=students)

from flask import Flask, render_template, request, redirect, url_for


# Admin Route to create a student record
@app.route('/admin/create_student', methods=['GET', 'POST'])
def create_student():
    if request.method == 'POST':
        # First, handle basic student information
        if 'user_id' not in request.form:
            username = request.form['username']
            email = request.form['email']

            # Create a new User record
            new_user = User(username=username, email=email, password=generate_password_hash("default_password"), role="student")
            db.session.add(new_user)
            db.session.commit()  # Commit to get user ID
            user_id = new_user.id

            # Redirect to the second part of the form with the user_id
            return redirect(url_for('create_student', user_id=user_id))

        # Second, handle additional student details
        user_id = request.form['user_id']
        dob = request.form['dob']
        father_name = request.form['father_name']
        address = request.form['address']
        contact_number = request.form['contact_number']
        gender = request.form['gender']
        date_of_admission = request.form['date_of_admission']
        course = request.form['course']
        year_of_study = request.form['year_of_study']
        student_status = request.form['student_status']
        emergency_contact_number = request.form['emergency_contact_number']
        nationality = request.form['nationality']
        city = request.form['city']
        state = request.form['state']
        zip_code = request.form['zip_code']

        print("------")
        print(user_id, dob, gender, year_of_study, emergency_contact_number)
        print("------")
        # Check if the student already exists in the database (based on user_id)
        existing_student = StudentDetails.query.filter_by(user_id=user_id).first()
        if existing_student:
            flash("Student details already exist!", "warning")
            return redirect(url_for('view_student', user_id=user_id))

        # Create a new StudentDetails record
        new_student = StudentDetails(
            user_id=user_id, dob=dob, father_name=father_name, address=address,
            contact_number=contact_number, gender=gender, date_of_admission=date_of_admission,
            course=course, year_of_study=year_of_study, student_status=student_status,
            emergency_contact_number=emergency_contact_number, nationality=nationality,
            city=city, state=state, zip_code=zip_code
        )
        db.session.add(new_student)
        db.session.commit()  # Commit to save the student details

        flash("Student created successfully!", "success")
        return redirect(url_for('view_student', user_id=user_id))

    # Render the form for the first part (basic student info)
    user_id = request.args.get('user_id', None)
    if user_id:
        return render_template('create_student.html', user_id=user_id)

    # Render the first part of the form
    return render_template('create_student.html')


# Admin View Student Route
@app.route('/admin/view_student/<int:user_id>')
def view_student(user_id):
    student = StudentDetails.query.filter_by(user_id=user_id).first()
    if student:
        return render_template('view_student.html', student=student)
    return "Student not found", 404

# Update Student Route
@app.route('/admin/update_student/<int:student_id>', methods=['GET', 'POST'])
def update_student(student_id):
    if 'role' not in session or session['role'] != 'admin':
        flash("You must be an admin to access this page.", "danger")
        return redirect(url_for('admin_login'))

    student = User.query.get_or_404(student_id)

    if request.method == 'POST':
        student.username = request.form['username']
        student.email = request.form['email']
        
        # Optional: Update password (ensure password is hashed)
        if request.form['password']:
            student.password = generate_password_hash(request.form['password'])
        
        db.session.commit()

        flash("Student profile updated successfully.", "success")
        return redirect(url_for('admin_dashboard'))

    return render_template('update_student.html', student=student)

# Delete Student Route with Confirmation
@app.route('/admin/delete_student/<int:student_id>', methods=['GET', 'POST'])
def delete_student(student_id):
    if 'role' not in session or session['role'] != 'admin':
        flash("You must be an admin to access this page.", "danger")
        return redirect(url_for('admin_login'))

    student = User.query.get_or_404(student_id)

    # If the request method is GET, show the confirmation page
    if request.method == 'GET':
        return render_template('delete_student.html', student=student)

    # If the request method is POST, delete the student
    db.session.delete(student)
    db.session.commit()

    flash("Student profile deleted successfully.", "success")
    return redirect(url_for('admin_dashboard'))


# Student Dashboard
@app.route('/student/dashboard', methods=['GET', 'POST'])
def student_dashboard():
    if 'role' not in session or session['role'] != 'student':
        flash("You need to log in as Student first!", "danger")
        return redirect(url_for('student_login'))
    # Get the student details using the logged-in user's ID
    student_details = StudentDetails.query.filter_by(user_id=session['user_id']).first()
    student_name_details = User.query.filter_by(id=session['user_id']).first()
    if student_details:
        return render_template('student_dashboard.html', student=student_details, student1 = student_name_details)
    else:
        flash("Student details not found!", "danger")
        return redirect(url_for('student_login'))  # Redirect back to log

# Logout route
@app.route('/logout')
def logout():
    session.clear()  # Clears the session
    flash("You have been logged out.", "info")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
