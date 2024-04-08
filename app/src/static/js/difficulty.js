document.getElementById('difficulty-submit-btn').addEventListener('click', (event) => {
    event.preventDefault()
    const difficulty = parseInt(document.getElementById("difficulty").value);
    
    const data = {
        "difficulty": difficulty
    }

    fetch('/difficulty', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then(
        (response) => response.json()
    ).then(
        (response) => {
            if (response.success) {
                console.log("changed difficulty")
            } else {
                console.log("failed to change difficulty")
            }
        }
    )
});