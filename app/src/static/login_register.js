document.getElementById('login-form-submit').addEventListener('click', (event) => {
    event.preventDefault()
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value.trim();
    console.log("handling login")
    if (username === '' || password === '') {
        alert('Please enter both username and password.')
    } else {
        const data = {
            username: username,
            password: password
        };
        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        }).then(
            (response) => response.json()
        ).then(
            (response) => {
                if (response.auth) {
                    alert("login successful");
                } else {
                    alert("login failure");
                }
            }
        )
    }
});

document.getElementById('register-form-submit').addEventListener('click', (event) => {
    event.preventDefault()
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value.trim();
    const confirmPassword = document.getElementById('confirm-password').value.trim();
    console.log("handling register")
    if (password !== confirmPassword) {
        
        alert("Passwords don't match! Please re-enter password.") 
    } else if (username === '' || password === '' || confirmPassword === '') {
        alert('Please enter both username and password.')
    } else {
        const data = {
            username: username,
            password: password
        };
        fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        }).then(
            (response) => response.json()
        ).then(
            (response) => {
                if (response.auth) {
                    alert("registration successful");
                } else {
                    alert("registration failure");
                }
            }
        )
    }
});