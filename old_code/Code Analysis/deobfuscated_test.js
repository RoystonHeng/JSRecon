function deleteNote2(noteId, userId, currentUserId, isAdmin) {
    // Step 1: Validate Note ID
    if (!noteId || typeof noteId !== "number") {
        alert("Invalid note ID.");
        return;
     }
  
    // Step 2: Validate User Permissions
    if (userId !== currentUserId) {
        alert("You do not have permission to delete this note.");
        return;
    }
  
    // Step 3: Send the request to delete the note
    fetch("/delete-note2", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ noteId: noteId })
    })
    
  }