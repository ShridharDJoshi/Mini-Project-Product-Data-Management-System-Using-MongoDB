// Authentication tab switching
function showTab(tabName) {
    // Hide all forms
    document.querySelectorAll('.auth-form').forEach(form => {
        form.classList.remove('active');
    });
    
    // Remove active class from all tabs
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected form and activate tab
    document.getElementById(tabName + '-form').classList.add('active');
    event.target.classList.add('active');
}

// Character counter for textareas
document.addEventListener('DOMContentLoaded', function() {
    const textareas = document.querySelectorAll('textarea[maxlength]');
    
    textareas.forEach(textarea => {
        const counter = textarea.parentNode.querySelector('.char-counter');
        if (counter) {
            // Update counter on input
            textarea.addEventListener('input', function() {
                const current = this.value.length;
                const max = this.getAttribute('maxlength');
                counter.textContent = `${current}/${max} characters`;
                
                // Add warning class if near limit
                if (current > max * 0.9) {
                    counter.style.color = '#dc3545';
                } else {
                    counter.style.color = '#666';
                }
            });
            
            // Initial count
            textarea.dispatchEvent(new Event('input'));
        }
    });
});

// Product search functionality
function filterProducts() {
    const searchValue = document.getElementById('search').value.toLowerCase();
    const rows = document.querySelectorAll('.product-row');
    
    rows.forEach(row => {
        const productName = row.getAttribute('data-name');
        if (productName.includes(searchValue)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}

// Product sorting functionality
function sortProducts() {
    const sortBy = document.getElementById('sort').value;
    const table = document.getElementById('productsTable');
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('.product-row'));
    
    rows.sort((a, b) => {
        let aVal, bVal;
        
        switch(sortBy) {
            case 'name':
                aVal = a.getAttribute('data-name');
                bVal = b.getAttribute('data-name');
                return aVal.localeCompare(bVal);
                
            case 'value':
                aVal = parseFloat(a.getAttribute('data-value'));
                bVal = parseFloat(b.getAttribute('data-value'));
                return bVal - aVal; // Descending order
                
            case 'date':
                aVal = parseFloat(a.getAttribute('data-date'));
                bVal = parseFloat(b.getAttribute('data-date'));
                return bVal - aVal; // Most recent first
                
            default:
                return 0;
        }
    });
    
    // Remove existing rows
    rows.forEach(row => row.remove());
    
    // Add sorted rows
    rows.forEach(row => tbody.appendChild(row));
}

// Toggle description visibility
function toggleDescription(button) {
    const descText = button.parentNode.querySelector('.description-text');
    const fullDesc = button.parentNode.querySelector('.full-description');
    
    if (fullDesc.style.display === 'none') {
        fullDesc.style.display = 'block';
        descText.style.display = 'none';
        button.textContent = 'Show Less';
    } else {
        fullDesc.style.display = 'none';
        descText.style.display = 'block';
        button.textContent = 'Show More';
    }
}

// Form validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    const inputs = form.querySelectorAll('input[required], textarea[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.style.borderColor = '#dc3545';
            isValid = false;
        } else {
            input.style.borderColor = '#ddd';
        }
    });
    
    // Password confirmation check
    if (formId === 'register-form') {
        const password = form.querySelector('[name="password"]').value;
        const confirmPassword = form.querySelector('[name="confirm_password"]').value;
        
        if (password !== confirmPassword) {
            form.querySelector('[name="confirm_password"]').style.borderColor = '#dc3545';
            alert('Passwords do not match!');
            isValid = false;
        }
    }
    
    return isValid;
}

// Auto-hide flash messages
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.remove();
            }, 300);
        }, 5000);
    });
});

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});