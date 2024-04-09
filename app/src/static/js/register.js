document
  .getElementById("register-form-submit")
  .addEventListener("click", (event) => {
    event.preventDefault();
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();
    const confirmPassword = document
      .getElementById("confirm-password")
      .value.trim();
    console.log("handling register");

    if (username === "" || password === "" || confirmPassword === "") {
      alert("Please fill in all the fields.");
      return;
    }

    if (password !== confirmPassword) {
      alert("Passwords don't match! Please re-enter password.");
      return;
    }

    const data = {
      username: username,
      password: password,
    };

    console.log(data);

    fetch("/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
  });
