document.addEventListener("DOMContentLoaded", () => {
    // Accordion headers
    document.querySelectorAll('.accordion-header').forEach(header => {
        header.addEventListener('click', () => {
            const item = header.parentElement;
            item.classList.toggle('active');
        });
    });

    // Auto-dismiss alerts after 3.5 seconds (3500 ms)
    const alerts = document.querySelectorAll('.messages .alert, .messages-container .alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = "opacity 0.6s ease, transform 0.6s ease, margin-bottom 0.6s ease, height 0.6s ease, padding 0.6s ease";
            alert.style.opacity = "0";
            alert.style.transform = "translateY(-10px)";
            
            setTimeout(() => {
                alert.style.height = "0";
                alert.style.padding = "0";
                alert.style.marginBottom = "0";
                setTimeout(() => {
                    alert.remove();
                    const container = alert.parentElement;
                    if (container && container.querySelectorAll('.alert').length === 0) {
                        container.remove();
                    }
                }, 300);
            }, 600);
        }, 3500);
    });
});