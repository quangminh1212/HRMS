// HRMS Main JavaScript

// Initialize tooltips and popovers
document.addEventListener('DOMContentLoaded', function() {
    // Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Bootstrap popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000);
});

// Global search functionality
function showSearchModal() {
    $('#searchModal').modal('show');
    setTimeout(function() {
        $('#quickSearch').focus();
    }, 500);
}

// Quick search with debounce
let searchTimeout;
$('#quickSearch').on('input', function() {
    clearTimeout(searchTimeout);
    const query = $(this).val().trim();
    
    if (query.length < 2) {
        $('#searchResults').html('');
        return;
    }
    
    $('#searchResults').html('<div class="text-center"><div class="spinner-border text-primary" role="status"></div></div>');
    
    searchTimeout = setTimeout(function() {
        $.ajax({
            url: '/api/search-employees',
            method: 'GET',
            data: { q: query },
            success: function(data) {
                if (data.length === 0) {
                    $('#searchResults').html('<p class="text-muted text-center">Không tìm thấy kết quả</p>');
                    return;
                }
                
                let html = '<div class="list-group">';
                data.forEach(function(emp) {
                    html += `
                        <a href="/employee/${emp.id}" class="list-group-item list-group-item-action">
                            <div class="d-flex w-100 justify-content-between">
                                <h6 class="mb-1">${emp.name}</h6>
                                <small class="text-muted">${emp.code}</small>
                            </div>
                            <p class="mb-1">${emp.position || 'Chưa có chức vụ'}</p>
                            <small class="text-muted">${emp.department || 'Chưa có đơn vị'}</small>
                        </a>
                    `;
                });
                html += '</div>';
                $('#searchResults').html(html);
            },
            error: function() {
                $('#searchResults').html('<p class="text-danger text-center">Có lỗi xảy ra khi tìm kiếm</p>');
            }
        });
    }, 300);
});

// Form validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form.checkValidity()) {
        form.classList.add('was-validated');
        return false;
    }
    return true;
}

// Date formatting
function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('vi-VN');
}

// Number formatting
function formatNumber(number) {
    return new Intl.NumberFormat('vi-VN').format(number);
}

// Currency formatting
function formatCurrency(amount) {
    return new Intl.NumberFormat('vi-VN', {
        style: 'currency',
        currency: 'VND'
    }).format(amount);
}

// Export functions
function exportToExcel(endpoint) {
    window.location.href = endpoint + '?format=excel';
}

function exportToWord(endpoint) {
    window.location.href = endpoint + '?format=word';
}

function exportToPDF(endpoint) {
    window.location.href = endpoint + '?format=pdf';
}

// Confirmation dialogs
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// AJAX form submission
function submitFormAjax(formId, successCallback) {
    const form = document.getElementById(formId);
    const formData = new FormData(form);
    
    $.ajax({
        url: form.action,
        method: form.method,
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            if (successCallback) {
                successCallback(response);
            } else {
                showNotification('success', 'Thao tác thành công!');
            }
        },
        error: function(xhr) {
            showNotification('danger', 'Có lỗi xảy ra: ' + xhr.responseText);
        }
    });
}

// Show notification
function showNotification(type, message) {
    const alertHtml = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    const container = document.querySelector('.container') || document.querySelector('.container-fluid');
    container.insertAdjacentHTML('afterbegin', alertHtml);
    
    setTimeout(function() {
        $('.alert').fadeOut('slow', function() {
            $(this).remove();
        });
    }, 5000);
}

// Table row selection
function toggleRowSelection(checkbox) {
    const row = checkbox.closest('tr');
    if (checkbox.checked) {
        row.classList.add('table-active');
    } else {
        row.classList.remove('table-active');
    }
}

// Select all checkboxes
function selectAllRows(masterCheckbox) {
    const checkboxes = document.querySelectorAll('input[type="checkbox"].row-checkbox');
    checkboxes.forEach(function(checkbox) {
        checkbox.checked = masterCheckbox.checked;
        toggleRowSelection(checkbox);
    });
}

// Print function
function printContent(elementId) {
    const content = document.getElementById(elementId).innerHTML;
    const printWindow = window.open('', '_blank');
    printWindow.document.write(`
        <html>
        <head>
            <title>In tài liệu</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body { padding: 20px; }
                @media print {
                    .no-print { display: none; }
                }
            </style>
        </head>
        <body>
            ${content}
            <script>
                window.onload = function() {
                    window.print();
                    window.onafterprint = function() {
                        window.close();
                    }
                }
            </script>
        </body>
        </html>
    `);
}

// Calculate age from date of birth
function calculateAge(dateOfBirth) {
    const today = new Date();
    const birthDate = new Date(dateOfBirth);
    let age = today.getFullYear() - birthDate.getFullYear();
    const monthDiff = today.getMonth() - birthDate.getMonth();
    
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
        age--;
    }
    
    return age;
}

// Calculate retirement date
function calculateRetirementDate(dateOfBirth, gender) {
    const birthDate = new Date(dateOfBirth);
    let retirementAge = gender === 'Nam' ? 60 : 55;
    let additionalMonths = gender === 'Nam' ? 3 : 4;
    
    let retirementDate = new Date(birthDate);
    retirementDate.setFullYear(birthDate.getFullYear() + retirementAge);
    retirementDate.setMonth(birthDate.getMonth() + additionalMonths);
    
    return retirementDate;
}

// File upload preview
function previewFile(input, previewId) {
    const preview = document.getElementById(previewId);
    const file = input.files[0];
    
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            if (file.type.startsWith('image/')) {
                preview.innerHTML = `<img src="${e.target.result}" class="img-thumbnail" style="max-width: 200px;">`;
            } else {
                preview.innerHTML = `<p class="text-muted">${file.name}</p>`;
            }
        };
        reader.readAsDataURL(file);
    }
}

// Dynamic form field addition
function addFormField(containerId, fieldHtml) {
    const container = document.getElementById(containerId);
    const div = document.createElement('div');
    div.innerHTML = fieldHtml;
    container.appendChild(div);
}

// Remove form field
function removeFormField(button) {
    button.closest('.form-group').remove();
}

// Data table initialization (if using DataTables)
function initDataTable(tableId) {
    if ($.fn.DataTable) {
        $(`#${tableId}`).DataTable({
            language: {
                url: '//cdn.datatables.net/plug-ins/1.10.24/i18n/Vietnamese.json'
            },
            pageLength: 25,
            responsive: true
        });
    }
}

// Chart initialization helper
function createChart(canvasId, type, data, options) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    return new Chart(ctx, {
        type: type,
        data: data,
        options: options || {
            responsive: true,
            maintainAspectRatio: false
        }
    });
}

// Session timeout warning
let sessionTimeout;
function resetSessionTimeout() {
    clearTimeout(sessionTimeout);
    sessionTimeout = setTimeout(function() {
        showNotification('warning', 'Phiên làm việc sắp hết hạn. Vui lòng lưu công việc của bạn.');
    }, 25 * 60 * 1000); // 25 minutes
}

// Reset timeout on user activity
document.addEventListener('click', resetSessionTimeout);
document.addEventListener('keypress', resetSessionTimeout);
resetSessionTimeout();
