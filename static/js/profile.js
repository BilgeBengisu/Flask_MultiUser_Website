//**** */ Profile Picture Upload

// Trigger file input when profile picture is clicked
document.addEventListener("DOMContentLoaded", function () {
    const profilePicInput = document.getElementById("profile-pic-input");
    const uploadForm = document.getElementById("upload-form");

    profilePicInput.addEventListener("change", function () {
        if (profilePicInput.files.length > 0) {
            uploadForm.submit(); // Auto-submit when a file is selected
        }
    });
});

// ****** //