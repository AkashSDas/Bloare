// *** Displaying edit user details form *** 
editUserBtn = document.querySelector(".edit-details-btn");
editUserBtn.addEventListener('click', () => {
    form = document.getElementsByClassName('details-update-form')[0];
    form.style.display = "block";
});

// *** Displaying edit user profile form *** 
editProfileBtn = document.querySelector(".edit-img-btn");
editProfileBtn.addEventListener('click', () => {
    form = document.getElementsByClassName('img-update-form')[0];
    form.style.display = "block";
});
