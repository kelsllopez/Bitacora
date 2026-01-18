document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('internaForm');
    const submitBtn = document.getElementById('submitBtn');
    const fechaInput = form.querySelector('input[type="date"]');

    const today = new Date().toISOString().split('T')[0];
    if (fechaInput) fechaInput.max = today;

    form.addEventListener('input', () => {
        submitBtn.disabled = !form.checkValidity();
    });
});