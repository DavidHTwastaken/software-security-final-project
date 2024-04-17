function submitAnswer(endpoint) {
  const answerInput = document.getElementById("answer");
  let answer = answerInput.value;
  if (answer === null) {
    return;
  }
  fetch(endpoint, {
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
      } else {
        alert("Incorrect solution");
      }
      answerInput.textContent = null;
    });
}

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
