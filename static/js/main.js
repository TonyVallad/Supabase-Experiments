// Main JavaScript for Supabase-Experiments Web Application

// Global utilities
window.SupabaseApp = {
    // Show toast notifications
    showAlert: function(message, type = 'info') {
        const alertContainer = document.createElement('div');
        alertContainer.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show position-fixed`;
        alertContainer.style.top = '20px';
        alertContainer.style.right = '20px';
        alertContainer.style.zIndex = '9999';
        alertContainer.style.minWidth = '300px';
        alertContainer.innerHTML = `
            <div class="d-flex align-items-center">
                <i class="fas fa-${this.getAlertIcon(type)} me-2"></i>
                <div>${message}</div>
            </div>
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(alertContainer);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (alertContainer.parentNode) {
                alertContainer.remove();
            }
        }, 5000);
    },

    getAlertIcon: function(type) {
        switch(type) {
            case 'success': return 'check-circle';
            case 'error': return 'exclamation-triangle';
            case 'warning': return 'exclamation-circle';
            default: return 'info-circle';
        }
    },

    // Format file size
    formatFileSize: function(sizeInMB) {
        if (sizeInMB >= 1024) {
            return `${(sizeInMB / 1024).toFixed(1)} GB`;
        }
        return `${sizeInMB} MB`;
    },

    // Format date
    formatDate: function(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    },

    // API helper functions
    api: {
        async request(url, options = {}) {
            const defaults = {
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'same-origin'
            };

            const config = { ...defaults, ...options };
            
            try {
                const response = await fetch(url, config);
                const data = await response.json();
                return data;
            } catch (error) {
                console.error('API request failed:', error);
                throw error;
            }
        },

        async get(url) {
            return this.request(url, { method: 'GET' });
        },

        async post(url, data) {
            return this.request(url, {
                method: 'POST',
                body: JSON.stringify(data)
            });
        },

        async put(url, data) {
            return this.request(url, {
                method: 'PUT',
                body: JSON.stringify(data)
            });
        },

        async delete(url) {
            return this.request(url, { method: 'DELETE' });
        }
    },

    // Loading state management
    setLoading: function(element, loading = true, originalText = '') {
        if (loading) {
            element.dataset.originalText = element.innerHTML;
            element.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Loading...';
            element.disabled = true;
        } else {
            element.innerHTML = element.dataset.originalText || originalText;
            element.disabled = false;
        }
    },

    // Initialize animations
    initAnimations: function() {
        // Fade-in animations
        const elements = document.querySelectorAll('.fade-in');
        elements.forEach((element, index) => {
            setTimeout(() => {
                element.style.animation = 'fadeIn 0.6s ease-in forwards';
            }, index * 100);
        });

        // Hover effects for cards
        const cards = document.querySelectorAll('.card');
        cards.forEach(card => {
            card.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-2px)';
                this.style.transition = 'transform 0.2s ease';
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0)';
            });
        });

        // Stat card hover effects
        const statCards = document.querySelectorAll('.stat-card');
        statCards.forEach(card => {
            card.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-5px) scale(1.02)';
                this.style.transition = 'transform 0.3s ease';
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1)';
            });
        });
    },

    // Initialize page
    init: function() {
        document.addEventListener('DOMContentLoaded', () => {
            this.initAnimations();
            
            // Initialize tooltips
            const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
            tooltipTriggerList.map(function (tooltipTriggerEl) {
                return new bootstrap.Tooltip(tooltipTriggerEl);
            });

            console.log('🚀 Supabase-Experiments Web App Initialized');
        });
    }
};

// Form validation utilities
window.FormValidator = {
    validateRequired: function(element, message = 'This field is required') {
        if (!element.value.trim()) {
            this.showFieldError(element, message);
            return false;
        }
        this.clearFieldError(element);
        return true;
    },

    validateEmail: function(element) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(element.value)) {
            this.showFieldError(element, 'Please enter a valid email address');
            return false;
        }
        this.clearFieldError(element);
        return true;
    },

    validateNumber: function(element, min = null, max = null) {
        const value = parseFloat(element.value);
        if (isNaN(value)) {
            this.showFieldError(element, 'Please enter a valid number');
            return false;
        }
        if (min !== null && value < min) {
            this.showFieldError(element, `Value must be at least ${min}`);
            return false;
        }
        if (max !== null && value > max) {
            this.showFieldError(element, `Value must be no more than ${max}`);
            return false;
        }
        this.clearFieldError(element);
        return true;
    },

    showFieldError: function(element, message) {
        element.classList.add('is-invalid');
        
        // Remove existing error message
        const existingError = element.parentNode.querySelector('.invalid-feedback');
        if (existingError) {
            existingError.remove();
        }

        // Add new error message
        const errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback';
        errorDiv.textContent = message;
        element.parentNode.appendChild(errorDiv);
    },

    clearFieldError: function(element) {
        element.classList.remove('is-invalid');
        const errorDiv = element.parentNode.querySelector('.invalid-feedback');
        if (errorDiv) {
            errorDiv.remove();
        }
    },

    validateForm: function(formElement) {
        let isValid = true;
        
        // Check all required fields
        const requiredFields = formElement.querySelectorAll('[required]');
        requiredFields.forEach(field => {
            if (!this.validateRequired(field)) {
                isValid = false;
            }
        });

        // Check email fields
        const emailFields = formElement.querySelectorAll('input[type="email"]');
        emailFields.forEach(field => {
            if (field.value && !this.validateEmail(field)) {
                isValid = false;
            }
        });

        // Check number fields
        const numberFields = formElement.querySelectorAll('input[type="number"]');
        numberFields.forEach(field => {
            if (field.value && !this.validateNumber(field)) {
                isValid = false;
            }
        });

        return isValid;
    }
};

// Initialize the application
SupabaseApp.init();