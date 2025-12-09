// Drag and Drop Upload
const uploadArea = document.getElementById('uploadArea');
const resumeInput = document.getElementById('resumeInput');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const submitBtn = document.getElementById('submitBtn');

if (uploadArea) {
    uploadArea.addEventListener('click', () => {
        resumeInput.click();
    });

    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            resumeInput.files = files;
            handleFileSelect();
        }
    });

    resumeInput.addEventListener('change', handleFileSelect);
}

function handleFileSelect() {
    const file = resumeInput.files[0];
    if (file) {
        const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
        
        if (!validTypes.includes(file.type)) {
            alert('Please upload a PDF or DOCX file');
            resumeInput.value = '';
            fileInfo.style.display = 'none';
            submitBtn.disabled = true;
            return;
        }

        fileName.textContent = file.name;
        fileInfo.style.display = 'block';
        submitBtn.disabled = false;
    }
}

// Filter and Sort Jobs
const matchFilter = document.getElementById('matchFilter');
const sortFilter = document.getElementById('sortFilter');

if (matchFilter) {
    matchFilter.addEventListener('change', filterAndSortJobs);
}

if (sortFilter) {
    sortFilter.addEventListener('change', filterAndSortJobs);
}

function filterAndSortJobs() {
    const matchValue = matchFilter.value;
    const sortValue = sortFilter.value;
    const jobCards = document.querySelectorAll('.job-card');
    const jobsContainer = document.getElementById('jobsContainer');
    
    let visibleCards = [];

    jobCards.forEach(card => {
        const matchScore = parseInt(card.dataset.match);
        let show = true;

        if (matchValue === 'high' && matchScore < 8) show = false;
        if (matchValue === 'medium' && (matchScore < 4 || matchScore >= 8)) show = false;
        if (matchValue === 'low' && matchScore >= 4) show = false;

        card.style.display = show ? 'block' : 'none';
        if (show) visibleCards.push(card);
    });

    if (sortValue === 'title') {
        visibleCards.sort((a, b) => {
            const titleA = a.querySelector('h5').textContent;
            const titleB = b.querySelector('h5').textContent;
            return titleA.localeCompare(titleB);
        });

        visibleCards.forEach(card => {
            jobsContainer.appendChild(card);
        });
    }
}

// Apply Job Function
function applyJob(jobTitle) {
    alert(`Application submitted for: ${jobTitle}\n\nThank you for your interest! We'll review your application shortly.`);
}

// Animate Progress Bars on Page Load
window.addEventListener('load', () => {
    const progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach(bar => {
        const width = bar.style.width;
        bar.style.width = '0';
        setTimeout(() => {
            bar.style.transition = 'width 1.5s ease-out';
            bar.style.width = width;
        }, 100);
    });
});

// Smooth Scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add active state to navbar links
document.addEventListener('DOMContentLoaded', () => {
    const currentLocation = location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentLocation) {
            link.classList.add('active');
        }
    });
});

// Tooltip initialization (if using Bootstrap tooltips)
const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
});
