/* =========================================================
   DRIVESHARE
   CUSTOMER PROFILE VALIDATION
========================================================= */

document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("customerProfileForm");

    if (!form) {
        return;
    }


    /* =====================================================
       GET FORM ELEMENTS
    ===================================================== */

    const address = document.getElementById("id_address");

    const dob = document.getElementById("id_date_of_birth");

    const aadhaar = document.getElementById("id_aadhaar_number");

    const aadhaarPhoto =
        document.getElementById("id_aadhaar_photo");

    const license =
        document.getElementById("id_driving_license_number");

    const licensePhoto =
        document.getElementById("id_driving_license_photo");

    const emergency =
        document.getElementById("id_emergency_contact");

    const profilePicture =
        document.getElementById("id_profile_picture");


    /* =====================================================
       CONSTANTS
    ===================================================== */

    const allowedImageTypes = [
        "image/jpeg",
        "image/png",
        "image/jpg"
    ];

    const maxFileSize = 5 * 1024 * 1024;


    /* =====================================================
       ERROR HELPERS
    ===================================================== */

    function showError(input, errorId, message) {

        if (input) {

            input.classList.add("input-error");
            input.classList.remove("input-success");
        }

        const error =
            document.getElementById(errorId);

        if (error) {

            error.textContent = message;
            error.classList.add("show");
        }

        return false;
    }


    function showSuccess(input, errorId) {

        if (input) {

            input.classList.remove("input-error");
            input.classList.add("input-success");
        }

        const error =
            document.getElementById(errorId);

        if (error) {

            error.textContent = "";
            error.classList.remove("show");
        }

        return true;
    }


    function clearValidation(input, errorId) {

        if (input) {

            input.classList.remove("input-error");
            input.classList.remove("input-success");
        }

        const error =
            document.getElementById(errorId);

        if (error) {

            error.textContent = "";
            error.classList.remove("show");
        }
    }


    /* =====================================================
       ADDRESS VALIDATION
    ===================================================== */

    function validateAddress() {

        if (!address) {
            return true;
        }

        const value =
            address.value.trim();


        if (value === "") {

            return showError(
                address,
                "addressError",
                "Please enter your address."
            );
        }


        if (value.length < 10) {

            return showError(
                address,
                "addressError",
                "Address must contain at least 10 characters."
            );
        }


        return showSuccess(
            address,
            "addressError"
        );
    }


    /* =====================================================
       DATE OF BIRTH VALIDATION
    ===================================================== */

    function validateDOB() {

        if (!dob) {
            return true;
        }

        const value = dob.value;


        if (!value) {

            return showError(
                dob,
                "dobError",
                "Please select your date of birth."
            );
        }


        const birthDate =
            new Date(value);

        const today =
            new Date();


        if (isNaN(birthDate.getTime())) {

            return showError(
                dob,
                "dobError",
                "Please enter a valid date of birth."
            );
        }


        if (birthDate > today) {

            return showError(
                dob,
                "dobError",
                "Date of birth cannot be in the future."
            );
        }


        let age =
            today.getFullYear() -
            birthDate.getFullYear();


        const monthDifference =
            today.getMonth() -
            birthDate.getMonth();


        if (
            monthDifference < 0 ||
            (
                monthDifference === 0 &&
                today.getDate() < birthDate.getDate()
            )
        ) {

            age--;
        }


        if (age < 18) {

            return showError(
                dob,
                "dobError",
                "You must be at least 18 years old."
            );
        }


        if (age > 100) {

            return showError(
                dob,
                "dobError",
                "Please enter a valid date of birth."
            );
        }


        return showSuccess(
            dob,
            "dobError"
        );
    }


    /* =====================================================
       AADHAAR VALIDATION
    ===================================================== */

    function validateAadhaar() {

        if (!aadhaar) {
            return true;
        }


        const value =
            aadhaar.value
                .replace(/\s/g, "")
                .trim();


        if (value === "") {

            return showError(
                aadhaar,
                "aadhaarError",
                "Please enter your Aadhaar number."
            );
        }


        if (!/^\d{12}$/.test(value)) {

            return showError(
                aadhaar,
                "aadhaarError",
                "Aadhaar number must contain exactly 12 digits."
            );
        }


        /*
         * Prevent obvious invalid values such as:
         * 000000000000
         * 111111111111
         */

        if (/^(\d)\1{11}$/.test(value)) {

            return showError(
                aadhaar,
                "aadhaarError",
                "Please enter a valid Aadhaar number."
            );
        }


        return showSuccess(
            aadhaar,
            "aadhaarError"
        );
    }


    /* =====================================================
       DRIVING LICENCE VALIDATION
    ===================================================== */

    function validateLicense() {

        if (!license) {
            return true;
        }


        const value =
            license.value
                .trim()
                .toUpperCase();


        if (value === "") {

            return showError(
                license,
                "licenseError",
                "Please enter your driving licence number."
            );
        }


        /*
         * General Indian driving licence format.
         *
         * Examples:
         * KA0120230001234
         * DL1420110012345
         * MH12-20230012345
         */

        if (!/^[A-Z0-9-]{8,20}$/.test(value)) {

            return showError(
                license,
                "licenseError",
                "Enter a valid driving licence number."
            );
        }


        return showSuccess(
            license,
            "licenseError"
        );
    }


    /* =====================================================
       EMERGENCY CONTACT VALIDATION
    ===================================================== */

    function validateEmergency() {

        if (!emergency) {
            return true;
        }


        const value =
            emergency.value
                .replace(/\D/g, "")
                .trim();


        if (value === "") {

            return showError(
                emergency,
                "emergencyError",
                "Please enter an emergency contact number."
            );
        }


        if (!/^[6-9]\d{9}$/.test(value)) {

            return showError(
                emergency,
                "emergencyError",
                "Enter a valid 10-digit Indian mobile number."
            );
        }


        return showSuccess(
            emergency,
            "emergencyError"
        );
    }


    /* =====================================================
       FILE VALIDATION
    ===================================================== */

    function validateFile(
        input,
        errorId,
        required,
        fieldName
    ) {

        if (!input) {

            return !required;
        }


        if (
            !input.files ||
            input.files.length === 0
        ) {

            if (required) {

                return showError(
                    null,
                    errorId,
                    "Please upload " + fieldName + "."
                );
            }

            clearValidation(
                null,
                errorId
            );

            return true;
        }


        const file =
            input.files[0];


        if (!allowedImageTypes.includes(file.type)) {

            return showError(
                null,
                errorId,
                "Only JPG, JPEG and PNG images are allowed."
            );
        }


        if (file.size > maxFileSize) {

            return showError(
                null,
                errorId,
                "Image size must be less than 5MB."
            );
        }


        clearValidation(
            null,
            errorId
        );


        return true;
    }


    /* =====================================================
       PROFILE PICTURE
    ===================================================== */

    if (profilePicture) {

        profilePicture.addEventListener(
            "change",
            function () {

                const file =
                    this.files[0];


                if (!file) {

                    clearValidation(
                        null,
                        "profilePictureError"
                    );

                    updateProgress();

                    return;
                }


                const valid =
                    validateFile(
                        profilePicture,
                        "profilePictureError",
                        false,
                        "your profile picture"
                    );


                if (!valid) {

                    this.value = "";

                    const preview =
                        document.getElementById(
                            "profilePreview"
                        );

                    if (preview) {

                        preview.src =
                            "/static/images/default-profile.png";
                    }

                    updateProgress();

                    return;
                }


                const reader =
                    new FileReader();


                reader.onload =
                    function (event) {

                        const preview =
                            document.getElementById(
                                "profilePreview"
                            );

                        if (preview) {

                            preview.src =
                                event.target.result;
                        }
                    };


                reader.readAsDataURL(file);


                updateProgress();
            }
        );
    }


    /* =====================================================
       AADHAAR PHOTO
    ===================================================== */

    if (aadhaarPhoto) {

        aadhaarPhoto.addEventListener(
            "change",
            function () {

                const valid =
                    validateFile(
                        aadhaarPhoto,
                        "aadhaarPhotoError",
                        true,
                        "your Aadhaar photo"
                    );


                const wrapper =
                    this.closest(".file-wrapper");


                if (wrapper) {

                    wrapper.classList.toggle(
                        "file-selected",
                        valid &&
                        this.files.length > 0
                    );
                }


                const fileText =
                    document.getElementById(
                        "aadhaarFileText"
                    );


                if (
                    valid &&
                    this.files.length > 0 &&
                    fileText
                ) {

                    fileText.textContent =
                        this.files[0].name;
                }


                updateProgress();
            }
        );
    }


    /* =====================================================
       DRIVING LICENCE PHOTO
    ===================================================== */

    if (licensePhoto) {

        licensePhoto.addEventListener(
            "change",
            function () {

                const valid =
                    validateFile(
                        licensePhoto,
                        "licensePhotoError",
                        true,
                        "your driving licence photo"
                    );


                const wrapper =
                    this.closest(".file-wrapper");


                if (wrapper) {

                    wrapper.classList.toggle(
                        "file-selected",
                        valid &&
                        this.files.length > 0
                    );
                }


                const fileText =
                    document.getElementById(
                        "licenseFileText"
                    );


                if (
                    valid &&
                    this.files.length > 0 &&
                    fileText
                ) {

                    fileText.textContent =
                        this.files[0].name;
                }


                updateProgress();
            }
        );
    }


    /* =====================================================
       LIVE INPUT VALIDATION
    ===================================================== */

    if (address) {

        address.addEventListener(
            "input",
            function () {

                validateAddress();
                updateProgress();
            }
        );
    }


    if (dob) {

        dob.addEventListener(
            "change",
            function () {

                validateDOB();
                updateProgress();
            }
        );
    }


    if (aadhaar) {

        aadhaar.addEventListener(
            "input",
            function () {

                /*
                 * Allow only digits.
                 */

                this.value =
                    this.value
                        .replace(/\D/g, "")
                        .slice(0, 12);


                validateAadhaar();
                updateProgress();
            }
        );
    }


    if (license) {

        license.addEventListener(
            "input",
            function () {

                this.value =
                    this.value
                        .toUpperCase()
                        .replace(/[^A-Z0-9-]/g, "")
                        .slice(0, 20);


                validateLicense();
                updateProgress();
            }
        );
    }


    if (emergency) {

        emergency.addEventListener(
            "input",
            function () {

                this.value =
                    this.value
                        .replace(/\D/g, "")
                        .slice(0, 10);


                validateEmergency();
                updateProgress();
            }
        );
    }


    /* =====================================================
       PROGRESS CALCULATION
    ===================================================== */

    function updateProgress() {

        const fields = [
            address,
            dob,
            emergency,
            aadhaar,
            license,
            aadhaarPhoto,
            licensePhoto
        ];


        let completed = 0;


        fields.forEach(function (field) {

            if (!field) {
                return;
            }


            if (
                field.type === "file"
            ) {

                if (
                    field.files &&
                    field.files.length > 0
                ) {

                    const file =
                        field.files[0];

                    if (
                        allowedImageTypes.includes(file.type) &&
                        file.size <= maxFileSize
                    ) {

                        completed++;
                    }
                }

            } else {

                if (
                    field.value &&
                    field.value.trim() !== ""
                ) {

                    completed++;
                }
            }

        });


        const percentage =
            Math.round(
                (completed / fields.length) * 100
            );


        const progressPercent =
            document.getElementById(
                "progressPercent"
            );

        const progressBar =
            document.getElementById(
                "progressBar"
            );


        if (progressPercent) {

            progressPercent.textContent =
                percentage + "%";
        }


        if (progressBar) {

            progressBar.style.width =
                percentage + "%";
        }
    }


    /* =====================================================
       FORM SUBMIT VALIDATION
    ===================================================== */

    form.addEventListener(
        "submit",
        function (event) {

            /*
             * Run every validation function.
             */

            const addressValid =
                validateAddress();

            const dobValid =
                validateDOB();

            const emergencyValid =
                validateEmergency();

            const aadhaarValid =
                validateAadhaar();

            const licenseValid =
                validateLicense();

            const aadhaarPhotoValid =
                validateFile(
                    aadhaarPhoto,
                    "aadhaarPhotoError",
                    true,
                    "your Aadhaar photo"
                );

            const licensePhotoValid =
                validateFile(
                    licensePhoto,
                    "licensePhotoError",
                    true,
                    "your driving licence photo"
                );


            const allValid =
                addressValid &&
                dobValid &&
                emergencyValid &&
                aadhaarValid &&
                licenseValid &&
                aadhaarPhotoValid &&
                licensePhotoValid;


            /* =============================================
               INVALID
            ============================================= */

            if (!allValid) {

                event.preventDefault();


                /*
                 * Alert message when something is missed.
                 */

                alert(
                    "Please complete all required fields correctly before saving your DriveShare profile."
                );


                /*
                 * Find first invalid field.
                 */

                const firstError =
                    form.querySelector(
                        ".input-error"
                    );


                if (firstError) {

                    firstError.scrollIntoView({
                        behavior: "smooth",
                        block: "center"
                    });


                    setTimeout(
                        function () {

                            firstError.focus();

                        },
                        400
                    );
                }


                updateProgress();

                return;
            }


            /* =============================================
               VALID
            ============================================= */

            const submitBtn =
                document.getElementById(
                    "submitBtn"
                );


            if (submitBtn) {

                submitBtn.classList.add(
                    "loading"
                );

                submitBtn.disabled = true;
            }

        }
    );


    /* =====================================================
       INITIALIZATION
    ===================================================== */

    updateProgress();

});