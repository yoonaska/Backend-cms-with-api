function previewImage(event) {
    var logoPreview = document.getElementById('logo-preview');
    logoPreview.src = URL.createObjectURL(event.target.files[0]);
    logoPreview.style.display = "block";
}

function ogimagepreviewImage(event) {
    var logoPreview = document.getElementById('og-image-logo-preview');
    logoPreview.src = URL.createObjectURL(event.target.files[0]);
    logoPreview.style.display = "block";
}
function validateInput(inputElement) {
    // Get the entered value from the input field
    const value = inputElement.value;
    
    // Convert the value to a number (parsing it as an integer)
    const numberValue = parseInt(value, 10);
    
    // Check if the number is less than 0
    if (numberValue < 0) {
        // If the number is less than 0, set the input value to 0
        inputElement.value = 0;
    }
}

$('#features').repeater({
    initEmpty: false,
    defaultValues: false, // Set this to false to use the placeholders instead of default values

    show: function () {
        $(this).slideDown();
        // Set the placeholders for the input fields inside the repeater
        $(this).find('input[name="name"]').attr('placeholder', 'Title');
        $(this).find('textarea[name="description"]').attr('placeholder', 'Description');
    },

    hide: function (deleteElement) {
        $(this).slideUp(deleteElement);
    }
});




"use strict";

// Class definition
var MCUpdateOrCreateProperty = function () {

    var validator;

    var form;
    const handleSubmit = () => {
        // Get elements
        form = document.getElementById('create-or-update-company-profile-form');
        const submitButton = document.getElementById('create-or-update-company-profile-submit');
    
        validator = FormValidation.formValidation(
            
            form,
            {
                fields: {
                    'title': {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    },
                    'url': {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    },
                    'description_title': {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    },
                    'description': {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    },
                    'meta_keyword': {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    },
                    'meta_keyword': {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    },
                    'meta_image_title': {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    },
                    'meta_description': {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    },
                    // 'service_image': {
                    //     validators: {
                    //         file: {
                    //             maxSize: 1024 * 1024, // Maximum file size in bytes (1 MB)
                    //             message: 'The selected file is not valid or is above 1 MB'
                    //         }
                    //     }
                    // },
                    // 'og_image': {
                    //     validators: {
                    //         file: {
                    //             extension: 'jpg,jpeg,png',
                    //             type: 'image/jpeg,image/png',
                    //             maxSize: 1024 * 1024, // Maximum file size in bytes (1 MB)
                    //             message: 'The selected file is not valid or is above 1 MB'
                    //         }
                    //     }
                    // },
                },
                plugins: {
                    trigger: new FormValidation.plugins.Trigger(),
                    bootstrap: new FormValidation.plugins.Bootstrap5({
                        rowSelector: '.fv-row',
                        eleInvalidClass: '',
                        eleValidClass: ''
                    })
                }
            }
        );

        submitButton.addEventListener('click', e => {
            e.preventDefault();

            // Validate form before submit
            if (validator) {
                validator.validate().then(function (status) {
                    
                    console.log('validated!');
                    submitButton.setAttribute('data-kt-indicator', 'on');

                    // Disable button to avoid multiple click
                    submitButton.disabled = true;

                    if (status == 'Valid') {

                        // Handle submit button
                        e.preventDefault();
                        const btn = document.getElementById('create-or-update-company-profile-submit');
                        const text = document.getElementById('banner-loader-text');
                        btn.disabled = true;
                        btn.style.display = 'none';
                        text.style.display = 'block';

                        submitButton.setAttribute('data-kt-indicator', 'on');

                        // Disable submit button whilst loading
                        submitButton.disabled = true;
                        submitButton.removeAttribute('data-kt-indicator');
                        // Enable submit button after loading
                        submitButton.disabled = false;

                        // Redirect to customers list page
                        form.submit();
                    } else {
                        submitButton.removeAttribute('data-kt-indicator');

                        // Enable button
                        submitButton.disabled = false;
                        Swal.fire({
                            html: "Sorry, looks like there are some errors detected, please try again.",
                            icon: "error",
                            buttonsStyling: false,
                            confirmButtonText: "Ok, got it!",
                            customClass: {
                                confirmButton: "btn btn-primary"
                            }
                        });
                    }
                });
            }
        });

    }



    
    // Public methods
    return {
        init: function () {
            handleSubmit();
            
        }
    };
}();




// On document ready
KTUtil.onDOMContentLoaded(function () {
    MCUpdateOrCreateProperty.init();
});



