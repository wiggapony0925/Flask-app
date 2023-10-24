function deleteNote(noteId) {
    fetch('/vending_machine/<int:machine_id>/notes/<int:note_id>/delete', {
        method: 'POST',
        body : JSON.stringify({noteId: noteId}),
    }).then((_res) => {
        window.location.href = "/vending_machine_dashboard/<int:machine_id>'"
    })
}