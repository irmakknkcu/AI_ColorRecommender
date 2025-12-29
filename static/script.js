// ========================================
// COLOR STUDIO - Main Script
// ========================================

// DOM Elements
const uploadBox = document.getElementById('uploadBox');
const imageInput = document.getElementById('imageInput');
const previewContainer = document.getElementById('previewContainer');
const previewImage = document.getElementById('previewImage');
const analyzeBtn = document.getElementById('analyzeBtn');

// File Input Handler
imageInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) displayPreview(file);
});

// Upload Box Click
uploadBox.addEventListener('click', () => imageInput.click());

// Drag & Drop
uploadBox.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadBox.classList.add('dragover');
});

uploadBox.addEventListener('dragleave', (e) => {
    e.preventDefault();
    uploadBox.classList.remove('dragover');
});

uploadBox.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadBox.classList.remove('dragover');
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
        imageInput.files = e.dataTransfer.files;
        displayPreview(file);
    }
});

// Display Preview
function displayPreview(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImage.src = e.target.result;
        previewContainer.style.display = 'block';
        analyzeBtn.style.display = 'flex';
        uploadBox.querySelector('.upload-content').style.display = 'none';
    };
    reader.readAsDataURL(file);
}

// Clear Preview
function clearPreview() {
    previewImage.src = '';
    previewContainer.style.display = 'none';
    analyzeBtn.style.display = 'none';
    imageInput.value = '';
    uploadBox.querySelector('.upload-content').style.display = 'block';
}

// Analyze Image
async function analyzeImage() {
    const file = imageInput.files[0];
    if (!file) {
        showError('Please select an image');
        return;
    }
    
    // Show loading
    document.getElementById('uploadSection').style.display = 'none';
    document.getElementById('loadingSection').style.display = 'flex';
    document.getElementById('resultsSection').style.display = 'none';
    document.getElementById('errorSection').style.display = 'none';
    
    const formData = new FormData();
    formData.append('image', file);
    
    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'An error occurred');
        }
        
        displayResults(data);
        
    } catch (error) {
        showError(error.message);
    }
}

// Display Results
function displayResults(data) {
    document.getElementById('loadingSection').style.display = 'none';
    document.getElementById('resultsSection').style.display = 'block';
    
    // Set image
    document.getElementById('resultImage').src = data.image_base64;
    
    // Display dominant colors
    displayDominantColors(data);
    
    // Display parsed data if available
    if (data.parsed_data) {
        displayParsedResults(data.parsed_data);
        document.getElementById('fallbackAnalysis').style.display = 'none';
    } else {
        // Fallback
        document.getElementById('analysisContent').textContent = data.analysis;
        document.getElementById('fallbackAnalysis').style.display = 'block';
        hideAllCards();
    }
    
    // Scroll to results
    document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Display Dominant Colors
function displayDominantColors(data) {
    const palette = document.getElementById('colorPalette');
    palette.innerHTML = '';
    
    const colors = data.parsed_data?.dominant_colors || 
                   (data.dominant_colors?.map((hex, i) => ({
                       hex: `#${hex}`,
                       name: `Color ${i + 1}`,
                       percentage: null
                   })) || []);
    
    colors.forEach(color => {
        const hex = color.hex || '#000000';
        const item = document.createElement('div');
        item.className = 'color-item';
        item.onclick = () => copyToClipboard(hex);
        
        item.innerHTML = `
            <div class="color-swatch" style="background-color: ${hex}"></div>
            <div class="color-info">
                <div class="color-name">${color.name || 'Color'}</div>
                <div class="color-code">${hex.toUpperCase()}</div>
                ${color.percentage ? `<div class="color-percent">${color.percentage}%</div>` : ''}
            </div>
        `;
        
        palette.appendChild(item);
    });
}

// Display Parsed Results
function displayParsedResults(parsed) {
    // Wall Colors
    if (parsed.wall_colors && parsed.wall_colors.length > 0) {
        const card = document.getElementById('wallColorsCard');
        const list = document.getElementById('wallColorsList');
        list.innerHTML = '';
        
        parsed.wall_colors.forEach(color => {
            const hex = color.hex || '#000000';
            const item = document.createElement('div');
            item.className = 'wall-color-item';
            item.innerHTML = `
                <div class="wall-swatch" style="background-color: ${hex}" onclick="copyToClipboard('${hex}')"></div>
                <div class="wall-info">
                    <div class="wall-name">${color.name || 'Suggested Color'}</div>
                    <div class="wall-code">${hex.toUpperCase()}</div>
                    <div class="wall-reason">${color.reason || ''}</div>
                </div>
            `;
            list.appendChild(item);
        });
        
        card.style.display = 'block';
    } else {
        document.getElementById('wallColorsCard').style.display = 'none';
    }
    
    // Decoration Tips
    if (parsed.decoration_tips && parsed.decoration_tips.length > 0) {
        const card = document.getElementById('tipsCard');
        const list = document.getElementById('tipsList');
        list.innerHTML = '';
        
        parsed.decoration_tips.forEach(tip => {
            const item = document.createElement('div');
            item.className = 'tip-item';
            item.textContent = tip;
            list.appendChild(item);
        });
        
        card.style.display = 'block';
    } else {
        document.getElementById('tipsCard').style.display = 'none';
    }
    
    // Furniture
    if (parsed.furniture_colors && parsed.furniture_colors.length > 0) {
        const card = document.getElementById('furnitureCard');
        const list = document.getElementById('furnitureList');
        list.innerHTML = '';
        
        parsed.furniture_colors.forEach(item => {
            const el = document.createElement('div');
            el.className = 'list-item';
            el.textContent = item;
            list.appendChild(el);
        });
        
        card.style.display = 'block';
    } else {
        document.getElementById('furnitureCard').style.display = 'none';
    }
    
    // Accessories
    if (parsed.accessories_colors && parsed.accessories_colors.length > 0) {
        const card = document.getElementById('accessoriesCard');
        const list = document.getElementById('accessoriesList');
        list.innerHTML = '';
        
        parsed.accessories_colors.forEach(item => {
            const el = document.createElement('div');
            el.className = 'list-item';
            el.textContent = item;
            list.appendChild(el);
        });
        
        card.style.display = 'block';
    } else {
        document.getElementById('accessoriesCard').style.display = 'none';
    }
    
    // Harmony
    if (parsed.color_harmony) {
        document.getElementById('harmonyCard').style.display = 'block';
        document.getElementById('harmonyText').textContent = parsed.color_harmony;
    } else {
        document.getElementById('harmonyCard').style.display = 'none';
    }
    
    // Summary
    if (parsed.summary) {
        document.getElementById('summaryCard').style.display = 'block';
        document.getElementById('summaryText').textContent = parsed.summary;
    } else {
        document.getElementById('summaryCard').style.display = 'none';
    }
}

// Hide All Cards
function hideAllCards() {
    document.getElementById('wallColorsCard').style.display = 'none';
    document.getElementById('tipsCard').style.display = 'none';
    document.getElementById('furnitureCard').style.display = 'none';
    document.getElementById('accessoriesCard').style.display = 'none';
    document.getElementById('harmonyCard').style.display = 'none';
    document.getElementById('summaryCard').style.display = 'none';
}

// Show Error
function showError(message) {
    document.getElementById('loadingSection').style.display = 'none';
    document.getElementById('uploadSection').style.display = 'flex';
    document.getElementById('errorSection').style.display = 'flex';
    document.getElementById('errorMessage').textContent = message;
}

// Reset App
function resetApp() {
    document.getElementById('uploadSection').style.display = 'flex';
    document.getElementById('loadingSection').style.display = 'none';
    document.getElementById('resultsSection').style.display = 'none';
    document.getElementById('errorSection').style.display = 'none';
    clearPreview();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Copy to Clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast(`Copied: ${text}`);
    });
}

// Show Toast
function showToast(message) {
    const container = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = 'toast success';
    toast.textContent = message;
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s var(--ease-out) forwards';
        setTimeout(() => toast.remove(), 300);
    }, 2500);
}
