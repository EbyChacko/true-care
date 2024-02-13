
// contact page form validation

function validateForm() {
    var name = document.getElementById("name").value;
    var mobile = document.getElementById("mobile").value;
    var email = document.getElementById("email").value;
    var message = document.getElementById("message").value;

    var nameError = document.getElementById("nameError");
    var mobileError = document.getElementById("mobileError");
    var emailError = document.getElementById("emailError");
    var messageError = document.getElementById("messageError");

    // Reset previous error messages
    nameError.innerHTML = "";
    mobileError.innerHTML = "";
    emailError.innerHTML = "";
    messageError.innerHTML = "";

    var isValid = true;

    // Validate Name
    if (name.trim() === "") {
        nameError.innerHTML = "Name is required.";
        isValid = false;
        nameError.style.visibility = "visible";
    }

    // Validate Mobile
    function validateMobileNumber(mobile) {
        var mobileValidations = /^(\+\d{1,3}\s?\d{1,}\s?\d{1,}\s?\d{1,}|\d{10})$/;
        return mobileValidations.test(mobile);
    }
    if (mobile.trim() === "" || !validateMobileNumber(mobile)) {
        mobileError.innerHTML = "Mobile is required and must be a 10 digit number.";
        isValid = false;
        mobileError.style.visibility = "visible";
    }

    // Validate Email
    var emailExtentions = /^[^\s@]+@[^\s@]+\.(com|in|ie|org|net|edu|gov|mil|int|co|uk|us|au|)$/;
    if (email.trim() === "" || !emailExtentions.test(email)) {
        emailError.innerHTML = "Email is required and must be a valid email address.";
        isValid = false;
        emailError.style.visibility = "visible";
    }

    // Validate Message
    if (message.trim() === "") {
        messageError.innerHTML = "Message is required.";
        isValid = false;
        messageError.style.visibility = "visible";
    }

    return isValid;
}


// Update_details form validation
function validateUpdateForm() {
    console.log("inside the validator")
    var name = document.getElementById("name").value;
    var mobile = document.getElementById("mobile").value;
    var email = document.getElementById("email").value;
    var address = document.getElementById("address").value;
    var dateOfBirth = document.getElementById("date_of_birth").value;
    var country = document.getElementById("country").value;
    var zipcode = document.getElementById("zipcode").value;

    var nameError = document.getElementById("nameError");
    var mobileError = document.getElementById("mobileError");
    var emailError = document.getElementById("emailError");
    var addressError = document.getElementById("addressError");
    var dateOfBirthError = document.getElementById("dateOfBirthError");
    var countryError = document.getElementById("countryError");
    var zipcodeError = document.getElementById("zipcodeError");

    // Reset previous error messages
    nameError.innerHTML = "";
    mobileError.innerHTML = "";
    emailError.innerHTML = "";
    addressError.innerHTML = "";
    dateOfBirthError.innerHTML = "";
    countryError.innerHTML = "";
    zipcodeError.innerHTML = "";

    var isValid = true;

    // Validate Name
    if (name.trim() === "") {
        nameError.innerHTML = "Name is required.";
        isValid = false;
        nameError.style.visibility = "visible";
    }

    // Validate Mobile
    function validateMobileNumber(mobile) {
        var mobileValidations = /^(\+\d{1,3}\s?\d{1,}\s?\d{1,}\s?\d{1,}|\d{10})$/;
        return mobileValidations.test(mobile);
    }
    if (mobile.trim() === "" || !validateMobileNumber(mobile)) {
        mobileError.innerHTML = "Mobile is required and must be a 10 digit number.";
        isValid = false;
        mobileError.style.visibility = "visible";
    }

    // Validate Email
    var emailExtentions = /^[^\s@]+@[^\s@]+\.(com|in|ie|org|net|edu|gov|mil|int|co|uk|us|au|)$/;
    if (email.trim() === "" || !emailExtentions.test(email)) {
        emailError.innerHTML = "Email is required and must be a valid email address.";
        isValid = false;
        emailError.style.visibility = "visible";
    }

    // Validate Address
    if (address.trim() === "") {
        addressError.innerHTML = "Address is required.";
        isValid = false;
        addressError.style.visibility = "visible";
    }

    // Validate Date of Birth
    if (dateOfBirth.trim() === "") {
        dateOfBirthError.innerHTML = "Date of Birth is required.";
        isValid = false;
        dateOfBirthError.style.visibility = "visible";
    }

    // Validate Country
    if (country.trim() === "") {
        countryError.innerHTML = "Country is required.";
        isValid = false;
        countryError.style.visibility = "visible";
    }

    // Validate Zip Code
    if (zipcode.trim() === "") {
        zipcodeError.innerHTML = "Zip Code is required.";
        isValid = false;
        zipcodeError.style.visibility = "visible";
    }

    return isValid;
}


function validateAppointmentForm(){
    print("from the validate appointment function")
}


document.getElementById('photo-input').addEventListener('change', function(event) {
    var input = event.target;
    if (input.files && input.files[0]) {
        if (input.files[0].size <= 10485760) {  // Maximum size in bytes (10 MB)
            var reader = new FileReader();
            reader.onload = function(e) {
                document.getElementById('profile-image').src = e.target.result;
            };
            reader.readAsDataURL(input.files[0]);
        } else {
            // Reset the input field to prevent uploading large files
            input.value = '';
            alert('File size too large. Maximum is 10 MB.');
        }
        var reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('profile-image').src = e.target.result;
        };
        reader.readAsDataURL(input.files[0]);
    }
});


$(document).ready(function() {
    $('#departments').change(function() {
        var departmentId = $(this).val();
        if (departmentId) {
            $.ajax({
                type: 'GET',
                url: '/get_doctors/',  // URL to fetch doctors for the selected department
                data: {'department_id': departmentId},
                success: function(data) {
                    $('#doctor').html(data);
                }
            });
        } else {
            $('#doctor').html('<option value="">Select Doctor...</option>');
        }
    });
});