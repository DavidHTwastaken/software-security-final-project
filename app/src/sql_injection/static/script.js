document.getElementById("submit-btn").addEventListener("click", (event) => {
  let answer = document.getElementById("answer").textContent;
  if (answer === null) {
    return;
  }
  fetch("/sqli/submit", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ answer: answer }),
  })
    .then((res) => res.json())
    .then((res) => {
      if (res["success"]) {
        alert("Success!");
      }
    });
});

document.getElementById("answer").addEventListener("keypress", (event) => {
  if (event.key === "Enter") {
    // Cancel the default action
    event.preventDefault();
    // Trigger the button element with a click
    document.getElementById("submit-btn").click();
  }
});

document.getElementById("query").addEventListener("keypress", (event) => {
  if (event.key === "Enter") {
    // Cancel the default action
    event.preventDefault();
    // Trigger the button element with a click
    document.getElementById("search-btn").click();
  }
});
