// Initialize Supabase client
const supabaseUrl = 'https://tijevatcuxldctpwwflh.supabase.co';
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRpamV2YXRjdXhsZGN0cHd3ZmxoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjgxMTM1NzksImV4cCI6MjA0MzY4OTU3OX0.KZiGvJK7jEYrxOIohAHxHey24iZCGd11o2eHqk4OMfg';
const supabase = supabase.createClient(supabaseUrl, supabaseKey);

// Signup functionality
if (document.getElementById('signup-button')) {
    document.getElementById('signup-button').addEventListener('click', async () => {
        const email = document.getElementById('email').value;
        const age = document.getElementById('age').value;
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirm-password').value;
        const errorMessage = document.getElementById('error-message');

        errorMessage.textContent = ''; // Clear any previous error messages

        if (password !== confirmPassword) {
            errorMessage.textContent = "Passwords do not match";
            return;
        }

        try {
            const { user, error } = await supabase.auth.signUp({
                email: email,
                password: password,
            });

            if (error) throw error;

            // Add additional user data to a custom table
            const { data, error: profileError } = await supabase
                .from('profiles')
                .insert([{ user_id: user.id, age: age }]);

            if (profileError) throw profileError;

            alert('Signup successful! Please check your email to verify your account.');
            window.location.href = 'login.html'; // Redirect to login page
        } catch (error) {
            errorMessage.textContent = error.message;
        }
    });
}

// Login functionality
if (document.getElementById('login-button')) {
    document.getElementById('login-button').addEventListener('click', async () => {
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const errorMessage = document.getElementById('error-message');

        errorMessage.textContent = ''; // Clear any previous error messages

        try {
            const { user, error } = await supabase.auth.signIn({
                email: email,
                password: password,
            });

            if (error) throw error;

            alert('Login successful!');
            window.location.href = 'index.html'; // Redirect to main page
        } catch (error) {
            errorMessage.textContent = error.message;
        }
    });
}

// Check authentication status on page load
window.addEventListener('DOMContentLoaded', async () => {
    const { data: { user } } = await supabase.auth.getUser();
    if (user && window.location.pathname.includes('login.html')) {
        // If user is already logged in and on login page, redirect to index.html
        window.location.href = 'index.html';
    } else if (!user && window.location.pathname.includes('index.html')) {
        // If user is not logged in and on index.html, redirect to login page
        window.location.href = 'login.html';
    }
});