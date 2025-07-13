// DOM Elements
const analyzeForm = document.getElementById('analyzeForm');
const vintedUrlInput = document.getElementById('vintedUrl');
const analyzeBtn = document.getElementById('analyzeBtn');
const loadingState = document.getElementById('loadingState');
const resultsSection = document.getElementById('resultsSection');
const errorState = document.getElementById('errorState');
const tryAnotherBtn = document.getElementById('tryAnotherBtn');
const retryBtn = document.getElementById('retryBtn');

// Result elements
const itemTitle = document.getElementById('itemTitle');
const itemPrice = document.getElementById('itemPrice');
const itemBrand = document.getElementById('itemBrand');
const itemCategory = document.getElementById('itemCategory');
const itemSize = document.getElementById('itemSize');
const itemCondition = document.getElementById('itemCondition');

const resellableResult = document.getElementById('resellableResult');
const profitResult = document.getElementById('profitResult');
const timeResult = document.getElementById('timeResult');
const priceResult = document.getElementById('priceResult');
const riskResult = document.getElementById('riskResult');

const similarItemsList = document.getElementById('similarItemsList');
const errorMessage = document.getElementById('errorMessage');

// State management
let currentUrl = '';

// Event Listeners
analyzeForm.addEventListener('submit', handleFormSubmit);
tryAnotherBtn.addEventListener('click', resetForm);
retryBtn.addEventListener('click', () => {
    if (currentUrl) {
        analyzeItem(currentUrl);
    }
});

// Form submission handler
async function handleFormSubmit(e) {
    e.preventDefault();
    
    const url = vintedUrlInput.value.trim();
    if (!url) {
        showError('Please enter a Vinted URL');
        return;
    }
    
    if (!url.includes('www.vinted')) {
        showError('Please enter a valid Vinted URL');
        return;
    }
    
    currentUrl = url;
    await analyzeItem(url);
}

// Main analysis function
async function analyzeItem(url) {
    try {
        // Show loading state
        showLoading();
        
        // Make API call
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to analyze item');
        }
        
        const data = await response.json();
        
        // Display results
        displayResults(data);
        
    } catch (error) {
        console.error('Analysis error:', error);
        showError(error.message || 'An error occurred while analyzing the item');
    }
}

// Display results
function displayResults(data) {
    // Hide loading and error states
    hideLoading();
    hideError();
    
    // Populate item details
    populateItemDetails(data.item_data);
    
    // Populate analysis results
    populateAnalysisResults(data.analysis);
    
    // Populate similar items
    populateSimilarItems(data.similar_items);
    
    // Show results
    showResults();
}

// Populate item details
function populateItemDetails(itemData) {
    itemTitle.textContent = itemData.title || 'N/A';
    itemPrice.textContent = itemData.price ? `€${itemData.price}` : 'N/A';
    itemBrand.textContent = itemData.brand || 'N/A';
    itemCategory.textContent = itemData.category || 'N/A';
    itemSize.textContent = itemData.size || 'N/A';
    itemCondition.textContent = itemData.condition || 'N/A';
}

// Populate analysis results
function populateAnalysisResults(analysis) {
    resellableResult.textContent = analysis.resellable || 'Unknown';
    profitResult.textContent = analysis.estimated_profit || 'Unknown';
    timeResult.textContent = analysis.time_to_sell || 'Unknown';
    priceResult.textContent = analysis.estimated_resale_price || 'Unknown';
    riskResult.textContent = analysis.risks || 'No risks identified';
    
    // Add visual indicators
    updateResellableIndicator(analysis.resellable);
}

// Update resellable indicator
function updateResellableIndicator(resellable) {
    const card = resellableResult.closest('.result-card');
    const icon = card.querySelector('.card-icon i');
    
    if (resellable && resellable.toLowerCase() === 'yes') {
        card.style.borderLeftColor = '#10b981';
        icon.style.color = '#10b981';
        icon.className = 'fas fa-check-circle';
    } else if (resellable && resellable.toLowerCase() === 'no') {
        card.style.borderLeftColor = '#ef4444';
        icon.style.color = '#ef4444';
        icon.className = 'fas fa-times-circle';
    } else {
        card.style.borderLeftColor = '#f59e0b';
        icon.style.color = '#f59e0b';
        icon.className = 'fas fa-question-circle';
    }
}

// Populate similar items
function populateSimilarItems(similarItems) {
    if (!similarItems || similarItems.length === 0) {
        similarItemsList.innerHTML = '<p style="color: #64748b; text-align: center;">No similar items found</p>';
        return;
    }
    
    const itemsHTML = similarItems.map(item => `
        <div class="similar-item">
            <h4>${item.title}</h4>
            <div class="similar-item-details">
                <span>Brand: <strong>${item.brand}</strong></span>
                <span>Category: <strong>${item.category}</strong></span>
                <span>Size: <strong>${item.size}</strong></span>
                <span>Condition: <strong>${item.condition}</strong></span>
                <span>Original Price: <strong>€${item.original_price}</strong></span>
                <span>Sold Price: <strong>€${item.sold_price}</strong></span>
                <span>Days to Sell: <strong>${item.days_to_sell}</strong></span>
                <span>Profit: <strong>€${item.sold_price - item.original_price}</strong></span>
            </div>
        </div>
    `).join('');
    
    similarItemsList.innerHTML = itemsHTML;
}

// Reset form
function resetForm() {
    // Clear form
    analyzeForm.reset();
    
    // Hide all states
    hideLoading();
    hideError();
    hideResults();
    
    // Reset current URL
    currentUrl = '';
    
    // Reset button states
    analyzeBtn.disabled = false;
    analyzeBtn.innerHTML = '<i class="fas fa-search"></i><span>Check Resell Value</span>';
}

// Show loading state
function showLoading() {
    hideError();
    hideResults();
    loadingState.classList.remove('hidden');
    analyzeBtn.disabled = true;
    analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i><span>Analyzing...</span>';
}

// Hide loading state
function hideLoading() {
    loadingState.classList.add('hidden');
    analyzeBtn.disabled = false;
    analyzeBtn.innerHTML = '<i class="fas fa-search"></i><span>Check Resell Value</span>';
}

// Show results
function showResults() {
    resultsSection.classList.remove('hidden');
}

// Hide results
function hideResults() {
    resultsSection.classList.add('hidden');
}

// Show error
function showError(message) {
    hideLoading();
    hideResults();
    errorMessage.textContent = message;
    errorState.classList.remove('hidden');
}

// Hide error
function hideError() {
    errorState.classList.add('hidden');
}

// Utility function to format currency
function formatCurrency(amount) {
    if (typeof amount === 'string') {
        return amount;
    }
    return `€${amount.toFixed(2)}`;
}

// Add some nice animations
document.addEventListener('DOMContentLoaded', function() {
    // Add fade-in animation to form container
    const formContainer = document.querySelector('.form-container');
    formContainer.style.opacity = '0';
    formContainer.style.transform = 'translateY(20px)';
    
    setTimeout(() => {
        formContainer.style.transition = 'all 0.6s ease';
        formContainer.style.opacity = '1';
        formContainer.style.transform = 'translateY(0)';
    }, 100);
    
    // Add input focus effects
    vintedUrlInput.addEventListener('focus', function() {
        this.parentElement.style.transform = 'scale(1.02)';
    });
    
    vintedUrlInput.addEventListener('blur', function() {
        this.parentElement.style.transform = 'scale(1)';
    });
});

// Add keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + Enter to submit form
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        if (vintedUrlInput === document.activeElement) {
            analyzeForm.dispatchEvent(new Event('submit'));
        }
    }
    
    // Escape to reset form
    if (e.key === 'Escape') {
        resetForm();
    }
});

// Add URL validation
vintedUrlInput.addEventListener('input', function() {
    const url = this.value.trim();
    const isValid = url === '' || url.includes('www.vinted');
    
    if (!isValid) {
        this.style.borderColor = '#ef4444';
        this.style.backgroundColor = '#fef2f2';
    } else {
        this.style.borderColor = '#e2e8f0';
        this.style.backgroundColor = '#f7fafc';
    }
});

// Add copy to clipboard functionality for results
function addCopyFunctionality() {
    const resultValues = document.querySelectorAll('.result-value');
    resultValues.forEach(value => {
        value.style.cursor = 'pointer';
        value.title = 'Click to copy';
        value.addEventListener('click', function() {
            navigator.clipboard.writeText(this.textContent).then(() => {
                // Show a brief tooltip
                const originalText = this.textContent;
                this.textContent = 'Copied!';
                this.style.color = '#10b981';
                
                setTimeout(() => {
                    this.textContent = originalText;
                    this.style.color = '#1e293b';
                }, 1000);
            });
        });
    });
}

// Call copy functionality after results are displayed
const originalDisplayResults = displayResults;
displayResults = function(data) {
    originalDisplayResults(data);
    setTimeout(addCopyFunctionality, 100);
}; 