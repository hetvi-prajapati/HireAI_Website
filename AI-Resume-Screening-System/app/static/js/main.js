document.addEventListener('DOMContentLoaded', () => {
    // Basic interaction for flash messages
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });

    // File upload preview logic
    const fileInput = document.getElementById('resume-upload');
    const fileNameDisplay = document.getElementById('file-name-display');
    
    if (fileInput && fileNameDisplay) {
        fileInput.addEventListener('change', function(e) {
            if (this.files && this.files.length > 0) {
                fileNameDisplay.textContent = this.files[0].name;
                fileNameDisplay.classList.remove('d-none');
            } else {
                fileNameDisplay.textContent = '';
                fileNameDisplay.classList.add('d-none');
            }
        });
    }

    // Initialize tooltips (if using Bootstrap)
    if (typeof bootstrap !== 'undefined') {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
});
