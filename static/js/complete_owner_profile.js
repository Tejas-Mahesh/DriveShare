/* =========================================================
   DRIVESHARE OWNER PROFILE
   CREATE + EDIT VALIDATION
========================================================= */

document.addEventListener("DOMContentLoaded", function () {

    const form =
        document.getElementById("ownerProfileForm");

    if (!form) {
        return;
    }


    /* =====================================================
       EDIT MODE
    ===================================================== */

    const isEditing =
        form.dataset.editing === "true";


    /* =====================================================
       GET ELEMENTS
    ===================================================== */

    const profilePicture =
        document.getElementById("id_profile_picture");

    const address =
        document.getElementById("id_address");

    const aadhaar =
        document.getElementById("id_aadhaar_number");

    const aadhaarPhoto =
        document.getElementById("id_aadhaar_photo");

    const drivingLicense =
        document.getElementById(
            "id_driving_license_number"
        );

    const drivingLicensePhoto =
        document.getElementById(
            "id_driving_license_photo"
        );

    const pan =
        document.getElementById("id_pan_number");

    const bankAccount =
        document.getElementById("id_bank_account");

    const ifsc =
        document.getElementById("id_ifsc_code");

    const upi =
        document.getElementById("id_upi_id");


    /* =====================================================
       BUTTON
    ===================================================== */

    const saveButton =
        document.getElementById("saveProfileBtn");

    const buttonText =
        document.getElementById("buttonText");


    /* =====================================================
       PROFILE PREVIEW
    ===================================================== */

    const profilePreview =
        document.getElementById("profilePreview");

    const profileFileName =
        document.getElementById("profileFileName");


    /* =====================================================
       FILE NAMES
    ===================================================== */

    const aadhaarFileName =
        document.getElementById("aadhaarFileName");

    const licenseFileName =
        document.getElementById("licenseFileName");


    /* =====================================================
       ERROR ELEMENTS
    ===================================================== */

    const errors = {

        profilePicture:
            document.getElementById(
                "profilePictureError"
            ),

        address:
            document.getElementById(
                "addressError"
            ),

        aadhaar:
            document.getElementById(
                "aadhaarError"
            ),

        aadhaarPhoto:
            document.getElementById(
                "aadhaarPhotoError"
            ),

        license:
            document.getElementById(
                "licenseError"
            ),

        licensePhoto:
            document.getElementById(
                "licensePhotoError"
            ),

        pan:
            document.getElementById(
                "panError"
            ),

        bank:
            document.getElementById(
                "bankError"
            ),

        ifsc:
            document.getElementById(
                "ifscError"
            ),

        upi:
            document.getElementById(
                "upiError"
            )
    };


    /* =====================================================
       CONSTANTS
    ===================================================== */

    const MAX_FILE_SIZE =
        5 * 1024 * 1024;


    const allowedImageTypes = [

        "image/jpeg",
        "image/jpg",
        "image/png"

    ];


    /* =====================================================
       HELPER
    ===================================================== */

    function clean(value) {

        return value
            ? value.trim()
            : "";
    }


    /* =====================================================
       SHOW ERROR
    ===================================================== */

    function showError(
        input,
        errorElement,
        message
    ) {

        if (input) {

            input.classList.remove(
                "input-success"
            );

            input.classList.add(
                "input-error"
            );
        }


        if (errorElement) {

            errorElement.textContent =
                message;

            errorElement.classList.add(
                "show"
            );
        }

        return false;
    }


    /* =====================================================
       SHOW SUCCESS
    ===================================================== */

    function showSuccess(
        input,
        errorElement
    ) {

        if (input) {

            input.classList.remove(
                "input-error"
            );

            input.classList.add(
                "input-success"
            );
        }


        if (errorElement) {

            errorElement.textContent =
                "";

            errorElement.classList.remove(
                "show"
            );
        }

        return true;
    }


    /* =====================================================
       CLEAR VALIDATION
    ===================================================== */

    function clearValidation(
        input,
        errorElement
    ) {

        if (input) {

            input.classList.remove(
                "input-error",
                "input-success"
            );
        }


        if (errorElement) {

            errorElement.textContent =
                "";

            errorElement.classList.remove(
                "show"
            );
        }
    }


    /* =====================================================
       FILE VALIDATION
       
       CREATE MODE:
       File is required.
       
       EDIT MODE:
       File is optional because old file already exists.
    ===================================================== */

    function validateFile(
        input,
        errorElement,
        fieldName,
        required
    ) {

        if (!input) {
            return false;
        }


        /*
         * No NEW file selected.
         */

        if (
            !input.files ||
            input.files.length === 0
        ) {

            /*
             * CREATE MODE
             */

            if (required) {

                return showError(
                    input,
                    errorElement,
                    fieldName +
                    " is required."
                );
            }


            /*
             * EDIT MODE
             *
             * Existing database file remains.
             */

            clearValidation(
                input,
                errorElement
            );

            return true;
        }


        const file =
            input.files[0];


        /* FILE TYPE */

        if (
            !allowedImageTypes.includes(
                file.type
            )
        ) {

            return showError(
                input,
                errorElement,
                fieldName +
                " must be JPG, JPEG or PNG."
            );
        }


        /* FILE SIZE */

        if (
            file.size >
            MAX_FILE_SIZE
        ) {

            return showError(
                input,
                errorElement,
                fieldName +
                " must be less than 5MB."
            );
        }


        return showSuccess(
            input,
            errorElement
        );
    }


    /* =====================================================
       PROFILE PICTURE
    ===================================================== */

    function validateProfilePicture() {

        return validateFile(

            profilePicture,

            errors.profilePicture,

            "Profile picture",

            !isEditing
        );
    }


    /* =====================================================
       PROFILE PICTURE CHANGE
    ===================================================== */

    if (profilePicture) {

        profilePicture.addEventListener(
            "change",
            function () {

                if (
                    !this.files ||
                    !this.files.length
                ) {
                    return;
                }


                const file =
                    this.files[0];


                if (profileFileName) {

                    profileFileName.textContent =
                        file.name;
                }


                /*
                 * Preview only valid image.
                 */

                if (
                    allowedImageTypes.includes(
                        file.type
                    ) &&
                    file.size <=
                        MAX_FILE_SIZE &&
                    profilePreview
                ) {

                    const reader =
                        new FileReader();


                    reader.onload =
                        function (event) {

                            profilePreview.src =
                                event.target.result;
                        };


                    reader.readAsDataURL(
                        file
                    );
                }


                validateProfilePicture();

                updateProgress();
            }
        );
    }


    /* =====================================================
       ADDRESS
    ===================================================== */

    function validateAddress() {

        if (!address) {
            return false;
        }


        const value =
            clean(address.value);


        if (!value) {

            return showError(
                address,
                errors.address,
                "Address is required."
            );
        }


        if (value.length < 10) {

            return showError(
                address,
                errors.address,
                "Please enter a complete address."
            );
        }


        if (value.length > 500) {

            return showError(
                address,
                errors.address,
                "Address cannot exceed 500 characters."
            );
        }


        return showSuccess(
            address,
            errors.address
        );
    }


    /* =====================================================
       AADHAAR
    ===================================================== */

    function validateAadhaar() {

        if (!aadhaar) {
            return false;
        }


        const value =
            clean(aadhaar.value)
                .replace(/\s/g, "");


        if (!value) {

            return showError(
                aadhaar,
                errors.aadhaar,
                "Aadhaar number is required."
            );
        }


        if (
            !/^\d{12}$/.test(value)
        ) {

            return showError(
                aadhaar,
                errors.aadhaar,
                "Aadhaar number must contain exactly 12 digits."
            );
        }


        return showSuccess(
            aadhaar,
            errors.aadhaar
        );
    }


    /* =====================================================
       AADHAAR PHOTO
    ===================================================== */

    function validateAadhaarPhoto() {

        return validateFile(

            aadhaarPhoto,

            errors.aadhaarPhoto,

            "Aadhaar photo",

            !isEditing
        );
    }


    if (aadhaarPhoto) {

        aadhaarPhoto.addEventListener(
            "change",
            function () {

                if (
                    this.files &&
                    this.files.length &&
                    aadhaarFileName
                ) {

                    aadhaarFileName.textContent =
                        this.files[0].name;
                }


                validateAadhaarPhoto();

                updateProgress();
            }
        );
    }


    /* =====================================================
       DRIVING LICENCE NUMBER
    ===================================================== */

    function validateDrivingLicense() {

        if (!drivingLicense) {
            return false;
        }


        const value =
            clean(drivingLicense.value)
                .toUpperCase()
                .replace(/\s/g, "");


        if (!value) {

            return showError(
                drivingLicense,
                errors.license,
                "Driving Licence number is required."
            );
        }


        const licensePattern =
            /^[A-Z]{2}[0-9A-Z]{10,16}$/;


        if (
            !licensePattern.test(value)
        ) {

            return showError(
                drivingLicense,
                errors.license,
                "Enter a valid Driving Licence number."
            );
        }


        return showSuccess(
            drivingLicense,
            errors.license
        );
    }


    /* =====================================================
       DRIVING LICENCE PHOTO
    ===================================================== */

    function validateDrivingLicensePhoto() {

        return validateFile(

            drivingLicensePhoto,

            errors.licensePhoto,

            "Driving Licence photo",

            !isEditing
        );
    }


    if (drivingLicensePhoto) {

        drivingLicensePhoto.addEventListener(
            "change",
            function () {

                if (
                    this.files &&
                    this.files.length &&
                    licenseFileName
                ) {

                    licenseFileName.textContent =
                        this.files[0].name;
                }


                validateDrivingLicensePhoto();

                updateProgress();
            }
        );
    }


    /* =====================================================
       PAN
    ===================================================== */

    function validatePAN() {

        if (!pan) {
            return false;
        }


        const value =
            clean(pan.value)
                .toUpperCase()
                .replace(/\s/g, "");


        if (!value) {

            return showError(
                pan,
                errors.pan,
                "PAN number is required."
            );
        }


        const panPattern =
            /^[A-Z]{5}[0-9]{4}[A-Z]$/;


        if (
            !panPattern.test(value)
        ) {

            return showError(
                pan,
                errors.pan,
                "Enter a valid PAN number. Example: ABCDE1234F"
            );
        }


        return showSuccess(
            pan,
            errors.pan
        );
    }


    /* =====================================================
       BANK ACCOUNT
    ===================================================== */

    function validateBankAccount() {

        if (!bankAccount) {
            return false;
        }


        const value =
            clean(bankAccount.value)
                .replace(/\s/g, "");


        if (!value) {

            return showError(
                bankAccount,
                errors.bank,
                "Bank account number is required."
            );
        }


        if (
            !/^\d{9,18}$/.test(value)
        ) {

            return showError(
                bankAccount,
                errors.bank,
                "Bank account number must contain 9 to 18 digits."
            );
        }


        return showSuccess(
            bankAccount,
            errors.bank
        );
    }


    /* =====================================================
       IFSC
    ===================================================== */

    function validateIFSC() {

        if (!ifsc) {
            return false;
        }


        const value =
            clean(ifsc.value)
                .toUpperCase()
                .replace(/\s/g, "");


        if (!value) {

            return showError(
                ifsc,
                errors.ifsc,
                "IFSC code is required."
            );
        }


        const ifscPattern =
            /^[A-Z]{4}0[A-Z0-9]{6}$/;


        if (
            !ifscPattern.test(value)
        ) {

            return showError(
                ifsc,
                errors.ifsc,
                "Enter a valid IFSC code. Example: SBIN0001234"
            );
        }


        return showSuccess(
            ifsc,
            errors.ifsc
        );
    }


    /* =====================================================
       UPI
    ===================================================== */

    function validateUPI() {

        if (!upi) {
            return false;
        }


        const value =
            clean(upi.value);


        if (!value) {

            return showError(
                upi,
                errors.upi,
                "UPI ID is required."
            );
        }


        const upiPattern =
            /^[a-zA-Z0-9._-]{2,50}@[a-zA-Z]{2,30}$/;


        if (
            !upiPattern.test(value)
        ) {

            return showError(
                upi,
                errors.upi,
                "Enter a valid UPI ID. Example: yourname@oksbi"
            );
        }


        return showSuccess(
            upi,
            errors.upi
        );
    }


    /* =====================================================
       CHECK EXISTING FILE
       
       This is important for EDIT MODE.
    ===================================================== */

    function hasExistingProfileFile(
        fieldName
    ) {

        /*
         * The Django template tells us through
         * the existing text.
         *
         * If editing and the selected-file
         * area contains "Current..." / "Change...",
         * the database already has a file.
         */

        if (!isEditing) {
            return false;
        }


        if (
            fieldName === "profile"
        ) {

            return (
                profileFileName &&
                profileFileName.textContent.trim() !== ""
            );
        }


        if (
            fieldName === "aadhaar"
        ) {

            return (
                aadhaarFileName &&
                aadhaarFileName.textContent
                    .toLowerCase()
                    .includes("change")
            );
        }


        if (
            fieldName === "license"
        ) {

            return (
                licenseFileName &&
                licenseFileName.textContent
                    .toLowerCase()
                    .includes("change")
            );
        }


        return false;
    }


    /* =====================================================
       PROGRESS
    ===================================================== */

    function updateProgress() {

        const fields = [

            profilePicture,

            address,

            aadhaar,

            aadhaarPhoto,

            drivingLicense,

            drivingLicensePhoto,

            pan,

            bankAccount,

            ifsc,

            upi
        ];


        let totalFields = 0;

        let completed = 0;


        fields.forEach(
            function (element) {

                if (!element) {
                    return;
                }


                totalFields++;


                /*
                 * FILE FIELD
                 */

                if (
                    element.type === "file"
                ) {

                    if (
                        element.files &&
                        element.files.length > 0
                    ) {

                        completed++;

                        return;
                    }


                    /*
                     * Existing files count
                     * during EDIT MODE.
                     */

                    if (
                        isEditing
                    ) {

                        if (
                            element ===
                                profilePicture &&
                            hasExistingProfileFile(
                                "profile"
                            )
                        ) {

                            completed++;

                        } else if (
                            element ===
                                aadhaarPhoto &&
                            hasExistingProfileFile(
                                "aadhaar"
                            )
                        ) {

                            completed++;

                        } else if (
                            element ===
                                drivingLicensePhoto &&
                            hasExistingProfileFile(
                                "license"
                            )
                        ) {

                            completed++;
                        }
                    }

                } else {

                    /*
                     * Normal fields
                     */

                    if (
                        clean(element.value)
                    ) {

                        completed++;
                    }
                }

            }
        );


        if (totalFields === 0) {
            return;
        }


        const percentage =
            Math.round(
                (
                    completed /
                    totalFields
                ) * 100
            );


        const progressBar =
            document.getElementById(
                "progressBar"
            );


        const progressPercentage =
            document.getElementById(
                "progressPercentage"
            );


        if (progressBar) {

            progressBar.style.width =
                percentage + "%";
        }


        if (progressPercentage) {

            progressPercentage.textContent =
                percentage + "%";
        }
    }


    /* =====================================================
       ADDRESS INPUT
    ===================================================== */

    if (address) {

        address.addEventListener(
            "input",
            function () {

                clearValidation(
                    address,
                    errors.address
                );

                updateProgress();
            }
        );
    }


    /* =====================================================
       AADHAAR INPUT
    ===================================================== */

    if (aadhaar) {

        aadhaar.addEventListener(
            "input",
            function () {

                this.value =
                    this.value
                        .replace(/\D/g, "")
                        .slice(0, 12);


                clearValidation(
                    aadhaar,
                    errors.aadhaar
                );


                updateProgress();
            }
        );
    }


    /* =====================================================
       DRIVING LICENCE INPUT
    ===================================================== */

    if (drivingLicense) {

        drivingLicense.addEventListener(
            "input",
            function () {

                this.value =
                    this.value
                        .toUpperCase()
                        .replace(/\s/g, "");


                clearValidation(
                    drivingLicense,
                    errors.license
                );


                updateProgress();
            }
        );
    }


    /* =====================================================
       PAN INPUT
    ===================================================== */

    if (pan) {

        pan.addEventListener(
            "input",
            function () {

                this.value =
                    this.value
                        .toUpperCase()
                        .replace(/\s/g, "")
                        .slice(0, 10);


                clearValidation(
                    pan,
                    errors.pan
                );


                updateProgress();
            }
        );
    }


    /* =====================================================
       BANK ACCOUNT INPUT
    ===================================================== */

    if (bankAccount) {

        bankAccount.addEventListener(
            "input",
            function () {

                this.value =
                    this.value
                        .replace(/\D/g, "")
                        .slice(0, 18);


                clearValidation(
                    bankAccount,
                    errors.bank
                );


                updateProgress();
            }
        );
    }


    /* =====================================================
       IFSC INPUT
    ===================================================== */

    if (ifsc) {

        ifsc.addEventListener(
            "input",
            function () {

                this.value =
                    this.value
                        .toUpperCase()
                        .replace(/\s/g, "")
                        .slice(0, 11);


                clearValidation(
                    ifsc,
                    errors.ifsc
                );


                updateProgress();
            }
        );
    }


    /* =====================================================
       UPI INPUT
    ===================================================== */

    if (upi) {

        upi.addEventListener(
            "input",
            function () {

                clearValidation(
                    upi,
                    errors.upi
                );


                updateProgress();
            }
        );
    }


    /* =====================================================
       FORM SUBMISSION
    ===================================================== */

    form.addEventListener(
        "submit",
        function (event) {

            event.preventDefault();


            const validations = [

                validateProfilePicture(),

                validateAddress(),

                validateAadhaar(),

                validateAadhaarPhoto(),

                validateDrivingLicense(),

                validateDrivingLicensePhoto(),

                validatePAN(),

                validateBankAccount(),

                validateIFSC(),

                validateUPI()
            ];


            const isValid =
                validations.every(
                    function (result) {
                        return result === true;
                    }
                );


            updateProgress();


            /* =============================================
               INVALID
            ============================================== */

            if (!isValid) {

                alert(
                    "Please check the highlighted fields and complete the required information correctly."
                );


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

                            if (
                                typeof firstError.focus ===
                                "function"
                            ) {

                                firstError.focus();
                            }

                        },
                        500
                    );
                }


                return;
            }


            /* =============================================
               CONFIRMATION
            ============================================== */

            const actionText =
                isEditing
                    ? "update your owner profile"
                    : "save your owner profile";


            const confirmation =
                confirm(
                    "All information looks valid. Do you want to " +
                    actionText +
                    "?"
                );


            if (!confirmation) {
                return;
            }


            /* =============================================
               LOADING
            ============================================== */

            if (saveButton) {

                saveButton.disabled =
                    true;

                saveButton.classList.add(
                    "loading"
                );
            }


            if (buttonText) {

                buttonText.textContent =
                    isEditing
                        ? "Updating..."
                        : "Saving...";
            }


            /* =============================================
               REAL FORM SUBMISSION
            ============================================== */

            HTMLFormElement.prototype.submit.call(
                form
            );
        }
    );


    /* =====================================================
       INITIAL PROGRESS
    ===================================================== */

    updateProgress();

});