document.addEventListener('DOMContentLoaded', () => {
    // 1. Dashboard Tab Switcher (For Custom Admin Dashboard & Student Panel)
    const tabButtons = document.querySelectorAll('[data-tab]');
    const tabContents = document.querySelectorAll('.tab-content');

    if (tabButtons.length > 0 && tabContents.length > 0) {
        // Read URL query parameter or active localStorage tab
        const urlParams = new URLSearchParams(window.location.search);
        let activeTab = urlParams.get('tab') || localStorage.getItem('ctrla_active_tab') || tabButtons[0].getAttribute('data-tab');

        // Check if such tab exists
        const checkTab = document.getElementById(activeTab);
        if (!checkTab) {
            activeTab = tabButtons[0].getAttribute('data-tab');
        }

        const switchTab = (tabId) => {
            // Hide all tab contents
            tabContents.forEach(content => {
                content.classList.remove('active');
            });

            // Deactivate all tab buttons
            tabButtons.forEach(btn => {
                btn.classList.remove('active');
            });

            // Show selected tab content
            const targetContent = document.getElementById(tabId);
            if (targetContent) {
                targetContent.classList.add('active');
            }

            // Activate corresponding button
            const targetBtn = document.querySelector(`[data-tab="${tabId}"]`);
            if (targetBtn) {
                targetBtn.classList.add('active');
            }

            // Save active tab in local storage
            localStorage.setItem('ctrla_active_tab', tabId);
        };

        // Initialize active tab
        switchTab(activeTab);

        // Bind click event
        tabButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                const targetTab = btn.getAttribute('data-tab');
                switchTab(targetTab);
            });
        });
    }

    // 2. Attendance Radial Gauge Animation
    const gaugeFill = document.querySelector('.gauge-fill');
    if (gaugeFill) {
        const percentage = parseFloat(gaugeFill.getAttribute('data-percentage')) || 0;
        const radius = 75;
        const circumference = 2 * Math.PI * radius; // 471.23

        // Set initial SVG properties
        gaugeFill.style.strokeDasharray = circumference;
        gaugeFill.style.strokeDashoffset = circumference;

        // Animate stroke dashoffset to percentage value after rendering
        setTimeout(() => {
            const offset = circumference - (percentage / 100) * circumference;
            gaugeFill.style.strokeDashoffset = offset;
        }, 150);
    }
});
