// script.js

// Confirmation dialog for student deletion (Admin Dashboard)
document.querySelectorAll('a[href^="/delete_student"]').forEach(function (link) {
    link.addEventListener('click', function (event) {
        if (!confirm("Are you sure you want to delete this student?")) {
            event.preventDefault();
        }
    });
});

// Confirmation dialog for logout
document.querySelectorAll('a[href^="/logout"]').forEach(function (link) {
    link.addEventListener('click', function (event) {
        if (!confirm("Are you sure you want to log out?")) {
            event.preventDefault();
        }
    });
});

// Form validation for registration and profile update
document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    
    if (form) {
        form.addEventListener('submit', function (event) {
            const password = document.getElementById('password');
            const confirmPassword = document.getElementById('confirm_password');

            // Validate password match
            if (password && confirmPassword && password.value !== confirmPassword.value) {
                alert("Passwords do not match!");
                event.preventDefault();
            }

            // Additional validation for email format (example)
            const email = document.getElementById('email');
            if (email && !email.value.includes('@')) {
                alert('Please enter a valid email address.');
                event.preventDefault();
            }

            // Example of targeting specific forms (optional, if needed)
            if (form.id === 'register_form') {
                // Additional validation for registration form
            }
        });
    }
});

// Flash message removal (if any)
setTimeout(() => {
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach((msg) => msg.style.display = 'none');
}, 5000);  // hide flash messages after 5 seconds
