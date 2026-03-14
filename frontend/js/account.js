const accountForm = document.getElementById("account-form");
const nameInput = document.getElementById("name");
const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");
const successMessage = document.getElementById("success-message");

function getCurrentUser() {
    const savedUser = localStorage.getItem("currentUser");

    if (!savedUser) {
        return null;
    }

    return JSON.parse(savedUser);
}

function loadUserDetails() {
    const currentUser = getCurrentUser();

    if (!currentUser) {
        return;
    }

    if (currentUser.name) {
        nameInput.value = currentUser.name;
    }

    if (currentUser.email) {
        emailInput.value = currentUser.email;
    }
}

accountForm.addEventListener("sumbit", function(event) {
    event.preventDefault();

    const currentUser = getCurrentUser();

    if (!currentUser) {
        alert("No user is logged in.");
        return;
    }

    const updatedUser = {
        ...currentUser,
        name: nameInput.value,
        email: emailInput.value,
        password: passwordInput.value
    };

    localStorage.setItem("currentUser", JSON.stringify(updatedUser));

    successMessage.style.display = "block";
});

loadUserDetails();
