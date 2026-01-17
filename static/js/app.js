/**
 * App.js - Main Application Logic
 */

// DOM Elements
const storyInput = document.getElementById('storyInput');
const generateBtn = document.getElementById('generateBtn');
const clearBtn = document.getElementById('clearBtn');
const playBtn = document.getElementById('playBtn');
const pauseBtn = document.getElementById('pauseBtn');
const restartBtn = document.getElementById('restartBtn');
const downloadBtn = document.getElementById('downloadBtn');

const loadingState = document.getElementById('loadingState');
const emptyState = document.getElementById('emptyState');
const animationCanvas = document.getElementById('animationCanvas');
const animationControls = document.getElementById('animationControls');
const animationInfo = document.getElementById('animationInfo');

const svgCanvas = document.getElementById('svgCanvas');
const animationContent = document.getElementById('animationContent');
const animationText = document.getElementById('animationText');

const toast = document.getElementById('toast');

// Initialize Animator
const animator = new StickFigureAnimator(svgCanvas, animationContent, animationText);

// API Base URL
const API_BASE = window.location.origin;

/**
 * Show toast notification
 */
function showToast(message, type = 'info') {
    toast.textContent = message;
    toast.className = `toast ${type}`;
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

/**
 * Update UI state
 */
function updateUIState(state) {
    // Hide all states
    loadingState.style.display = 'none';
    emptyState.style.display = 'none';
    animationCanvas.style.display = 'none';
    animationControls.style.display = 'none';
    animationInfo.style.display = 'none';
    
    // Show requested state
    switch(state) {
        case 'loading':
            loadingState.style.display = 'block';
            generateBtn.disabled = true;
            break;
        case 'empty':
            emptyState.style.display = 'block';
            generateBtn.disabled = false;
            break;
        case 'animation':
            animationCanvas.style.display = 'block';
            animationControls.style.display = 'flex';
            animationInfo.style.display = 'block';
            generateBtn.disabled = false;
            break;
    }
}

/**
 * Generate animation from story
 */
async function generateAnimation() {
    const story = storyInput.value.trim();
    
    if (!story) {
        showToast('请输入故事内容', 'error');
        return;
    }
    
    updateUIState('loading');
    
    try {
        const response = await fetch(`${API_BASE}/api/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ story })
        });
        
        const result = await response.json();
        
        if (!result.success) {
            throw new Error(result.message || '生成失败');
        }
        
        // Load animation data
        animator.loadAnimation(result.data);
        
        // Update info display
        updateAnimationInfo(result.data);
        
        // Show animation
        updateUIState('animation');
        
        // Auto-play
        setTimeout(() => {
            animator.play();
        }, 500);
        
        showToast('动画生成成功！', 'success');
        
    } catch (error) {
        console.error('Generation error:', error);
        showToast(`生成失败: ${error.message}`, 'error');
        updateUIState('empty');
    }
}

/**
 * Update animation info display
 */
function updateAnimationInfo(data) {
    document.getElementById('infoTitle').textContent = data.title || '未命名';
    document.getElementById('infoDescription').textContent = data.description || '无描述';
    document.getElementById('infoScenes').textContent = data.scenes.length;
    document.getElementById('infoCharacters').textContent = data.characters.length;
}

/**
 * Clear input
 */
function clearInput() {
    storyInput.value = '';
    storyInput.focus();
}

/**
 * Load example story
 */
function loadExample(example) {
    storyInput.value = example;
    storyInput.focus();
}

/**
 * Download animation
 */
function downloadAnimation() {
    try {
        animator.exportSVG();
        showToast('动画已下载', 'success');
    } catch (error) {
        console.error('Download error:', error);
        showToast('下载失败', 'error');
    }
}

// Event Listeners
generateBtn.addEventListener('click', generateAnimation);
clearBtn.addEventListener('click', clearInput);

playBtn.addEventListener('click', () => {
    const state = animator.getState();
    if (state.progress === 1 || state.progress === 0) {
        animator.restart();
    } else {
        animator.resume();
    }
});

pauseBtn.addEventListener('click', () => {
    animator.pause();
});

restartBtn.addEventListener('click', () => {
    animator.restart();
});

downloadBtn.addEventListener('click', downloadAnimation);

// Example chips
document.querySelectorAll('.chip').forEach(chip => {
    chip.addEventListener('click', (e) => {
        const example = e.target.dataset.example;
        loadExample(example);
    });
});

// Enter to submit (Ctrl/Cmd + Enter)
storyInput.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        generateAnimation();
    }
});

// Initialize
updateUIState('empty');

console.log('🎬 AI Stick Figure Story Animator initialized');
