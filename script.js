// Boston Parking Analyzer - Fixed Version

class ParkingAnalyzer {
    constructor() {
        this.isAnalyzed = false;
        this.currentLanguage = 'en';
        
        this.translations = [
            "Select your language:",
            "Selecciona tu idioma:",
            "选择你的语言:",
            "Selecione seu idioma:"
        ];
        
        this.init();
    }

    init() {
        console.log('Initializing ParkingAnalyzer...');
        this.setupEventListeners();
        this.startRotatingText();
    }

    setupEventListeners() {
        console.log('Setting up event listeners...');
        
        // File input handling
        const fileInput = document.getElementById('file-input');
        const uploadButton = document.getElementById('upload-button');
        
        if (uploadButton && fileInput) {
            uploadButton.addEventListener('click', () => {
                console.log('Upload button clicked');
                fileInput.click();
            });
            
            fileInput.addEventListener('change', (event) => {
                console.log('File selected');
                this.handleFileUpload(event);
            });
        } else {
            console.error('Upload button or file input not found');
        }

        // Language selection
        const languageSelect = document.getElementById('language-select');
        if (languageSelect) {
            languageSelect.addEventListener('change', (event) => {
                console.log('Language changed to:', event.target.value);
                this.currentLanguage = event.target.value;
            });
        }

        // Action buttons
        const reminderButton = document.getElementById('reminder-button');
        const reportButton = document.getElementById('report-button');
        
        if (reminderButton) {
            reminderButton.addEventListener('click', () => {
                this.handleReminderRequest();
            });
        }
        
        if (reportButton) {
            reportButton.addEventListener('click', () => {
                this.handleReportIssue();
            });
        }
    }

    startRotatingText() {
        console.log('Starting text rotation...');
        let currentIndex = 0;
        const rotatingElement = document.getElementById('rotating-text');
        
        if (!rotatingElement) {
            console.error('Rotating text element not found');
            return;
        }

        // Start rotation immediately and then repeat
        setInterval(() => {
            currentIndex = (currentIndex + 1) % this.translations.length;
            rotatingElement.textContent = this.translations[currentIndex];
            console.log('Text rotated to:', this.translations[currentIndex]);
        }, 2000);
    }

    async handleFileUpload(event) {
        const file = event.target.files[0];
        if (!file) {
            console.log('No file selected');
            return;
        }

        console.log('Processing file:', file.name);

        // Reset state
        this.resetAnalysis();
        
        // Display the image
        this.displayUploadedImage(file);
        
        // Show loading state
        this.showLoading();
        
        try {
            // Simulate analysis (replace with real API call later)
            const result = await this.simulateAnalysis();
            this.showResults(result);
            this.showActionButtons();
            this.isAnalyzed = true;
            
        } catch (error) {
            console.error('Analysis failed:', error);
            this.showError('Something went wrong during analysis. Please try again.');
        }
    }

    displayUploadedImage(file) {
        const imageElement = document.getElementById('uploaded-image');
        const placeholder = document.getElementById('upload-placeholder');
        
        if (!imageElement || !placeholder) {
            console.error('Image elements not found');
            return;
        }

        const imageUrl = URL.createObjectURL(file);
        imageElement.src = imageUrl;
        imageElement.classList.remove('hidden');
        placeholder.classList.add('hidden');
        
        console.log('Image displayed');
    }

    resetAnalysis() {
        console.log('Resetting analysis...');
        this.isAnalyzed = false;
        this.hideResults();
        this.hideActionButtons();
        this.showUploadButton();
    }

    showLoading() {
        console.log('Showing loading state...');
        const resultsSection = document.getElementById('results-section');
        const loading = document.getElementById('loading');
        const error = document.getElementById('error');
        const results = document.getElementById('results');
        
        if (resultsSection) resultsSection.classList.remove('hidden');
        if (loading) loading.classList.remove('hidden');
        if (error) error.classList.add('hidden');
        if (results) results.classList.add('hidden');
    }

    showResults(resultText) {
        console.log('Showing results:', resultText);
        const loading = document.getElementById('loading');
        const results = document.getElementById('results');
        const resultsText = document.getElementById('results-text');
        
        if (loading) loading.classList.add('hidden');
        if (results) results.classList.remove('hidden');
        if (resultsText) resultsText.textContent = resultText;
    }

    showError(errorMessage) {
        console.log('Showing error:', errorMessage);
        const loading = document.getElementById('loading');
        const error = document.getElementById('error');
        const results = document.getElementById('results');
        
        if (loading) loading.classList.add('hidden');
        if (error) {
            error.classList.remove('hidden');
            const errorText = error.querySelector('p');
            if (errorText) errorText.textContent = errorMessage;
        }
        if (results) results.classList.add('hidden');
    }

    hideResults() {
        const resultsSection = document.getElementById('results-section');
        if (resultsSection) resultsSection.classList.add('hidden');
    }

    showActionButtons() {
        console.log('Showing action buttons...');
        const uploadContainer = document.getElementById('upload-button-container');
        const actionButtons = document.getElementById('action-buttons');
        
        if (uploadContainer) uploadContainer.classList.add('hidden');
        if (actionButtons) {
            actionButtons.classList.remove('hidden');
            actionButtons.classList.add('flex');
        }
    }

    hideActionButtons() {
        const actionButtons = document.getElementById('action-buttons');
        if (actionButtons) {
            actionButtons.classList.add('hidden');
            actionButtons.classList.remove('flex');
        }
    }

    showUploadButton() {
        const uploadContainer = document.getElementById('upload-button-container');
        if (uploadContainer) uploadContainer.classList.remove('hidden');
    }

    async simulateAnalysis() {
        console.log('Starting analysis simulation...');
        // Mock implementation - replace with real API call later
        return new Promise((resolve) => {
            setTimeout(() => {
                const result = "You can park here - but be sure to move your car by 5:00pm! After that, this space will become a valet zone.";
                console.log('Analysis complete:', result);
                resolve(result);
            }, 2000);
        });
    }

    async handleReminderRequest() {
        console.log('Reminder requested');
        alert('Reminder feature coming soon!');
    }

    async handleReportIssue() {
        console.log('Issue report requested');
        alert('Issue reporting feature coming soon!');
    }
}

// Initialize the app when the page loads
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded, starting app...');
    new ParkingAnalyzer();
});

// Also try to initialize immediately in case DOMContentLoaded already fired
if (document.readyState === 'loading') {
    // Document is still loading, wait for DOMContentLoaded
    console.log('Document still loading, waiting for DOMContentLoaded...');
} else {
    // Document has already loaded
    console.log('Document already loaded, starting app immediately...');
    new ParkingAnalyzer();
}