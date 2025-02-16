function deleteNote(noteId) {
    fetch("/delete-note", {
      method: "POST",
      body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
      window.location.href = "/";
    });
  }

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
  .then(response => response.json())
  .then(data => {
      if (data.success) {
          alert("Note deleted successfully!");
          window.location.href = "/";
      } else {
          alert("Error: " + data.message);
      }
  })
  .catch(error => {
      console.error("Error deleting note:", error);
  });
}
function addProduct(isAdmin) {
  alert("Adding product...");

  fetch("/add-product", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ isAdmin: isAdmin })
  })
  .then(response => response.json())
  .then(data => {
    alert(data.message); // Show the response message
    if (data.success) {
      window.location.href = "/";
    }
  })
  .catch(error => {
    console.error("Error:", error);
  });
}


function addProduct2(isAdmin) {
  if (!isAdmin) {
    alert("You do not have permission to add a product.");
    return;
  }

  alert("Adding product...");

  fetch("/add-product", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ isAdmin: isAdmin })
  })
  .then(response => response.json())
  .then(data => {
    alert(data.message); // Show the response message
    if (data.success) {
      window.location.href = "/";
    }
  })
  .catch(error => {
    console.error("Error:", error);
  });
}