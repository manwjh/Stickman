/**
 * App.js - Modern Mobile-First Application
 * Enhanced for Gen Z users with fun interactions
 */

// ================================
// DOM Elements
// ================================

const storyInput = document.getElementById('storyInput');
const generateBtn = document.getElementById('generateBtn');
const clearBtn = document.getElementById('clearBtn');
const playPauseBtn = document.getElementById('playPauseBtn');
const playPauseIcon = document.getElementById('playPauseIcon');
const restartBtn = document.getElementById('restartBtn');
const downloadBtn = document.getElementById('downloadBtn');
const exportGIFBtn = document.getElementById('exportGIFBtn');
const exportVideoBtn = document.getElementById('exportVideoBtn');
const shareBtn = document.getElementById('shareBtn');
const langToggle = document.getElementById('langToggle');
const charCount = document.getElementById('charCount');

const loadingState = document.getElementById('loadingState');
const emptyState = document.getElementById('emptyState');
const animationCanvas = document.getElementById('animationCanvas');
const animationControls = document.getElementById('animationControls');
const animationInfo = document.getElementById('animationInfo');

const svgCanvas = document.getElementById('svgCanvas');
const animationContent = document.getElementById('animationContent');
const animationText = document.getElementById('animationText');

const keyframeThumbnails = document.getElementById('keyframeThumbnails');
const thumbnailsContainer = document.getElementById('thumbnailsContainer');
const thumbnailsScroll = document.getElementById('thumbnailsScroll');
const toggleThumbnails = document.getElementById('toggleThumbnails');

const toast = document.getElementById('toast');
const shareModal = document.getElementById('shareModal');
const confettiCanvas = document.getElementById('confetti');

// ================================
// Initialize
// ================================

const animator = new StickFigureAnimator(svgCanvas, animationContent, animationText);
const API_BASE = window.location.origin;
let isPlaying = false;
let currentAnimationData = null;

// ================================
// Confetti Animation
// ================================

class ConfettiEffect {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.particles = [];
        this.animationId = null;
        
        this.resize();
        window.addEventListener('resize', () => this.resize());
    }
    
    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }
    
    createParticle() {
        return {
            x: Math.random() * this.canvas.width,
            y: -10,
            vx: (Math.random() - 0.5) * 4,
            vy: Math.random() * 3 + 2,
            rotation: Math.random() * 360,
            rotationSpeed: (Math.random() - 0.5) * 10,
            color: ['#6366f1', '#ec4899', '#f59e0b', '#10b981', '#3b82f6'][Math.floor(Math.random() * 5)],
            size: Math.random() * 8 + 4,
            shape: Math.random() > 0.5 ? 'circle' : 'square'
        };
    }
    
    launch() {
        for (let i = 0; i < 50; i++) {
            this.particles.push(this.createParticle());
        }
        
        if (!this.animationId) {
            this.animate();
        }
    }
    
    animate() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        for (let i = this.particles.length - 1; i >= 0; i--) {
            const p = this.particles[i];
            
            this.ctx.save();
            this.ctx.translate(p.x, p.y);
            this.ctx.rotate(p.rotation * Math.PI / 180);
            this.ctx.fillStyle = p.color;
            
            if (p.shape === 'circle') {
                this.ctx.beginPath();
                this.ctx.arc(0, 0, p.size, 0, Math.PI * 2);
                this.ctx.fill();
            } else {
                this.ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size);
            }
            
            this.ctx.restore();
            
            p.x += p.vx;
            p.y += p.vy;
            p.rotation += p.rotationSpeed;
            p.vy += 0.2; // Gravity
            
            if (p.y > this.canvas.height + 10) {
                this.particles.splice(i, 1);
            }
        }
        
        if (this.particles.length > 0) {
            this.animationId = requestAnimationFrame(() => this.animate());
        } else {
            this.animationId = null;
        }
    }
}

const confetti = new ConfettiEffect(confettiCanvas);

// ================================
// Toast Notification
// ================================

function showToast(message, type = 'info', emoji = '') {
    const toastIcon = toast.querySelector('.toast-icon');
    const toastMessage = toast.querySelector('.toast-message');
    
    const emojis = {
        success: '✅',
        error: '❌',
        info: 'ℹ️',
        warning: '⚠️'
    };
    
    toastIcon.textContent = emoji || emojis[type] || emojis.info;
    toastMessage.textContent = message;
    
    toast.className = `toast ${type}`;
    toast.classList.add('show');
    
    // Haptic feedback on mobile
    if (navigator.vibrate) {
        navigator.vibrate(type === 'error' ? [50, 50, 50] : 50);
    }
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// ================================
// UI State Management
// ================================

function updateUIState(state) {
    loadingState.style.display = 'none';
    emptyState.style.display = 'none';
    animationCanvas.style.display = 'none';
    animationControls.style.display = 'none';
    animationInfo.style.display = 'none';
    keyframeThumbnails.style.display = 'none';
    
    switch(state) {
        case 'loading':
            loadingState.style.display = 'flex';
            generateBtn.disabled = true;
            break;
        case 'empty':
            emptyState.style.display = 'flex';
            generateBtn.disabled = false;
            break;
        case 'animation':
            animationCanvas.style.display = 'block';
            animationControls.style.display = 'flex';
            animationInfo.style.display = 'flex';
            keyframeThumbnails.style.display = 'block';
            generateBtn.disabled = false;
            break;
    }
}

// ================================
// Character Counter
// ================================

function updateCharCount() {
    const count = storyInput.value.length;
    const max = storyInput.getAttribute('maxlength') || 500;
    charCount.textContent = `${count}/${max}`;
    
    if (count > max * 0.9) {
        charCount.style.color = '#f59e0b';
    } else {
        charCount.style.color = 'var(--text-secondary)';
    }
}

storyInput.addEventListener('input', updateCharCount);

// ================================
// Generate Animation
// ================================

async function generateAnimation() {
    const story = storyInput.value.trim();
    
    if (!story) {
        showToast(i18n.t('toast.empty_story'), 'error');
        storyInput.focus();
        return;
    }
    
    // Get selected mode
    const modeRadio = document.querySelector('input[name="animation-mode"]:checked');
    const mode = modeRadio ? modeRadio.value : 'professional';
    
    updateUIState('loading');
    
    try {
        const response = await fetch(`${API_BASE}/api/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                story: story,
                mode: mode
            })
        });
        
        const result = await response.json();
        
        if (!result.success) {
            throw new Error(result.message || i18n.t('toast.generate_failed'));
        }
        
        currentAnimationData = result.data;
        
        // 调试：打印接收到的数据结构
        console.log('Animation data received:', result.data);
        console.log('Characters:', result.data.characters);
        console.log('Keyframes count:', result.data.keyframes?.length);
        if (result.data.keyframes && result.data.keyframes.length > 0) {
            console.log('First keyframe:', result.data.keyframes[0]);
            console.log('First keyframe characters:', result.data.keyframes[0].characters);
        }
        
        // Load animation
        animator.loadAnimation(result.data);
        
        // Store current animation data
        currentAnimationData = result.data;
        
        // Update info
        updateAnimationInfo(result.data);
        
        // Show animation
        updateUIState('animation');
        
        // Auto-play with celebration
        setTimeout(() => {
            animator.play();
            isPlaying = true;
            updatePlayPauseButton();
            confetti.launch();
        }, 500);
        
        // Show success with mode info
        const modeText = mode === 'simple' ? '简单模式' : '专业模式';
        showToast(`${i18n.t('toast.generate_success')} (${modeText})`, 'success', '🎉');
        
    } catch (error) {
        console.error('Generation error:', error);
        showToast(`${i18n.t('toast.generate_failed')}: ${error.message}`, 'error');
        updateUIState('empty');
    }
}

// ================================
// Update Animation Info
// ================================

function updateAnimationInfo(data) {
    const scenesCount = data.keyframes ? 1 : 0;
    const framesCount = data.keyframes?.length || 0;
    
    document.getElementById('infoScenes').textContent = scenesCount;
    document.getElementById('infoCharacters').textContent = data.characters?.length || 0;
    
    // Generate keyframe thumbnails
    generateKeyframeThumbnails(data);
}

// ================================
// Keyframe Thumbnails
// ================================

function generateKeyframeThumbnails(data) {
    if (!data.keyframes || data.keyframes.length === 0) {
        keyframeThumbnails.style.display = 'none';
        return;
    }
    
    // Clear existing thumbnails
    thumbnailsContainer.innerHTML = '';
    
    // Show thumbnails container first
    keyframeThumbnails.style.display = 'block';
    
    // 如果有 debug_session_id，直接加载后端生成的 SVG
    const debugSessionId = data.debug_session_id;
    
    if (debugSessionId) {
        console.log(`Loading pre-generated SVGs from session: ${debugSessionId}`);
        loadPreGeneratedThumbnails(data, debugSessionId);
    } else {
        console.log('Generating thumbnails from animation data');
        generateThumbnailsFromData(data);
    }
}

/**
 * 加载后端预生成的 SVG 缩略图
 */
function loadPreGeneratedThumbnails(data, sessionId) {
    const totalFrames = data.keyframes.length;
    const maxThumbnails = 15;
    
    // 智能采样
    const samplesToShow = [];
    if (totalFrames > maxThumbnails) {
        const step = Math.floor(totalFrames / maxThumbnails);
        for (let i = 0; i < totalFrames; i += step) {
            samplesToShow.push(i);
        }
        samplesToShow.push(totalFrames - 1);
    } else {
        for (let i = 0; i < totalFrames; i++) {
            samplesToShow.push(i);
        }
    }
    
    console.log(`Showing ${samplesToShow.length} thumbnails out of ${totalFrames} frames`);
    
    // 为每个采样点创建缩略图
    samplesToShow.forEach((frameIndex, displayIndex) => {
        const keyframe = data.keyframes[frameIndex];
        const item = document.createElement('div');
        item.className = 'thumbnail-item';
        item.dataset.frameIndex = frameIndex;
        
        // 加载后端生成的 SVG
        const svgUrl = `/debug_logs/${sessionId}/keyframe_svgs/keyframe_${String(frameIndex).padStart(3, '0')}.svg`;
        const img = document.createElement('img');
        img.src = svgUrl;
        img.className = 'thumbnail-svg';
        img.alt = `Frame ${frameIndex}`;
        
        // 错误处理
        img.onerror = () => {
            console.warn(`Failed to load SVG for frame ${frameIndex}, falling back to generated thumbnail`);
            // 降级到动态生成
            const fallbackItem = createThumbnailItem(keyframe, frameIndex, data);
            item.replaceWith(fallbackItem);
        };
        
        item.appendChild(img);
        
        // 添加信息标签
        const info = document.createElement('div');
        info.className = 'thumbnail-info';
        const timeInSeconds = (keyframe.timestamp_ms / 1000).toFixed(1);
        info.innerHTML = `<div class="thumbnail-label">帧 ${frameIndex}</div>${timeInSeconds}s`;
        item.appendChild(info);
        
        // 点击跳转
        item.addEventListener('click', () => {
            jumpToFrame(frameIndex);
        });
        
        thumbnailsContainer.appendChild(item);
        
        // 第一帧设为激活状态
        if (displayIndex === 0) {
            item.classList.add('active');
        }
    });
}

/**
 * 从动画数据动态生成缩略图（降级方案）
 */
function generateThumbnailsFromData(data) {
    const totalFrames = data.keyframes.length;
    const isInterpolated = !!data.target_fps;
    const maxThumbnails = 15;
    
    let samplesToShow = new Set();
    
    if (isInterpolated && totalFrames > maxThumbnails) {
        const step = Math.floor(totalFrames / maxThumbnails);
        for (let i = 0; i < totalFrames; i += step) {
            samplesToShow.add(i);
        }
        samplesToShow.add(totalFrames - 1);
        console.log(`Interpolated data: showing ${samplesToShow.size} thumbnails out of ${totalFrames} frames`);
    } else {
        for (let i = 0; i < totalFrames; i++) {
            samplesToShow.add(i);
        }
        console.log(`Keyframe data: showing all ${totalFrames} thumbnails`);
    }
    
    // Setup keyframe reached callback
    animator.onKeyframeReached = (frameIndex, keyframe) => {
        if (samplesToShow.has(frameIndex) && !document.querySelector(`[data-frame-index="${frameIndex}"]`)) {
            const thumbnailItem = createThumbnailItem(keyframe, frameIndex, data);
            thumbnailsContainer.appendChild(thumbnailItem);
            thumbnailItem.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
            thumbnailItem.style.animation = 'fadeInUp 0.3s ease';
        }
    };
    
    // Create first thumbnail immediately (frame 0)
    if (data.keyframes.length > 0 && samplesToShow.has(0)) {
        const firstThumbnail = createThumbnailItem(data.keyframes[0], 0, data);
        thumbnailsContainer.appendChild(firstThumbnail);
        firstThumbnail.classList.add('active');
    }
}

function createThumbnailItem(keyframe, index, animationData) {
    const item = document.createElement('div');
    item.className = 'thumbnail-item';
    item.dataset.frameIndex = index;
    
    // Create mini SVG
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('class', 'thumbnail-svg');
    svg.setAttribute('viewBox', '0 0 800 600');
    svg.setAttribute('preserveAspectRatio', 'xMidYMid meet');
    
    // Background
    const bg = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    bg.setAttribute('width', '800');
    bg.setAttribute('height', '600');
    bg.setAttribute('fill', 'white');
    svg.appendChild(bg);
    
    // Ground line
    const ground = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    ground.setAttribute('x1', '0');
    ground.setAttribute('y1', '550');
    ground.setAttribute('x2', '800');
    ground.setAttribute('y2', '550');
    ground.setAttribute('stroke', '#ddd');
    ground.setAttribute('stroke-width', '2');
    svg.appendChild(ground);
    
    // Render characters
    const characters = keyframe.characters || {};
    animationData.characters.forEach(char => {
        const pose = characters[char.id];
        if (pose) {
            renderSkeletonToSVG(svg, pose, char.color);
        }
    });
    
    item.appendChild(svg);
    
    // Info label
    const info = document.createElement('div');
    info.className = 'thumbnail-info';
    const timeInSeconds = (keyframe.timestamp_ms / 1000).toFixed(1);
    info.innerHTML = `<div class="thumbnail-label">帧 ${index}</div>${timeInSeconds}s`;
    item.appendChild(info);
    
    // Click to seek
    item.addEventListener('click', () => {
        seekToFrame(index);
        // Update active state
        document.querySelectorAll('.thumbnail-item').forEach(t => t.classList.remove('active'));
        item.classList.add('active');
    });
    
    return item;
}

function renderSkeletonToSVG(svg, pose, color) {
    /**
     * 统一的骨骼渲染入口
     * 
     * 支持的格式：
     * - 12DOF: pose.joints (原始关节坐标)
     * - 6DOF: pose.pose (角度表示)
     */
    
    if (pose.joints) {
        // 12DOF 原始关节格式
        render12DOFFromJoints(svg, pose.joints, color);
    } else if (pose.pose) {
        // 6DOF 格式
        render6DOFSkeleton(svg, pose.pose, color);
    } else {
        console.error('未知的骨骼数据格式:', pose);
    }
}

function render6DOFSkeleton(svg, pose, color) {
    /**
     * 渲染6DOF骨骼（角度表示）
     * pose 格式: { head_x, head_y, body_angle, left_arm_angle, ... }
     */
    const parts = ['body', 'left_arm', 'right_arm', 'left_leg', 'right_leg'];
    
    parts.forEach(partName => {
        if (pose[partName]) {
            const part = pose[partName];
            const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
            line.setAttribute('x1', part.x1);
            line.setAttribute('y1', part.y1);
            line.setAttribute('x2', part.x2);
            line.setAttribute('y2', part.y2);
            line.setAttribute('stroke', color);
            line.setAttribute('stroke-width', part['stroke-width'] || 3);
            line.setAttribute('stroke-linecap', 'round');
            svg.appendChild(line);
        }
    });
    
    // Head
    if (pose.head) {
        const head = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        head.setAttribute('cx', pose.head.cx);
        head.setAttribute('cy', pose.head.cy);
        head.setAttribute('r', pose.head.r);
        head.setAttribute('stroke', color);
        head.setAttribute('fill', 'none');
        head.setAttribute('stroke-width', '3');
        svg.appendChild(head);
    }
}

function render12DOFFromJoints(svg, joints, color) {
    /**
     * 从原始12DOF关节坐标渲染火柴人
     * joints 格式: { head: {x, y}, neck: {x, y}, waist: {x, y}, ... }
     */
    
    // 绘制顺序：从后到前，避免遮挡
    const connections = [
        // 腿部
        ['left_hip', 'left_foot', 3],
        ['right_hip', 'right_foot', 3],
        // 髋部连接
        ['left_hip', 'waist', 3],
        ['right_hip', 'waist', 3],
        // 躯干
        ['waist', 'neck', 4],
        ['neck', 'head', 3],
        // 肩部连接
        ['neck', 'left_shoulder', 3],
        ['neck', 'right_shoulder', 3],
        // 手臂
        ['left_shoulder', 'left_hand', 3],
        ['right_shoulder', 'right_hand', 3]
    ];
    
    // 绘制连接线
    connections.forEach(([joint1, joint2, width]) => {
        if (joints[joint1] && joints[joint2]) {
            const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
            line.setAttribute('x1', joints[joint1].x);
            line.setAttribute('y1', joints[joint1].y);
            line.setAttribute('x2', joints[joint2].x);
            line.setAttribute('y2', joints[joint2].y);
            line.setAttribute('stroke', color);
            line.setAttribute('stroke-width', width);
            line.setAttribute('stroke-linecap', 'round');
            svg.appendChild(line);
        }
    });
    
    // 头部（圆圈）
    if (joints.head) {
        const head = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        head.setAttribute('cx', joints.head.x);
        head.setAttribute('cy', joints.head.y);
        head.setAttribute('r', '20');
        head.setAttribute('stroke', color);
        head.setAttribute('fill', 'none');
        head.setAttribute('stroke-width', '3');
        svg.appendChild(head);
    }
}

function seekToFrame(frameIndex) {
    if (!currentAnimationData || !currentAnimationData.keyframes) return;
    
    const keyframe = currentAnimationData.keyframes[frameIndex];
    if (!keyframe) return;
    
    // Calculate target time (in seconds for GSAP)
    const targetTime = keyframe.timestamp_ms / 1000;
    
    // Seek to the frame
    if (animator.timeline) {
        animator.timeline.seek(targetTime);
        animator.pause();
        isPlaying = false;
        updatePlayPauseButton();
    }
}

function toggleThumbnailsCollapse() {
    thumbnailsScroll.classList.toggle('collapsed');
    toggleThumbnails.classList.toggle('collapsed');
}

// ================================
// Play/Pause Control
// ================================

function updatePlayPauseButton() {
    if (isPlaying) {
        playPauseIcon.textContent = '⏸️';
        playPauseBtn.setAttribute('title', i18n.t('control.pause'));
    } else {
        playPauseIcon.textContent = '▶️';
        playPauseBtn.setAttribute('title', i18n.t('control.play'));
    }
}

function togglePlayPause() {
    if (isPlaying) {
        animator.pause();
        isPlaying = false;
    } else {
        const state = animator.getState();
        if (state.progress === 1) {
            animator.restart();
        } else {
            animator.resume();
        }
        isPlaying = true;
    }
    updatePlayPauseButton();
}

function restartAnimation() {
    animator.restart();
    isPlaying = true;
    updatePlayPauseButton();
}

// ================================
// Clear Input
// ================================

function clearInput() {
    storyInput.value = '';
    updateCharCount();
    storyInput.focus();
    
    // Haptic feedback
    if (navigator.vibrate) {
        navigator.vibrate(30);
    }
}

// ================================
// Load Example
// ================================

function loadExample(exampleKey) {
    const exampleText = i18n.t(exampleKey);
    storyInput.value = exampleText;
    updateCharCount();
    
    // Auto-scroll to input
    storyInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
    storyInput.focus();
    
    // Haptic feedback
    if (navigator.vibrate) {
        navigator.vibrate(30);
    }
}

// ================================
// Download Animation
// ================================

function downloadAnimation() {
    try {
        animator.exportSVG();
        showToast(i18n.t('toast.download_success'), 'success', '💾');
    } catch (error) {
        console.error('Download error:', error);
        showToast(i18n.t('toast.download_failed'), 'error');
    }
}

// ================================
// Export Video
// ================================

async function exportVideo() {
    try {
        showToast('🎬 正在录制动画...', 'info');
        
        if (!currentAnimationData || !currentAnimationData.keyframes) {
            throw new Error('没有动画数据');
        }
        
        const svg = document.getElementById('svgCanvas');
        if (!svg) {
            throw new Error('SVG canvas not found');
        }
        
        const canvas = document.createElement('canvas');
        canvas.width = 800;
        canvas.height = 600;
        const ctx = canvas.getContext('2d');
        
        if (!canvas.captureStream) {
            throw new Error('您的浏览器不支持视频录制功能');
        }
        
        const stream = canvas.captureStream(0);
        
        let mimeType = 'video/webm;codecs=vp9';
        if (!MediaRecorder.isTypeSupported(mimeType)) {
            mimeType = 'video/webm;codecs=vp8';
            if (!MediaRecorder.isTypeSupported(mimeType)) {
                mimeType = 'video/webm';
            }
        }
        
        const mediaRecorder = new MediaRecorder(stream, {
            mimeType: mimeType,
            videoBitsPerSecond: 2500000
        });
        
        const chunks = [];
        mediaRecorder.ondataavailable = (e) => {
            if (e.data.size > 0) {
                chunks.push(e.data);
            }
        };
        
        mediaRecorder.onstop = () => {
            if (chunks.length === 0) {
                showToast('视频录制失败：没有数据', 'error');
                return;
            }
            
            const blob = new Blob(chunks, { type: mimeType });
            if (blob.size === 0) {
                showToast('视频录制失败：文件为空', 'error');
                return;
            }
            
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `animation_${Date.now()}.webm`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            
            setTimeout(() => URL.revokeObjectURL(url), 100);
            
            showToast('视频导出成功！', 'success', '🎬');
            confetti.launch();
            
            animator.restart();
            isPlaying = true;
            updatePlayPauseButton();
        };
        
        mediaRecorder.onerror = (e) => {
            console.error('MediaRecorder error:', e);
            showToast('视频录制出错', 'error');
        };
        
        mediaRecorder.start();
        console.log('Recording started');
        
        animator.pause();
        isPlaying = false;
        
        const keyframes = currentAnimationData.keyframes;
        const targetFPS = 30;
        const frameInterval = 1000 / targetFPS;
        
        console.log(`Exporting ${keyframes.length} frames at ${targetFPS} FPS`);
        
        async function renderFrameByFrame(frameIndex) {
            if (frameIndex >= keyframes.length) {
                console.log(`Recording complete: ${frameIndex} frames`);
                mediaRecorder.stop();
                return;
            }
            
            const keyframe = keyframes[frameIndex];
            
            if (keyframe.characters) {
                Object.keys(keyframe.characters).forEach(charId => {
                    const charData = keyframe.characters[charId];
                    if (charData.joints) {
                        animator.updateSkeletonPose(charId, charData.joints);
                    }
                });
            }
            
            if (keyframe.text) {
                animationText.textContent = keyframe.text;
            }
            
            await new Promise(resolve => requestAnimationFrame(resolve));
            
            ctx.fillStyle = 'white';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            try {
                const svgData = new XMLSerializer().serializeToString(svg);
                const svgBlob = new Blob([svgData], { type: 'image/svg+xml;charset=utf-8' });
                const url = URL.createObjectURL(svgBlob);
                
                await new Promise((resolve, reject) => {
                    const img = new Image();
                    img.onload = () => {
                        ctx.drawImage(img, 0, 0);
                        URL.revokeObjectURL(url);
                        
                        const track = stream.getVideoTracks()[0];
                        if (track.requestFrame) {
                            track.requestFrame();
                        }
                        
                        resolve();
                    };
                    img.onerror = () => {
                        URL.revokeObjectURL(url);
                        reject(new Error('Image load failed'));
                    };
                    img.src = url;
                });
                
                if (frameIndex % 10 === 0) {
                    const progress = Math.round((frameIndex / keyframes.length) * 100);
                    console.log(`Recording: ${progress}% (${frameIndex}/${keyframes.length})`);
                }
                
            } catch (err) {
                console.error('Frame render error:', err);
            }
            
            setTimeout(() => renderFrameByFrame(frameIndex + 1), frameInterval);
        }
        
        await renderFrameByFrame(0);
        
    } catch (error) {
        console.error('Export video error:', error);
        showToast('视频导出失败: ' + error.message, 'error');
    }
}

// ================================
// Export GIF
// ================================

async function exportGIF() {
    try {
        if (!currentAnimationData || !currentAnimationData.debug_session_id) {
            showToast('无法导出GIF：缺少session信息', 'error');
            return;
        }
        
        showToast('🎨 正在生成GIF...', 'info');
        
        const sessionId = currentAnimationData.debug_session_id;
        
        const response = await fetch('/api/export/gif', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                session_id: sessionId,
                fps: 30,
                quality: 80,
                optimize: true
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'GIF导出失败');
        }
        
        // 下载GIF
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `animation_${sessionId}.gif`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        
        setTimeout(() => URL.revokeObjectURL(url), 100);
        
        showToast('GIF导出成功！', 'success', '🎨');
        confetti.launch();
        
    } catch (error) {
        console.error('Export GIF error:', error);
        showToast('GIF导出失败: ' + error.message, 'error');
    }
}

// ================================
// Share Modal
// ================================

function openShareModal() {
    shareModal.classList.add('show');
    document.body.classList.add('no-scroll');
}

function closeShareModal() {
    shareModal.classList.remove('show');
    document.body.classList.remove('no-scroll');
}

// Share actions
function handleShare(action) {
    switch(action) {
        case 'copy':
            navigator.clipboard.writeText(window.location.href)
                .then(() => {
                    showToast('链接已复制到剪贴板', 'success', '🔗');
                    closeShareModal();
                })
                .catch(() => {
                    showToast('复制失败', 'error');
                });
            break;
        case 'download':
            downloadAnimation();
            closeShareModal();
            break;
        case 'video':
            exportVideo();
            closeShareModal();
            break;
    }
}

// ================================
// Language Toggle
// ================================

function updateLanguageButton() {
    const currentLang = i18n.getCurrentLanguage();
    langToggle.setAttribute('title', currentLang === 'en' ? '切换到中文' : 'Switch to English');
}

// ================================
// Event Listeners
// ================================

// Generate button
generateBtn.addEventListener('click', generateAnimation);

// Clear button
clearBtn.addEventListener('click', clearInput);

// Play/Pause
playPauseBtn.addEventListener('click', togglePlayPause);

// Restart
restartBtn.addEventListener('click', restartAnimation);

// Download
downloadBtn.addEventListener('click', downloadAnimation);

// Export GIF
exportGIFBtn.addEventListener('click', exportGIF);

// Export video
exportVideoBtn.addEventListener('click', exportVideo);

// Share
shareBtn.addEventListener('click', openShareModal);

// Thumbnails toggle
toggleThumbnails.addEventListener('click', toggleThumbnailsCollapse);

// Language toggle
langToggle.addEventListener('click', () => {
    i18n.toggleLanguage();
    updateLanguageButton();
    
    // Haptic feedback
    if (navigator.vibrate) {
        navigator.vibrate(30);
    }
});

// Example pills
document.querySelectorAll('.pill').forEach(pill => {
    pill.addEventListener('click', (e) => {
        const exampleKey = e.currentTarget.getAttribute('data-example-key');
        if (exampleKey) {
            loadExample(exampleKey);
        }
    });
});

// Share modal events
shareModal.addEventListener('click', (e) => {
    if (e.target === shareModal) {
        closeShareModal();
    }
});

document.querySelector('.modal-close')?.addEventListener('click', closeShareModal);

document.querySelectorAll('.share-option').forEach(option => {
    option.addEventListener('click', (e) => {
        const action = e.currentTarget.getAttribute('data-share');
        if (action) {
            handleShare(action);
        }
    });
});

// Keyboard shortcuts
storyInput.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + Enter to generate
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        generateAnimation();
    }
});

document.addEventListener('keydown', (e) => {
    // Space to play/pause (when not typing)
    if (e.code === 'Space' && e.target !== storyInput && animationControls.style.display !== 'none') {
        e.preventDefault();
        togglePlayPause();
    }
    
    // R to restart
    if (e.key === 'r' && e.target !== storyInput && animationControls.style.display !== 'none') {
        e.preventDefault();
        restartAnimation();
    }
    
    // ESC to close modal
    if (e.key === 'Escape' && shareModal.classList.contains('show')) {
        closeShareModal();
    }
});

// ================================
// Touch Gestures
// ================================

let touchStartX = 0;
let touchStartY = 0;

animationCanvas.addEventListener('touchstart', (e) => {
    touchStartX = e.touches[0].clientX;
    touchStartY = e.touches[0].clientY;
}, { passive: true });

animationCanvas.addEventListener('touchend', (e) => {
    const touchEndX = e.changedTouches[0].clientX;
    const touchEndY = e.changedTouches[0].clientY;
    
    const deltaX = touchEndX - touchStartX;
    const deltaY = touchEndY - touchStartY;
    
    // Swipe left to restart
    if (Math.abs(deltaX) > Math.abs(deltaY) && Math.abs(deltaX) > 50) {
        if (deltaX < 0) {
            restartAnimation();
            showToast('重新播放', 'info', '🔄');
        }
    }
    
    // Tap to play/pause
    if (Math.abs(deltaX) < 10 && Math.abs(deltaY) < 10) {
        togglePlayPause();
    }
}, { passive: true });

// ================================
// PWA Install Prompt
// ================================

let deferredPrompt;

window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    
    // Show install hint
    setTimeout(() => {
        showToast('💡 可以将应用添加到主屏幕', 'info');
    }, 5000);
});

window.addEventListener('appinstalled', () => {
    showToast('应用已安装！', 'success', '🎉');
    confetti.launch();
    deferredPrompt = null;
});

// ================================
// Initialize App
// ================================

function initApp() {
    updateUIState('empty');
    updateCharCount();
    updateLanguageButton();
    
    // Fetch version
    fetch(`${API_BASE}/api/version`)
        .then(response => response.json())
        .then(data => {
            const versionEl = document.getElementById('appVersion');
            if (versionEl && data.version) {
                versionEl.textContent = data.version;
            }
        })
        .catch(err => console.log('Could not fetch version'));
    
    console.log('🎬', i18n.t('console.initialized'));
    
    // Welcome animation
    setTimeout(() => {
        if (storyInput.value === '') {
            storyInput.placeholder = i18n.t('input.placeholder');
        }
    }, 500);
}

// Start the app
initApp();

// ================================
// Service Worker Registration (PWA)
// ================================

if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(() => console.log('✅ Service Worker registered'))
            .catch(err => console.log('❌ Service Worker registration failed:', err));
    });
}
