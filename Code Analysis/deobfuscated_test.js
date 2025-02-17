fetch("/delete-note2", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({ noteId: noteId })
})