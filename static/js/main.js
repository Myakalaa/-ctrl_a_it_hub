document.addEventListener('DOMContentLoaded', () => {
    // 1. Sticky Navbar styling on scroll
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // 2. Mobile Nav Toggle
    const toggleBtn = document.querySelector('.nav-toggle');
    const navLinks = document.querySelector('.nav-links');
    if (toggleBtn && navLinks) {
        toggleBtn.addEventListener('click', () => {
            navLinks.classList.toggle('open');
            const icon = toggleBtn.querySelector('i');
            if (icon.classList.contains('fa-bars')) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-times');
            } else {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        });
    }

    // 3. Mobile Dropdown Toggle (for touch screens / mobile view)
    const dropdowns = document.querySelectorAll('.dropdown');
    dropdowns.forEach(dropdown => {
        const link = dropdown.querySelector('.nav-link');
        link.addEventListener('click', (e) => {
            if (window.innerWidth <= 768) {
                e.preventDefault(); // Stop navigation click on mobile to expand submenus
                dropdown.classList.toggle('open');
                
                // Close other dropdowns
                dropdowns.forEach(other => {
                    if (other !== dropdown) {
                        other.classList.remove('open');
                    }
                });
            }
        });
    });

    // 4. Hero Slider Rotation
    const slides = document.querySelectorAll('.hero-slide');
    if (slides.length > 0) {
        let currentSlide = 0;
        const slideInterval = 6000;

        const nextSlide = () => {
            slides[currentSlide].classList.remove('active');
            currentSlide = (currentSlide + 1) % slides.length;
            slides[currentSlide].classList.add('active');
        };

        const prevSlide = () => {
            slides[currentSlide].classList.remove('active');
            currentSlide = (currentSlide - 1 + slides.length) % slides.length;
            slides[currentSlide].classList.add('active');
        };

        let autoRotation = setInterval(nextSlide, slideInterval);

        const nextBtn = document.querySelector('.slider-arrow.next');
        const prevBtn = document.querySelector('.slider-arrow.prev');

        if (nextBtn && prevBtn) {
            nextBtn.addEventListener('click', () => {
                clearInterval(autoRotation);
                nextSlide();
                autoRotation = setInterval(nextSlide, slideInterval);
            });
            prevBtn.addEventListener('click', () => {
                clearInterval(autoRotation);
                prevSlide();
                autoRotation = setInterval(nextSlide, slideInterval);
            });
        }
    }

    // 5. Syllabus Expand Accordion
    const syllabusButtons = document.querySelectorAll('.syllabus-btn');
    syllabusButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const syllabusId = btn.getAttribute('data-target');
            const syllabusContent = document.getElementById(syllabusId);
            
            if (syllabusContent) {
                syllabusContent.classList.toggle('open');
                const icon = btn.querySelector('i');
                if (icon) {
                    if (syllabusContent.classList.contains('open')) {
                        icon.classList.remove('fa-chevron-down');
                        icon.classList.add('fa-chevron-up');
                    } else {
                        icon.classList.remove('fa-chevron-up');
                        icon.classList.add('fa-chevron-down');
                    }
                }
            }
        });
    });

    // 6. Interactive Circular Orbit Graphic Content Hub Changer
    const orbitNodes = document.querySelectorAll('.circle-node, .wheel-wedge');
    const centerHub = document.querySelector('.circle-center-hub');
    if (orbitNodes.length > 0 && centerHub) {
        // Save original logo content
        const originalLogoHTML = centerHub.innerHTML;

        const nodeData = {
            'node-1': { title: 'Placement', desc: '100% Job Referrals & Interviews', icon: 'fa-briefcase', color: '#0056b3' },
            'node-2': { title: 'Innovate', desc: 'Industrial Project Frameworks', icon: 'fa-lightbulb', color: '#f7941d' },
            'node-3': { title: 'Teaching', desc: 'Real-time Corporate Mentor Guides', icon: 'fa-chalkboard-teacher', color: '#e83e8c' },
            'node-4': { title: 'Skills', desc: 'Hands-on Coding Practice Sessions', icon: 'fa-tools', color: '#28a745' },
            'node-5': { title: 'Develop', desc: 'Full-stack Backend & Web Projects', icon: 'fa-laptop-code', color: '#0070ad' },
            'node-6': { title: 'Sharing', desc: 'Knowledge Forums & Code Reviews', icon: 'fa-share-alt', color: '#6f42c1' },
            'node-7': { title: 'Support', desc: '24/7 Digital Lab & Doubt Support', icon: 'fa-headset', color: '#17a2b8' },
            'node-8': { title: 'Mentor', desc: 'MNC Senior Developer Sessions', icon: 'fa-user-friends', color: '#fd7e14' },
            'node-9': { title: 'Guidance', desc: 'Mock HR Tests & Career Mapping', icon: 'fa-compass', color: '#e07b00' }
        };

        orbitNodes.forEach(node => {
            // Find which node class/attr it has
            let nodeKey = node.getAttribute('data-node');
            if (!nodeKey) {
                for (let i = 1; i <= 9; i++) {
                    if (node.classList.contains(`node-${i}`)) {
                        nodeKey = `node-${i}`;
                        break;
                    }
                }
            }

            if (nodeKey && nodeData[nodeKey]) {
                const data = nodeData[nodeKey];

                const showInfo = () => {
                    centerHub.innerHTML = `
                        <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; animation: fadeIn 0.3s ease;">
                            <i class="fas ${data.icon}" style="color:${data.color}; font-size:1.8rem; margin-bottom:0.25rem;"></i>
                            <h4 style="font-family:var(--font-main); font-size:0.75rem; font-weight:700; text-transform:uppercase; color:var(--text-dark); margin:2px 0;">${data.title}</h4>
                            <p style="font-size:0.58rem; color:var(--text-muted); line-height:1.2; margin:0; padding:0 2px;">${data.desc}</p>
                        </div>
                    `;
                };

                const resetInfo = () => {
                    centerHub.innerHTML = originalLogoHTML;
                };

                // Desktop Hover
                node.addEventListener('mouseenter', showInfo);
                node.addEventListener('mouseleave', resetInfo);

                // Mobile Touch support
                node.addEventListener('click', (e) => {
                    e.stopPropagation();
                    showInfo();
                });
            }
        });

        // Click outside center hub on mobile resets it
        document.addEventListener('click', () => {
            centerHub.innerHTML = originalLogoHTML;
        });
    }

    // 7. Hash offset scroll adjustments for sticky navbar compatibility
    const adjustHashScroll = () => {
        if (window.location.hash) {
            const target = document.querySelector(window.location.hash);
            if (target) {
                setTimeout(() => {
                    const elementPosition = target.getBoundingClientRect().top + window.scrollY;
                    window.scrollTo({
                        top: elementPosition - 110, // Offset matching navbar + top bar
                        behavior: 'smooth'
                    });
                }, 150);
            }
        }
    };
    window.addEventListener('load', adjustHashScroll);
    window.addEventListener('hashchange', adjustHashScroll);

    // 8. Scroll observer trigger for Interactive Wheel flying bubbles
    const visionSection = document.querySelector('.vision-section-wrapper');
    if (visionSection) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    visionSection.classList.add('active');
                    observer.unobserve(entry.target); // Trigger only once for performance
                }
            });
        }, { threshold: 0.15 });
        observer.observe(visionSection);
    }

    // 9. Dark/Light Theme Switcher Logic
    const themeToggleBtn = document.getElementById('themeToggleBtn');
    if (themeToggleBtn) {
        const themeIcon = themeToggleBtn.querySelector('i');
        
        // Update the button icon based on the current theme
        const updateThemeIcon = (theme) => {
            if (theme === 'dark') {
                themeIcon.className = 'fas fa-sun';
                themeToggleBtn.setAttribute('title', 'Switch to Light Theme');
            } else {
                themeIcon.className = 'fas fa-moon';
                themeToggleBtn.setAttribute('title', 'Switch to Dark Theme');
            }
        };

        // Set initial icon on load
        const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
        updateThemeIcon(currentTheme);

        // Click event listener
        themeToggleBtn.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('ctrla_theme', newTheme);
            updateThemeIcon(newTheme);
        });
    }
});
