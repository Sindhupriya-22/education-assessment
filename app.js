// Career Guidance Platform - Main JavaScript File

document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Form validation and enhancement
    const forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Assessment form enhancements
    const assessmentForm = document.getElementById('assessmentForm');
    if (assessmentForm) {
        initializeAssessmentForm();
    }

    // Results page enhancements
    if (document.querySelector('.results-page')) {
        initializeResultsPage();
    }

    // Language switching
    initializeLanguageSwitching();

    // Mobile optimizations
    initializeMobileOptimizations();
});

function initializeAssessmentForm() {
    const form = document.getElementById('assessmentForm');
    const sections = form.querySelectorAll('.section-header');
    
    // Add progress indicator
    addProgressIndicator(sections.length);
    
    // Form sections navigation
    let currentSection = 0;
    const totalSections = sections.length;
    
    // Track form completion progress
    const inputs = form.querySelectorAll('input[required], select[required]');
    let completedInputs = 0;
    
    inputs.forEach(input => {
        input.addEventListener('change', function() {
            updateProgress();
            validateSection(this);
        });
    });
    
    function updateProgress() {
        const completed = Array.from(inputs).filter(input => {
            if (input.type === 'radio') {
                return input.name && form.querySelector(`input[name="${input.name}"]:checked`);
            }
            return input.value.trim() !== '';
        }).length;
        
        const progressPercent = (completed / inputs.length) * 100;
        const progressBar = document.querySelector('.assessment-progress');
        if (progressBar) {
            progressBar.style.width = progressPercent + '%';
            progressBar.setAttribute('aria-valuenow', progressPercent);
        }
    }
    
    function validateSection(input) {
        const section = input.closest('.section-header').nextElementSibling;
        if (section) {
            const sectionInputs = section.querySelectorAll('input[required], select[required]');
            const sectionComplete = Array.from(sectionInputs).every(inp => {
                if (inp.type === 'radio') {
                    return form.querySelector(`input[name="${inp.name}"]:checked`);
                }
                return inp.value.trim() !== '';
            });
            
            if (sectionComplete) {
                section.classList.add('section-complete');
            } else {
                section.classList.remove('section-complete');
            }
        }
    }
    
    // Form submission enhancement
    form.addEventListener('submit', function(e) {
        const submitBtn = form.querySelector('button[type="submit"]');
        if (submitBtn) {
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing your assessment...';
            submitBtn.disabled = true;
        }
        
        // Show loading overlay
        showLoadingOverlay('Analyzing your profile and generating recommendations...');
    });
}

function addProgressIndicator(totalSections) {
    const progressHTML = `
        <div class="progress mb-4" style="height: 8px;">
            <div class="progress-bar assessment-progress" role="progressbar" 
                 style="width: 0%" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100">
            </div>
        </div>
    `;
    
    const form = document.getElementById('assessmentForm');
    const firstSection = form.querySelector('.section-header');
    if (firstSection) {
        firstSection.insertAdjacentHTML('beforebegin', progressHTML);
    }
}

function initializeResultsPage() {
    // Animate career cards on scroll
    const careerCards = document.querySelectorAll('.career-recommendation-card');
    
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
            }
        });
    }, observerOptions);
    
    careerCards.forEach(card => {
        observer.observe(card);
    });
    
    // Enhanced chart interactions
    initializeChartInteractions();
}

function initializeChartInteractions() {
    // Add click handlers for chart elements
    const charts = document.querySelectorAll('canvas[id*="Chart"]');
    
    charts.forEach(chart => {
        chart.addEventListener('click', function(evt) {
            const activePoints = Chart.getChart(chart).getElementsAtEventForMode(evt, 'nearest', { intersect: true }, true);
            
            if (activePoints.length > 0) {
                const chartData = Chart.getChart(chart).data;
                const datasetIndex = activePoints[0].datasetIndex;
                const index = activePoints[0].index;
                const label = chartData.labels[index];
                
                // Show career details for clicked segment
                showCareerQuickView(label);
            }
        });
    });
}

function showCareerQuickView(careerName) {
    // Find career card with matching name
    const careerCards = document.querySelectorAll('.career-card');
    
    careerCards.forEach(card => {
        const cardTitle = card.querySelector('.card-title');
        if (cardTitle && cardTitle.textContent.trim() === careerName) {
            card.scrollIntoView({ behavior: 'smooth', block: 'center' });
            card.classList.add('highlight-card');
            
            setTimeout(() => {
                card.classList.remove('highlight-card');
            }, 2000);
        }
    });
}

function initializeLanguageSwitching() {
    const langSwitcher = document.querySelector('.language-switcher');
    if (langSwitcher) {
        langSwitcher.addEventListener('change', function(e) {
            const selectedLang = e.target.value;
            const currentUrl = new URL(window.location);
            currentUrl.searchParams.set('lang', selectedLang);
            window.location.href = currentUrl.toString();
        });
    }
}

function initializeMobileOptimizations() {
    // Optimize for touch devices
    if ('ontouchstart' in window) {
        document.body.classList.add('touch-device');
        
        // Improve button tap targets
        const buttons = document.querySelectorAll('.btn');
        buttons.forEach(btn => {
            btn.style.minHeight = '44px';
        });
    }
    
    // Handle orientation changes
    window.addEventListener('orientationchange', function() {
        setTimeout(() => {
            // Recalculate chart sizes
            const charts = document.querySelectorAll('canvas');
            charts.forEach(chart => {
                const chartInstance = Chart.getChart(chart);
                if (chartInstance) {
                    chartInstance.resize();
                }
            });
        }, 100);
    });
    
    // Optimize scrolling performance
    let ticking = false;
    
    function updateScrollElements() {
        // Update navigation state based on scroll position
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 100) {
            navbar.classList.add('navbar-scrolled');
        } else {
            navbar.classList.remove('navbar-scrolled');
        }
        
        ticking = false;
    }
    
    window.addEventListener('scroll', function() {
        if (!ticking) {
            requestAnimationFrame(updateScrollElements);
            ticking = true;
        }
    });
}

function showLoadingOverlay(message = 'Loading...') {
    const overlay = document.createElement('div');
    overlay.className = 'loading-overlay';
    overlay.innerHTML = `
        <div class="loading-content">
            <div class="spinner-border text-primary mb-3" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <p class="mb-0">${message}</p>
        </div>
    `;
    
    document.body.appendChild(overlay);
    
    // Add CSS for overlay
    if (!document.querySelector('#loading-overlay-styles')) {
        const style = document.createElement('style');
        style.id = 'loading-overlay-styles';
        style.textContent = `
            .loading-overlay {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.8);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 9999;
                backdrop-filter: blur(3px);
            }
            .loading-content {
                text-align: center;
                color: white;
                padding: 2rem;
                border-radius: 8px;
                background: rgba(0, 0, 0, 0.5);
            }
            .highlight-card {
                box-shadow: 0 0 20px rgba(241, 89, 229, 0.7);
                transform: scale(1.02);
                transition: all 0.3s ease;
            }
            .navbar-scrolled {
                background-color: rgba(var(--bs-dark-rgb), 0.95) !important;
                backdrop-filter: blur(10px);
            }
        `;
        document.head.appendChild(style);
    }
}

function hideLoadingOverlay() {
    const overlay = document.querySelector('.loading-overlay');
    if (overlay) {
        overlay.remove();
    }
}

// Utility functions
function debounce(func, wait, immediate) {
    let timeout;
    return function executedFunction() {
        const context = this;
        const args = arguments;
        const later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}

// Error handling
window.addEventListener('error', function(e) {
    console.error('Application error:', e.error);
    
    // Show user-friendly error message
    const toast = document.createElement('div');
    toast.className = 'toast align-items-center text-white bg-danger border-0';
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                Something went wrong. Please refresh the page and try again.
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    document.body.appendChild(toast);
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // Remove toast after it's hidden
    toast.addEventListener('hidden.bs.toast', function() {
        toast.remove();
    });
});

// Export functions for use in other scripts
window.CareerGuidanceApp = {
    showLoadingOverlay,
    hideLoadingOverlay,
    debounce,
    throttle
};