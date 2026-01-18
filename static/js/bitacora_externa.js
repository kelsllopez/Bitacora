document.addEventListener('DOMContentLoaded', function () {

    const form = document.querySelector('form.needs-validation');
    if (!form) return;

    const submitBtn = form.querySelector('button[type="submit"]');
    const fechaInput = form.querySelector('input[type="date"]');

    if (fechaInput) {
        const today = new Date().toISOString().split('T')[0];
        fechaInput.max = today;
    }

    if (submitBtn) {
        form.addEventListener('input', () => {
            submitBtn.disabled = !form.checkValidity();
        });
    }

});