// Meta Content Manager - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            if (alert.classList.contains('alert-success')) {
                var bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        });
    }, 5000);

    // Add fade-in animation to cards
    var cards = document.querySelectorAll('.card');
    cards.forEach(function(card, index) {
        card.style.animationDelay = (index * 0.1) + 's';
        card.classList.add('fade-in');
    });

    // Form validation helpers
    addFormValidation();
    
    // Character counters
    addCharacterCounters();
    
    // Image preview functionality
    addImagePreview();
});

function addFormValidation() {
    // Add real-time validation to forms
    var forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                
                // Focus on first invalid field
                var firstInvalid = form.querySelector(':invalid');
                if (firstInvalid) {
                    firstInvalid.focus();
                    firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
            form.classList.add('was-validated');
        });
    });
}

function addCharacterCounters() {
    // Add character counters to textareas
    var textareas = document.querySelectorAll('textarea[data-max-length]');
    textareas.forEach(function(textarea) {
        var maxLength = parseInt(textarea.dataset.maxLength);
        var counter = document.createElement('div');
        counter.className = 'form-text text-end';
        counter.innerHTML = '<small><span class="char-count">0</span>/' + maxLength + ' characters</small>';
        
        textarea.parentNode.appendChild(counter);
        
        textarea.addEventListener('input', function() {
            var count = this.value.length;
            var spanCount = counter.querySelector('.char-count');
            spanCount.textContent = count;
            
            if (count > maxLength * 0.9) {
                spanCount.className = 'char-count text-warning';
            } else if (count > maxLength) {
                spanCount.className = 'char-count text-danger';
            } else {
                spanCount.className = 'char-count';
            }
        });
    });
}

function addImagePreview() {
    // Add image preview functionality to URL inputs
    var imageInputs = document.querySelectorAll('input[type="url"][data-preview]');
    imageInputs.forEach(function(input) {
        var previewId = input.dataset.preview;
        var preview = document.getElementById(previewId);
        
        if (preview) {
            input.addEventListener('input', function() {
                var url = this.value.trim();
                if (url && isValidImageUrl(url)) {
                    preview.src = url;
                    preview.style.display = 'block';
                    preview.onerror = function() {
                        this.style.display = 'none';
                    };
                } else {
                    preview.style.display = 'none';
                }
            });
        }
    });
}

function isValidImageUrl(url) {
    return /\.(jpg|jpeg|png|gif|webp)$/i.test(url) || 
           url.includes('imgur') || 
           url.includes('unsplash') ||
           url.includes('pexels') ||
           url.includes('pixabay');
}

// Utility functions
function showNotification(message, type = 'success') {
    var notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(function() {
        if (notification.parentNode) {
            var bsAlert = new bootstrap.Alert(notification);
            bsAlert.close();
        }
    }, 5000);
}

function copyToClipboard(text) {
    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(function() {
            showNotification('<i class="fas fa-check"></i> Copied to clipboard!', 'success');
        }).catch(function() {
            fallbackCopyToClipboard(text);
        });
    } else {
        fallbackCopyToClipboard(text);
    }
}

function fallbackCopyToClipboard(text) {
    var textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        var successful = document.execCommand('copy');
        if (successful) {
            showNotification('<i class="fas fa-check"></i> Copied to clipboard!', 'success');
        } else {
            showNotification('<i class="fas fa-exclamation-triangle"></i> Could not copy to clipboard', 'warning');
        }
    } catch (err) {
        showNotification('<i class="fas fa-exclamation-triangle"></i> Could not copy to clipboard', 'warning');
    }
    
    document.body.removeChild(textArea);
}

function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

function validateUrl(url) {
    try {
        new URL(url);
        return true;
    } catch {
        return false;
    }
}

function sanitizeHtml(str) {
    var temp = document.createElement('div');
    temp.textContent = str;
    return temp.innerHTML;
}

// Loading state management
function showLoading(element) {
    if (typeof element === 'string') {
        element = document.getElementById(element);
    }
    
    if (element) {
        element.innerHTML = `
            <div class="text-center py-4">
                <div class="spinner-border" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-2">Loading...</p>
            </div>
        `;
    }
}

function hideLoading(element) {
    if (typeof element === 'string') {
        element = document.getElementById(element);
    }
    
    if (element) {
        element.style.display = 'none';
    }
}

// Error handling
function handleApiError(error, fallbackMessage = 'An error occurred') {
    console.error('API Error:', error);
    
    var message = error.message || fallbackMessage;
    showNotification(`<i class="fas fa-exclamation-triangle"></i> ${message}`, 'danger');
}

// Form helpers
function resetForm(formId) {
    var form = document.getElementById(formId);
    if (form) {
        form.reset();
        form.classList.remove('was-validated');
        
        // Reset any custom validation states
        var inputs = form.querySelectorAll('.is-invalid, .is-valid');
        inputs.forEach(function(input) {
            input.classList.remove('is-invalid', 'is-valid');
        });
    }
}

function enableForm(formId) {
    var form = document.getElementById(formId);
    if (form) {
        var inputs = form.querySelectorAll('input, textarea, select, button');
        inputs.forEach(function(input) {
            input.disabled = false;
        });
    }
}

function disableForm(formId) {
    var form = document.getElementById(formId);
    if (form) {
        var inputs = form.querySelectorAll('input, textarea, select, button');
        inputs.forEach(function(input) {
            input.disabled = true;
        });
    }
}

// Analytics helpers
function createChart(canvas, data, options = {}) {
    // Placeholder for chart creation
    // You can integrate Chart.js or other charting libraries here
    console.log('Chart data:', data);
}

// Export functions for global use
window.MetaApp = {
    showNotification,
    copyToClipboard,
    formatNumber,
    validateUrl,
    sanitizeHtml,
    showLoading,
    hideLoading,
    handleApiError,
    resetForm,
    enableForm,
    disableForm,
    createChart
};