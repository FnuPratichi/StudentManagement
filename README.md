# A Backend-Focused Web Application powered by Python (Flask), utilizing PostgreSQL for database management. Deployed on AWS EC2 with containerization via Docker and ECR, utilizing AWS RDS for database hosting

DEMO of Project : https://drive.google.com/file/d/1gQp89QeTFFnt53DU6_wp3h_2lQwUn1Zg/view?usp=sharing

# 🚀 Project Features: Routes and Functionalities
# 🏠 Home Page
1. Route: /
2. Purpose: Allows users to select their role (Admin or Student).
3. Functionality:
    - Redirects users to the respective login pages based on their role.
    - Ensures only valid roles (Admin or Student) are allowed.
  
# 🔐 Authentication
# Admin Login
1. Route: /admin/login
2. Purpose: Enables administrators to log in.
3. Functionality:
      - Validates admin credentials (email and password).
      - Stores admin session data upon successful login.
      - Redirects to the admin dashboard for management activities.
        
# Student Login
1. Route: /student/login
2. Purpose: Allows students to log in.
3. Functionality:
      - Validates student credentials (email and password).
      - Tracks whether it's the student's first login.
      - Redirects first-time users to the password reset page for added security.
  

# 🔄 First-Time Login Password Reset
1. Route: /student/reset_password
2. Purpose: Empowers students to reset their default password during their first login.
3. Functionality:
    - Ensures the new password matches the confirmation.
    - Updates the database with the new password and sets first_login to False.
    - Redirect the student to their dashboard post-reset.

# 📊 Dashboards
<h2>Admin Dashboard </h2>
1. Route: /admin/dashboard <br>
2. Purpose: Displays an overview of all students. <br>
3. Functionality: <br>
        - Lists all users with the Student role. <br>
        - Provides detailed student information for management purposes. <br>
<h2>Student Dashboard </h2>
1. Route: /student/dashboard <br> 
2. Purpose: A personalized page for students. <br>
3. Functionality: <br>
     - Displays academic details, course information, and notifications. <br>

     
# 🛠️ Admin-Specific Functionalities (CRUD )
1. Create a New Student
   - Route: /admin/create_student
   - Purpose: Allows admins to add new student records.
2. Update Student Records
3. Delete Student Records


<img width="1470" alt="Screenshot 2025-01-12 at 5 49 37 PM" src="https://github.com/user-attachments/assets/0c5349d8-b133-496a-ba96-713c205ecd18" />  <BR>

<img width="1453" alt="Screenshot 2025-01-12 at 5 49 47 PM" src="https://github.com/user-attachments/assets/ab098367-9ad9-493d-a914-286e8417ed92" />
<img width="1470" alt="Screenshot 2025-01-12 at 5 50 18 PM" src="https://github.com/user-attachments/assets/5662ace8-110f-4b5f-9d9d-d237a2906257" />
<img width="1470" alt="Screenshot 2025-01-12 at 5 50 57 PM" src="https://github.com/user-attachments/assets/fb521ffe-85d0-4b95-92c4-dc7750cdbab2" />
<img width="1470" alt="Screenshot 2025-01-12 at 5 51 24 PM" src="https://github.com/user-attachments/assets/6f217915-5c79-4404-a560-217be11f79a2" />
<img width="1063" alt="Screenshot 2025-01-12 at 5 53 25 PM" src="https://github.com/user-attachments/assets/d14af26d-3a3c-44c6-b923-40f518d04c77" />
<img width="1158" alt="Screenshot 2025-01-12 at 5 53 42 PM" src="https://github.com/user-attachments/assets/db058a72-941e-4567-8adc-0a80fafb8fb3" />
<img width="1226" alt="Screenshot 2025-01-12 at 5 53 58 PM" src="https://github.com/user-attachments/assets/1a2e0333-09ab-41d7-b55c-9fff042eeba5" />
<img width="1250" alt="Screenshot 2025-01-12 at 5 55 44 PM" src="https://github.com/user-attachments/assets/b9deaf24-c0af-424a-976c-fa909a44060f" />
<img width="1470" alt="Screenshot 2025-01-12 at 5 57 04 PM" src="https://github.com/user-attachments/assets/be641683-9fc8-4c19-9cbb-7e0a5b1ec7bf" />
<img width="1231" alt="Screenshot 2025-01-12 at 5 57 36 PM" src="https://github.com/user-attachments/assets/6503cb5b-5711-48da-b299-9a0757290232" />
<img width="529" alt="Screenshot 2025-01-12 at 5 58 00 PM" src="https://github.com/user-attachments/assets/fafe68f4-868d-4bc3-a5be-8c341a41fdc2" />













