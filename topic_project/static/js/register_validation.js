// js code to check if usernames and emails are already in the database
// and valid and then to make sure the password added is
// of a high enough complexity and that both match.

console.log('Register validation script loaded');
document.addEventListener('DOMContentLoaded', function() {

    const usernameInput = document.getElementById('id_username');
    const emailInput = document.getElementById('id_email');
    const passwordInput = document.getElementById('id_password');
    const confirmPasswordInput = document.getElementById('confirm_password');
    const submitBtn = document.getElementById('submit-btn');
    
    let usernameValid = false;
    let emailValid = false;
    let passwordValid = false;
    let passwordsMatch = false;
    submitBtn.disabled = true;

    let usernameTimeout;
    let emailTimeout;

    usernameInput.addEventListener('input', function() {
        const username = this.value;
        const usernameValidation = document.getElementById('username-validation');
        const usernameSuccess = document.getElementById('username-success');
        const usernameChecking = document.getElementById('username-checking');
        
        usernameValidation.textContent = '';
        usernameSuccess.textContent = '';
        this.classList.remove('input-error', 'input-success');
        
        if (username.length < 3) {
            usernameValidation.textContent = 'Username must be at least 3 characters long';
            this.classList.add('input-error');
            usernameValid = false;
            usernameChecking.textContent = '';
        } else if (!/^[a-zA-Z0-9_]+$/.test(username)) {
            usernameValidation.textContent = 'Username can only contain letters, numbers, and underscores';
            this.classList.add('input-error');
            usernameValid = false;
            usernameChecking.textContent = '';
        } else {
            usernameChecking.textContent = 'Checking availability...';
            
            clearTimeout(usernameTimeout);
            
            usernameTimeout = setTimeout(() => {
                fetch(`/topic/register/check-username?username=${encodeURIComponent(username)}`)
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Network response was not ok');
                        }
                        return response.json();
                    })
                    .then(data => {
                        usernameChecking.textContent = '';
                        if (data.available) {
                            usernameSuccess.textContent = '✓ Username available';
                            this.classList.add('input-success');
                            usernameValid = true;
                        } else {
                            usernameValidation.textContent = 'This username is already taken';
                            this.classList.add('input-error');
                            usernameValid = false;
                        }
                        updateSubmitButton();
                    })
                    .catch(error => {
                        console.error('Error checking username:', error);
                        usernameChecking.textContent = '';
                        usernameValid = true;
                        updateSubmitButton();
                    });
            }, 300);
        }
        updateSubmitButton();
    });

    emailInput.addEventListener('input', function() {
        const email = this.value;
        const emailValidation = document.getElementById('email-validation');
        const emailSuccess = document.getElementById('email-success');
        const emailChecking = document.getElementById('email-checking');
        
        emailValidation.textContent = '';
        emailSuccess.textContent = '';
        this.classList.remove('input-error', 'input-success');
        
        const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        
        if (!emailPattern.test(email)) {
            emailValidation.textContent = 'Please enter a valid email address';
            this.classList.add('input-error');
            emailValid = false;
            emailChecking.textContent = '';
        } else {
            emailChecking.textContent = 'Checking availability...';
            
            clearTimeout(emailTimeout);
            
            emailTimeout = setTimeout(() => {
                fetch(`/topic/register/check-email?email=${encodeURIComponent(email)}`)
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Network response was not ok');
                        }
                        return response.json();
                    })
                    .then(data => {
                        emailChecking.textContent = '';
                        if (data.available) {
                            emailSuccess.textContent = '✓ Email available';
                            this.classList.add('input-success');
                            emailValid = true;
                        } else {
                            emailValidation.textContent = 'This email is already registered';
                            this.classList.add('input-error');
                            emailValid = false;
                        }
                        updateSubmitButton();
                    })
                    .catch(error => {
                        console.error('Error checking email:', error);
                        emailChecking.textContent = '';
                        emailValid = true;
                        updateSubmitButton();
                    });
            }, 300);
        }
        updateSubmitButton();
    });

    passwordInput.addEventListener('input', function() {
        const password = this.value;
        
        const hasLength = password.length >= 8;
        const hasUppercase = /[A-Z]/.test(password);
        const hasLowercase = /[a-z]/.test(password);
        const hasNumber = /[0-9]/.test(password);
        const hasSpecial = /[!@#$%^&*(),.?":{}|<>]/.test(password);

        const reqLength = document.getElementById('req-length');
        const reqUppercase = document.getElementById('req-uppercase');
        const reqLowercase = document.getElementById('req-lowercase');
        const reqNumber = document.getElementById('req-number');
        const reqSpecial = document.getElementById('req-special');
    
        console.log('Updating password requirements:', {
            hasLength, hasUppercase, hasLowercase, hasNumber, hasSpecial
        });
        
        if (hasLength) {
            reqLength.className = 'valid';
            reqLength.innerHTML = '✓ At least 8 characters';
        } else {
            reqLength.className = 'invalid';
            reqLength.innerHTML = '✗ At least 8 characters';
        }
        
        if (hasUppercase) {
            reqUppercase.className = 'valid';
            reqUppercase.innerHTML = '✓ At least one uppercase letter';
        } else {
            reqUppercase.className = 'invalid';
            reqUppercase.innerHTML = '✗ At least one uppercase letter';
        }
        
        if (hasLowercase) {
            reqLowercase.className = 'valid';
            reqLowercase.innerHTML = '✓ At least one lowercase letter';
        } else {
            reqLowercase.className = 'invalid';
            reqLowercase.innerHTML = '✗ At least one lowercase letter';
        }
        
        if (hasNumber) {
            reqNumber.className = 'valid';
            reqNumber.innerHTML = '✓ At least one number';
        } else {
            reqNumber.className = 'invalid';
            reqNumber.innerHTML = '✗ At least one number';
        }
        
        if (hasSpecial) {
            reqSpecial.className = 'valid';
            reqSpecial.innerHTML = '✓ At least one special character (!@#$%^&*)';
        } else {
            reqSpecial.className = 'invalid';
            reqSpecial.innerHTML = '✗ At least one special character (!@#$%^&*)';
        }
        

        const strengthBar = document.getElementById('password-strength');
        const requirementsMet = [hasLength, hasUppercase, hasLowercase, hasNumber, hasSpecial];
        const metCount = requirementsMet.filter(Boolean).length;
        
        strengthBar.className = '';
        if (metCount <= 2) {
            strengthBar.classList.add('strength-weak');
        } else if (metCount === 3) {
            strengthBar.classList.add('strength-fair');
        } else if (metCount === 4) {
            strengthBar.classList.add('strength-good');
        } else if (metCount === 5) {
            strengthBar.classList.add('strength-strong');
        }
        
        passwordValid = hasLength && hasUppercase && hasLowercase && hasNumber && hasSpecial;
        checkPasswordsMatch();
        updateSubmitButton();
    });

    confirmPasswordInput.addEventListener('input', checkPasswordsMatch);
    
    function checkPasswordsMatch() {
        const passwordMatch = document.getElementById('password-match');
        if (passwordInput.value !== confirmPasswordInput.value) {
            passwordMatch.textContent = 'Passwords do not match';
            passwordsMatch = false;
        } else if (passwordInput.value.length > 0 && confirmPasswordInput.value.length > 0) {
            passwordMatch.textContent = '✓ Passwords match';
            passwordMatch.style.color = '#28a745';
            passwordsMatch = true;
        } else {
            passwordMatch.textContent = '';
            passwordsMatch = false;
        }
        updateSubmitButton();
    }

    function updateSubmitButton() {
        submitBtn.disabled = !(usernameValid && emailValid && passwordValid && passwordsMatch);
    }


    document.getElementById('user_form').addEventListener('submit', function(e) {
        const isUsernameValid = usernameInput.classList.contains('input-success');
        const isEmailValid = emailInput.classList.contains('input-success');
        

        const password = passwordInput.value;
        const hasLength = password.length >= 8;
        const hasUppercase = /[A-Z]/.test(password);
        const hasLowercase = /[a-z]/.test(password);
        const hasNumber = /[0-9]/.test(password);
        const hasSpecial = /[!@#$%^&*(),.?":{}|<>]/.test(password);
        const isPasswordValid = hasLength && hasUppercase && hasLowercase && hasNumber && hasSpecial;
        
        const doPasswordsMatch = password === confirmPasswordInput.value && password.length > 0;
        
        if (!isUsernameValid || !isEmailValid || !isPasswordValid || !doPasswordsMatch) {
            e.preventDefault();
            e.stopPropagation();
            
            let errors = [];
            if (!isUsernameValid) errors.push("• Username is invalid or already taken");
            if (!isEmailValid) errors.push("• Email is invalid or already registered");
            if (!isPasswordValid) errors.push("• Password does not meet complexity requirements");
            if (!doPasswordsMatch) errors.push("• Passwords do not match");
            
            alert("Please fix the following errors:\n" + errors.join("\n"));
            return false;
        }
        
        console.log("Form validation passed, submitting...");
        return true;
    });
});