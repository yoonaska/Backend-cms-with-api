"use strict";

// Class definition
/*var DatatablesServerSide = function() {
    // Shared variables
    var table;
    var dt;

    // Private functions
    var initDatatable = function() {

        dt = $("#company-profile-datatable").DataTable({
            searchDelay: 500,
            serverSide: true,
            responsive: true,
            processing: true,
            order: [
                [0, 'desc']
            ],
            select: {
                style: 'multi',
                selector: 'td:first-child input[type="checkbox"]',
                className: 'row-selected'
            },
            ajax: {
                method: "POST",
                url: `${api_config.datatable}`,
                data: {
                    'csrfmiddlewaretoken': `${api_config.csrfmiddlewaretoken}`,
                },
            },
            columns: [
                {data   : 'id'},
                {data   : 'project_image'},
                {data   : 'title'},
                {data   : 'web_link'},
                {data   : 'is_active'},
                {data   : 'id'},
            ],

            columnDefs: [
                {
                    targets: 0,
                    orderable: false,
                    render: function (data) {
                        return `
                            <div class="form-check form-check-sm form-check-custom form-check-solid">
                                <input class="form-check-input checkbox-input-id" type="checkbox" value="${data}" />
                            </div>`;
                    }
                },
                {
                    searchable: true,
                    orderable: true,
                    targets: 3,
                    render: function(data, type, row) {
                        return `<div class="d-flex align-items-center">
                                    <div class="ms-5">
                                    <p class="text-gray-800  fs-5 fw-bolder"style="white-space: nowrap;overflow: hidden;text-overflow: ellipsis;max-width: 200px;display: inline-block;">${data}</p>
                                    </div>
                                </div>`;
                    }
                },
                {
                    searchable: true,
                    orderable: false,
                    targets: 1,
                    render: function(data, type, row) {
                        return `<div class="d-flex align-items-center">
                                    <div class="symbol symbol-50px me-3">
                                        <img src="${data}" class="" alt="">
                                    </div>
                                </div>`;
                    }
                },
                {
                    searchable: true,
                    orderable: true,
                    targets: 2,
                    render: function(data, type, row) {
                        let edit_url = api_config.edit_url.replace('0', row.encrypt_id.toString());
                        return `<div class="d-flex align-items-center">
                                    <a href="${edit_url}" class="symbol symbol-50px"style="white-space: nowrap;overflow: hidden;text-overflow: ellipsis;max-width: 200px;display: inline-block;" >
                                    </a>
                                    <div class="ms-5">
                                        <a href="${edit_url}" class="text-gray-800 text-hover-primary fs-5 fw-bolder gift-title" style="white-space: nowrap;overflow: hidden;text-overflow: ellipsis;max-width: 200px;display: inline-block;">${data}</a>
                                    </div>
                                </div>`;
                    }
                },
                {
                    searchable: false,
                    orderable: false,
                    targets: 4,
                    render: function(data, type, row) {
                        let label_badge_change = '';
                        if(data == 'True'){
                            label_badge_change = `<span style="cursor:pointer" data-id=${row.id}  class="btn btn-sm btn-outline btn-outline-dashed btn-outline-success btn-active-light-success active_inactive_language">Active</span>`;
                        }else if(data == 'False'){
                            label_badge_change =  `<span style="cursor:pointer" data-id=${row.id}  class="btn btn-sm btn-outline btn-outline-dashed btn-outline-danger btn-active-light-danger active_inactive_language">Inactive</span>`;
                        }
                        return label_badge_change;
                    }
                },
                {
                    targets: -1,
                    data: null,
                    orderable: false,
                    className: 'text-end',
                    render: function (data, type, row) {
                        let edit_url = api_config.edit_url.replace('0', row.encrypt_id.toString());
                        return `
                                <div class="d-flex justify-content-end flex-shrink-0">
                                    <a href="${edit_url}" class="btn btn-icon btn-bg-light btn-active-color-primary btn-sm me-1">
                                        <span class="svg-icon svg-icon-3">
                                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
                                                <path opacity="0.3" d="M21.4 8.35303L19.241 10.511L13.485 4.755L15.643 2.59595C16.0248 2.21423 16.5426 1.99988 17.0825 1.99988C17.6224 1.99988 18.1402 2.21423 18.522 2.59595L21.4 5.474C21.7817 5.85581 21.9962 6.37355 21.9962 6.91345C21.9962 7.45335 21.7817 7.97122 21.4 8.35303ZM3.68699 21.932L9.88699 19.865L4.13099 14.109L2.06399 20.309C1.98815 20.5354 1.97703 20.7787 2.03189 21.0111C2.08674 21.2436 2.2054 21.4561 2.37449 21.6248C2.54359 21.7934 2.75641 21.9115 2.989 21.9658C3.22158 22.0201 3.4647 22.0084 3.69099 21.932H3.68699Z" fill="currentColor" />
                                                <path d="M5.574 21.3L3.692 21.928C3.46591 22.0032 3.22334 22.0141 2.99144 21.9594C2.75954 21.9046 2.54744 21.7864 2.3789 21.6179C2.21036 21.4495 2.09202 21.2375 2.03711 21.0056C1.9822 20.7737 1.99289 20.5312 2.06799 20.3051L2.696 18.422L5.574 21.3ZM4.13499 14.105L9.891 19.861L19.245 10.507L13.489 4.75098L4.13499 14.105Z" fill="currentColor" />
                                            </svg>
                                        </span>
                                    </a>
                                    <a href="javascript:void(0)" data-id=${row.id} data-users-table-filter="delete_row" class="btn btn-icon btn-bg-light btn-active-color-primary btn-sm">
                                        <span class="svg-icon svg-icon-3">
                                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
                                                <path d="M5 9C5 8.44772 5.44772 8 6 8H18C18.5523 8 19 8.44772 19 9V18C19 19.6569 17.6569 21 16 21H8C6.34315 21 5 19.6569 5 18V9Z" fill="currentColor" />
                                                <path opacity="0.5" d="M5 5C5 4.44772 5.44772 4 6 4H18C18.5523 4 19 4.44772 19 5V5C19 5.55228 18.5523 6 18 6H6C5.44772 6 5 5.55228 5 5V5Z" fill="currentColor" />
                                                <path opacity="0.5" d="M9 4C9 3.44772 9.44772 3 10 3H14C14.5523 3 15 3.44772 15 4V4H9V4Z" fill="currentColor" />
                                            </svg>
                                        </span>
                                    </a>
                                </div>
                        `;
                    },
                },
            ],
            // Add data-filter attribute
            drawCallback: function(settings) {},
            createdRow: function(row, data, dataIndex) {
                $(row).find('td:eq(4)').attr('data-filter', data.CreditCardType);
            }
        });

        table = dt.$;
        // Re-init functions on every table re-draw -- more info: https://datatables.net/reference/event/draw
        dt.on('draw', function() {
            initToggleToolbar();
            toggleToolbars();
            handleDeleteRows();
            handleStatusFilter();
            ActiveOrIncativeUser();
            KTMenu.createInstances();
        });
    }

    // // Search Datatable --- official docs reference: https://datatables.net/reference/api/search()
    var handleSearchDatatable = function() {
        const filterSearch = document.querySelector('[data-users-table-filter="search"]');
        filterSearch.addEventListener('keyup', function(e) {
            dt.search(e.target.value).draw();
        });
    }

    // // Handle status filter dropdown
    var handleStatusFilter = () => {
        const filterStatus = document.querySelector('[data-users-filter="status"]');
        $(filterStatus).on('change', e => {
            let value = e.target.value;
            if(value === 'all'){
                value = '';
            }
            dt.column(3).search(value).draw();
        });
    }

    
    var ActiveOrIncativeUser = ()=>{
        const activeButton = document.getElementsByClassName('active_inactive_language')
        activeButton.forEach(d => {
            d.addEventListener('click', function(e) {
                const activeId = $(this).data('id');
                e.preventDefault();
                Swal.fire({
                    text: "Are you sure you want to change status",
                    icon: "warning",
                    showCancelButton: true,
                    buttonsStyling: true,
                    confirmButtonText: "Yes",
                    cancelButtonText: "No, return",
                    customClass: {
                        confirmButton: "btn btn-primary",
                        cancelButton: "btn btn-active-light"
                    }
                }).then(function(result){
                    if(result.value){               
                        $.post(`${api_config.active_inactive_company}`, {id:activeId }, function(data, status, xhr) {
                            if (data.status_code == 200) {
                                Swal.fire({
                                    text: "Successfully changed status ",
                                    icon: "success",
                                    buttonsStyling: false,
                                    confirmButtonText: "Ok, got it!",
                                    customClass: {
                                        confirmButton: "btn btn-primary"
                                    }
                                }).then(function() {
                                    dt.draw();
                                });
    
                            } else {
                                Swal.fire({
                                    text: "Something went wrong.",
                                    icon: "error",
                                    buttonsStyling: false,
                                    confirmButtonText: "Ok, got it!",
                                    customClass: {
                                        confirmButton: "btn fw-bold btn-primary",
                                    }
                                });
                            }
                        })
                    }
                })
            });
        });
    }

        
    
    // Delete customer
    var handleDeleteRows = () => {
        // Select all delete buttons
        const deleteButtons = document.querySelectorAll('[data-users-table-filter="delete_row"]');

        deleteButtons.forEach(d => {
            // Delete button on click
            d.addEventListener('click', function(e) {

                const destroyRecordIds = [$(this).data('id')];
                e.preventDefault();
                // Select parent row
                const parent = e.target.closest('tr');
                // Get customer name
                const userName = parent.querySelectorAll('td')[1].innerText;

                //     // SweetAlert2 pop up --- official docs reference: https://sweetalert2.github.io/
                Swal.fire({
                    text: "Are you sure you want to delete " + userName + "?",
                    icon: "warning",
                    showCancelButton: true,
                    buttonsStyling: false,
                    confirmButtonText: "Yes, delete!",
                    cancelButtonText: "No, cancel",
                    customClass: {
                        confirmButton: "btn fw-bold btn-danger",
                        cancelButton: "btn fw-bold btn-active-light-primary"
                    }
                }).then(function(result) {
                    if (result.value) {
                        $.post(`${api_config.delete_records}`, { ids: destroyRecordIds }, function(data, status, xhr) {

                            if (data.status_code == 200) {
                                Swal.fire({
                                    text: "Success",
                                    icon: "success",
                                    buttonsStyling: false,
                                    confirmButtonText: "Ok, got it!",
                                    customClass: {
                                        confirmButton: "btn fw-bold btn-primary",
                                    }
                                }).then(function() {
                                    // delete row data from server and re-draw datatable
                                    dt.draw();
                                });

                            } else {
                                Swal.fire({
                                    text: "Something went wrong.",
                                    icon: "error",
                                    buttonsStyling: false,
                                    confirmButtonText: "Ok, got it!",
                                    customClass: {
                                        confirmButton: "btn fw-bold btn-primary",
                                    }
                                });
                            }

                        }, 'json').done(function() {
                            console.log('Request done!');
                        }).fail(function(jqxhr, settings, ex) {
                            console.log('failed, ' + ex);
                            Swal.fire({
                                text: "Something went wrong.",
                                icon: "error",
                                buttonsStyling: false,
                                confirmButtonText: "Ok, got it!",
                                customClass: {
                                    confirmButton: "btn fw-bold btn-primary",
                                }
                            });
                        });

                    } else if (result.dismiss === 'cancel') {
                        Swal.fire({
                            text: userName + " was not deleted.",
                            icon: "error",
                            buttonsStyling: false,
                            confirmButtonText: "Ok, got it!",
                            customClass: {
                                confirmButton: "btn fw-bold btn-primary",
                            }
                        });
                    }
                });
            })
        });
    }



    // Init toggle toolbar
    var initToggleToolbar = function() {
        // Toggle selected action toolbar
        // Select all checkboxes
        const container = document.querySelector('#company-profile-datatable');
        const checkboxes = container.querySelectorAll('[type="checkbox"]');

        // Select elements
        const deleteSelected = document.querySelector('[data-users-table-select="delete_selected"]');

        // Toggle delete selected toolbar
        checkboxes.forEach(c => {
            // Checkbox on click event
            c.addEventListener('click', function() {
                setTimeout(function() {
                    toggleToolbars();
                }, 50);
            });
        });

        // Deleted selected rows
        deleteSelected.addEventListener('click', function() {

            const row_ids = []
            $(".checkbox-input-id:checkbox:checked").each(function() {
                row_ids.push($(this).val());
            });

            Swal.fire({
                text: "Are you sure you want to delete selected ?",
                icon: "warning",
                showCancelButton: true,
                buttonsStyling: false,
                showLoaderOnConfirm: true,
                confirmButtonText: "Yes, delete!",
                cancelButtonText: "No, cancel",
                customClass: {
                    confirmButton: "btn fw-bold btn-danger",
                    cancelButton: "btn fw-bold btn-active-light-primary"
                },
            }).then(function(result) {
                if (result.value) {

                    $.post(`${api_config.delete_records}`, { ids: row_ids }, function(data, status, xhr) {

                        if (data.status = 200) {
                            Swal.fire({
                                text: "You have deleted all selected ",
                                icon: "success",
                                buttonsStyling: false,
                                confirmButtonText: "Ok, got it!",
                                customClass: {
                                    confirmButton: "btn fw-bold btn-primary",
                                }
                            }).then(function() {
                                // delete row data from server and re-draw datatable
                                dt.draw();
                                const headerCheckbox = container.querySelectorAll('[type="checkbox"]')[0];
                                headerCheckbox.checked = false;
                            });

                        } else {
                            Swal.fire({
                                text: "Something went wrong.",
                                icon: "error",
                                buttonsStyling: false,
                                confirmButtonText: "Ok, got it!",
                                customClass: {
                                    confirmButton: "btn fw-bold btn-primary",
                                }
                            });
                        }

                    }, 'json').done(function() {
                        console.log('Request done!');
                    }).fail(function(jqxhr, settings, ex) {
                        console.log('failed, ' + ex);
                        Swal.fire({
                            text: "Something went wrong.",
                            icon: "error",
                            buttonsStyling: false,
                            confirmButtonText: "Ok, got it!",
                            customClass: {
                                confirmButton: "btn fw-bold btn-primary",
                            }
                        });
                    });

                } else if (result.dismiss === 'cancel') {
                    Swal.fire({
                        text: "Selected user was not deleted.",
                        icon: "error",
                        buttonsStyling: false,
                        confirmButtonText: "Ok, got it!",
                        customClass: {
                            confirmButton: "btn fw-bold btn-primary",
                        }
                    });
                }
            });
        });
    }

    var toggleToolbars = function() {
        // Define variables
        const container = document.querySelector('#company-profile-datatable');
        const toolbarBase = document.querySelector('[data-table-toolbar="base"]');
        const toolbarSelected = document.querySelector('[data-users-table-toolbar="selected"]');
        const selectedCount = document.querySelector('[data-users-table-select="selected_count"]');
        // Select refreshed checkbox DOM elements
        const allCheckboxes = container.querySelectorAll('tbody [type="checkbox"]');
        const headerCheckbox = container.querySelectorAll('[type="checkbox"]')[0];
      
        // Detect checkboxes state & count
        let checkedState = false;
        let count = 0;
      
        // Count checked boxes
        allCheckboxes.forEach(c => {
          if (c.checked) {
            checkedState = true;
            count++;
          }
        });
      
        // Toggle toolbars
        if (checkedState) {
            selectedCount.innerHTML = count;
          toolbarBase.classList.add('d-none');
          toolbarSelected.classList.remove('d-none');
        } else {
          toolbarBase.classList.remove('d-none');
          toolbarSelected.classList.add('d-none');
        }
      
        // Check/uncheck checkboxes based on "select all" checkbox state
        headerCheckbox.addEventListener('click', function() {
          allCheckboxes.forEach(c => {
            c.checked = headerCheckbox.checked;
          });
          checkedState = headerCheckbox.checked;
          count = headerCheckbox.checked ? allCheckboxes.length : 0;
          selectedCount.innerHTML = count;
          if (checkedState) {
            toolbarBase.classList.add('d-none');
            toolbarSelected.classList.remove('d-none');
          } else {
            toolbarBase.classList.remove('d-none');
            toolbarSelected.classList.add('d-none');
          }
        });
                // Uncheck header checkbox if not all checkboxes are checked
                if (checkedState && count !== allCheckboxes.length) {
                    headerCheckbox.checked = false;
                  } else if (count === 0) { // added new condition
                    headerCheckbox.checked = false;
                  }
                  else if (checkedState && count == allCheckboxes.length) {
                      headerCheckbox.checked = true;
                  }
          
      };
      


    // Public methods
    return {
        init: function() {
            initDatatable();
            handleSearchDatatable();
            initToggleToolbar();
            handleDeleteRows();
            ActiveOrIncativeUser();
            handleStatusFilter ();

        }
    }
}();

// On document ready
KTUtil.onDOMContentLoaded(function() {
    DatatablesServerSide.init();
});
*/



//MULTIPLE IMAGE UPLOADING WITH ORDERING

function imageUrlToBase64(url) {
    return new Promise(function (resolve, reject) {
        var img = new Image();
        img.crossOrigin = 'Anonymous';

        img.onload = function () {
            var canvas = document.createElement('canvas');
            var ctx = canvas.getContext('2d');
            canvas.width = img.width;
            canvas.height = img.height;
            ctx.drawImage(img, 0, 0);

            // Get the base64 data URL from the canvas
            var dataURL = canvas.toDataURL('image/png');

            // Resolve the promise with the base64 data URL
            resolve(dataURL);
        };

        img.onerror = function () {
            // Reject the promise if there is an error loading the image
            reject(new Error('Failed to load image.'));
        };

        img.src = url;
    });
}
// Function to add an image to the sortable list
function addImageToSortable(order, id, imageUrl,index) {
    $('#sortable').prepend('<li class="ui-state-default" data-order="' + order + '" data-id="' + id + '">' +
        '<div class="image-container">' +
        '<img src="' + imageUrl + '" style="width:100%;" /> ' +
        '<button class="delete-button" data-id="'+ id +'"" onclick="deleteImageCard(this)"><i class="fa fa-times del"></i></button>' +
        '</div>' +
        '<div class="order-number">' + index + '</div>' +
        '</li>');
}
function initialLoadImages (){
    var inputs = $('.initial-image input');
    var totalLength = inputs.length;

    $('.initial-image input').each(function (index) {
        var order = $(this).attr('data-order-id');
        var url = $(this).attr('data-url');
        var id = $(this).attr('data-id');
        let b_url = null
        
        // imageUrlToBase64(url)
        //     .then(function (base64Image) {
        //         // 'base64Image' contains the base64-encoded image data
        //         b_url = base64Image;
        //         // Now you can continue with your code here
        //     })
        //     .catch(function (error) {
        //         console.error('Error:', error);
        //     });
        // Create an object to store the data
        addImageToSortable(order,id,url,totalLength)
        totalLength-=1
        var imageData = {
            order: order,
            url: url,
            id: id
        };

        // Push the object to the array
    });
}
initialLoadImages()

$(function () {
    $('#images').change(function (e) {
        // Show the loading overlay
        $('#loading-overlay').show();
    
        var files = e.target.files;
        var formData = new FormData();
    
        for (var i = 0; i < files.length; i++) {
            var file = files[i];
            var order = i + 1;
            var key = order;
            formData.append(key, file);
        }
    
        // Add the CSRF token to the FormData
        formData.append('csrfmiddlewaretoken', api_config['csrfmiddlewaretoken']);
    
        $.ajax({
            url: api_config['image-order'],
            method: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function (response) {
                console.log(response);
    
                // Check if the response status is 200 and the message is 'Success'
                if (response.status_code === 200 && response.message === 'Success') {
                    // Get the URL to redirect to from the data-href attribute of the button
                    var redirectUrl = $('#save-button').data('href');
    
                    // Hide the loading overlay before redirecting
                    $('#loading-overlay').hide();
    
                    // Redirect to the specified URL
                    window.location.href = redirectUrl;
                }
            },
            error: function (error) {
                console.error(error);
                // Hide the loading overlay in case of an error
                $('#loading-overlay').hide();
            }
        });
    });
    
    
    
    $('#sortable').sortable();
    $('#sortable').disableSelection();

    // Sortable events
    $('#sortable').on('sortbeforestop', function (event) {
        reorderImages();
    });

    function reorderImages() {
        // Get the items
        var images = $('#sortable li');
        var i = 0, nrOrder = 0;
        
        for (i; i < images.length; i++) {
            var image = $(images[i]);
            if (image.hasClass('ui-state-default') && !image.hasClass('ui-sortable-placeholder')) {
                image.attr('data-order', nrOrder);
                var orderNumberBox = image.find('.order-number');
                orderNumberBox.html(nrOrder + 1);
                nrOrder++;
            }
        }

        // Collect image data and send it via AJAX
        var imageArray = [];
        images.each(function (index) {
            var image = $(this);
            if(!image.hasClass('ui-sortable-placeholder')){
                
            
                var order = index+=1;
                var imageId = image.data('id');
                imageArray.push({
                    order: order,
                    image_id: imageId,
                });
            }
        });
        // Send the image data via AJAX
        $.ajax({
            url: api_config['image-order'],
            method: 'POST',
            data: {
                images: JSON.stringify(imageArray),
                csrfmiddlewaretoken: api_config['csrfmiddlewaretoken'],
                is_update: 'True',
            },
            success: function (response) {
                console.log(response);
            },
            error: function (error) {
                console.error(error);
            }
        });
    }
});

function deleteImageCard(a) {
    var instanceId = $(a).data('id');
    $.ajax({
        url: api_config['delete-image'],
        method: 'POST',
        data: {
            instance_id: instanceId,
            csrfmiddlewaretoken: api_config['csrfmiddlewaretoken'],
        },
        success: function (response) {
            console.log(response);
            location.reload();
        },
        error: function (error) {
            console.error(error);
        }
    });
}

// Save buttion

// $(document).ready(function() {
// $('.btn-save').click(function() {
//     // Reload the current page
//     location.reload();
// });
// });

$('#save-button').click(function () {
    // Get the URL to redirect to from the data-href attribute of the button
    var redirectUrl = $(this).data('href');
    
    // Redirect to the specified URL
    window.location.href = redirectUrl;
});



// DELETE ALL API CALL ON CLICK
$(document).ready(function() {
    $('.btn-remove').click(function() {
        // Show a confirmation dialog
        Swal.fire({
            title: 'Confirm Delete',
            text: 'Are you sure you want to remove all images?',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Yes, remove all',
            cancelButtonText: 'No, cancel',
        }).then((result) => {
            if (result.isConfirmed) {
                // User clicked "Yes, remove all," so execute the AJAX request
                var is_delete_all = true; // Set to true or false as needed

                $.ajax({
                    url: api_config['delete-image'],
                    method: 'POST',
                    data: {
                        is_delete_all: is_delete_all,
                        csrfmiddlewaretoken: api_config['csrfmiddlewaretoken'],
                    },
                    success: function (response) {
                        Swal.fire('Deleted', 'All images have been removed.', 'success');
                        
                        // Reload the page after a successful delete
                        setTimeout(function() {
                            location.reload();
                        }, 1000);
                    },
                    error: function (error) {
                        Swal.fire('Error', 'An error occurred while removing images.', 'error');
                    }
                });
            }
        });
    });
});
