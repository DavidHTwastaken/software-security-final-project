document.getElementById('loginForm').addEventListener('submit', function(event) {
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value.trim();

    if (username === '' || password === '') {
        event.preventDefault();
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