function updateProperty() {
    const photo_update_button = document.getElementById('update_button');
    const fileInput = document.getElementById('photo'); const new_file = fileInput.files[0]; // Get the selected file
    console.log(new_file)
    if (!new_file) { alert('Please select a file.'); return; }
    if (!['image/png', 'image/jpg', 'image/jpeg'].includes(new_file.type)) { alert('Invalid file type. Please upload PNG, JPG or JPEG file.'); return; }
    if (new_file.size > 5 * 1024 * 1024) { alert('File is too large. Maximum size is 5 MB.'); return;}
    const data = {'property': 'fotka', 'file': new_file}
    console.log(data)
    fetch('/update_photo', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body:  JSON.stringify({data})
    })
    .then(response => response.json())
    .then(data => { if (data.success) { alert(data.message);} else { alert("Failed: " + data.message); } })
    .catch(error => {console.error("Error:", error);});
}