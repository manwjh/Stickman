/**
 * Animator.js - Skeleton-Based SVG Animation Engine
 * 
 * Features:
 * - 16-joint hierarchical skeleton rendering
 * - Keyframe-based animation with GSAP
 * - Smooth interpolation between poses
 * - Multi-character support
 */

class StickFigureAnimator {
    constructor(svgElement, contentGroup, textElement) {
        this.svg = svgElement;
        this.contentGroup = contentGroup;
        this.textElement = textElement;
        this.animationData = null;
        this.timeline = null;
        this.isPlaying = false;
        
        // Character elements (skeleton parts)
        this.characterElements = {};
        
        // Props elements
        this.propElements = {};
        
        // Layers for proper z-ordering
        this.propsLayer = null;
        this.charactersLayer = null;
        this.effectsLayer = null;
        
        // Callbacks for keyframe events
        this.onKeyframeReached = null;
    }

    /**
     * Load animation data
     */
    loadAnimation(data) {
        this.animationData = data;
        this.clear();
        this.createLayers();
        this.createSkeletonElements();
        
        // Create props if present
        if (data.props && data.props.length > 0) {
            this.createPropElements(data.props);
        }
    }

    /**
     * Create rendering layers
     */
    createLayers() {
        // Props layer (behind characters)
        this.propsLayer = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        this.propsLayer.id = 'propsLayer';
        this.contentGroup.appendChild(this.propsLayer);
        
        // Characters layer
        this.charactersLayer = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        this.charactersLayer.id = 'charactersLayer';
        this.contentGroup.appendChild(this.charactersLayer);
        
        // Effects layer (front)
        this.effectsLayer = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        this.effectsLayer.id = 'effectsLayer';
        this.contentGroup.appendChild(this.effectsLayer);
    }

    /**
     * Create skeleton elements
     */
    createSkeletonElements() {
        const characters = this.animationData.characters;
        
        characters.forEach(char => {
            const group = document.createElementNS('http://www.w3.org/2000/svg', 'g');
            group.id = `char_${char.id}`;
            group.classList.add('stick-figure');
            
            // Create skeleton parts (lines for bones, circle for head)
            const head = this.createCircle(char.color, 20);
            
            const neck = this.createLine(char.color, 2);
            const upperTorso = this.createLine(char.color, 3);
            const lowerTorso = this.createLine(char.color, 3);
            
            const leftShoulderConnector = this.createLine(char.color, 2);
            const rightShoulderConnector = this.createLine(char.color, 2);
            
            const leftUpperArm = this.createLine(char.color, 3);
            const leftForearm = this.createLine(char.color, 3);
            const rightUpperArm = this.createLine(char.color, 3);
            const rightForearm = this.createLine(char.color, 3);
            
            const leftHipConnector = this.createLine(char.color, 2);
            const rightHipConnector = this.createLine(char.color, 2);
            
            const leftThigh = this.createLine(char.color, 3);
            const leftCalf = this.createLine(char.color, 3);
            const rightThigh = this.createLine(char.color, 3);
            const rightCalf = this.createLine(char.color, 3);
            
            const joints = this.createJointMarkers(char.color);
            
            group.appendChild(leftThigh);
            group.appendChild(leftCalf);
            group.appendChild(rightThigh);
            group.appendChild(rightCalf);
            group.appendChild(leftHipConnector);
            group.appendChild(rightHipConnector);
            group.appendChild(lowerTorso);
            group.appendChild(upperTorso);
            group.appendChild(leftShoulderConnector);
            group.appendChild(rightShoulderConnector);
            group.appendChild(leftUpperArm);
            group.appendChild(leftForearm);
            group.appendChild(rightUpperArm);
            group.appendChild(rightForearm);
            group.appendChild(neck);
            group.appendChild(head);
            
            joints.forEach(j => group.appendChild(j));
            
            this.charactersLayer.appendChild(group);
            
            this.characterElements[char.id] = {
                group,
                head,
                neck,
                upperTorso,
                lowerTorso,
                leftShoulderConnector,
                rightShoulderConnector,
                leftUpperArm,
                leftForearm,
                rightUpperArm,
                rightForearm,
                leftHipConnector,
                rightHipConnector,
                leftThigh,
                leftCalf,
                rightThigh,
                rightCalf,
                joints,
                color: char.color
            };
        });
    }

    /**
     * Create prop elements
     */
    createPropElements(props) {
        props.forEach(prop => {
            const group = document.createElementNS('http://www.w3.org/2000/svg', 'g');
            group.id = `prop_${prop.id}`;
            group.classList.add('prop');
            
            // Parse SVG data and create shape
            const shape = this.createPropShape(prop);
            group.appendChild(shape);
            
            this.propsLayer.appendChild(group);
            
            this.propElements[prop.id] = {
                group,
                shape,
                data: prop
            };
        });
    }

    /**
     * Create prop shape from SVG data
     */
    createPropShape(prop) {
        const svgData = prop.svg_data || prop.type;
        const color = prop.color || '#666';
        
        if (svgData.startsWith('circle:')) {
            const radius = parseFloat(svgData.split(':')[1]) || 15;
            const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
            circle.setAttribute('r', radius);
            circle.setAttribute('fill', color);
            circle.setAttribute('stroke', '#000');
            circle.setAttribute('stroke-width', '2');
            return circle;
        }
        
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        path.setAttribute('d', svgData);
        path.setAttribute('fill', color);
        path.setAttribute('stroke', '#000');
        path.setAttribute('stroke-width', '2');
        path.setAttribute('stroke-linejoin', 'round');
        return path;
    }

    /**
     * Create joint markers
     */
    createJointMarkers(color) {
        const joints = [];
        const jointNames = [
            'neck', 'chest', 'waist',
            'left_shoulder', 'left_elbow', 'left_hand',
            'right_shoulder', 'right_elbow', 'right_hand',
            'left_hip', 'left_knee', 'left_foot',
            'right_hip', 'right_knee', 'right_foot'
        ];
        
        jointNames.forEach(name => {
            const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
            circle.setAttribute('r', '3');
            circle.setAttribute('fill', color);
            circle.setAttribute('opacity', '0.6');
            circle.setAttribute('data-joint', name);
            joints.push(circle);
        });
        
        return joints;
    }

    /**
     * Create SVG circle
     */
    createCircle(color, radius = 20) {
        const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        circle.classList.add('stick-figure-head');
        circle.setAttribute('stroke', color);
        circle.setAttribute('fill', 'none');
        circle.setAttribute('stroke-width', '3');
        circle.setAttribute('r', radius);
        return circle;
    }

    /**
     * Create SVG line
     */
    createLine(color, width = 3) {
        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        line.classList.add('stick-figure-part');
        line.setAttribute('stroke', color);
        line.setAttribute('stroke-width', width);
        line.setAttribute('stroke-linecap', 'round');
        return line;
    }

    /**
     * Update skeleton pose from joint positions
     */
    updateSkeletonPose(characterId, joints) {
        const elements = this.characterElements[characterId];
        if (!elements) return;

        const j = joints;

        // 头部
        elements.head.setAttribute('cx', j.head.x);
        elements.head.setAttribute('cy', j.head.y);

        // 12DOF: 简化的骨骼结构
        // 躯干: neck -> waist
        this.updateLine(elements.neck, j.head.x, j.head.y, j.neck.x, j.neck.y);
        this.updateLine(elements.upperTorso, j.neck.x, j.neck.y, j.waist.x, j.waist.y);
        // lowerTorso 不需要（12DOF没有chest）
        this.updateLine(elements.lowerTorso, j.waist.x, j.waist.y, j.waist.x, j.waist.y);

        // 肩部连接: neck -> shoulders
        this.updateLine(elements.leftShoulderConnector, j.neck.x, j.neck.y, j.left_shoulder.x, j.left_shoulder.y);
        this.updateLine(elements.rightShoulderConnector, j.neck.x, j.neck.y, j.right_shoulder.x, j.right_shoulder.y);

        // 手臂: shoulder -> hand (直线，12DOF没有elbow)
        this.updateLine(elements.leftUpperArm, j.left_shoulder.x, j.left_shoulder.y, j.left_hand.x, j.left_hand.y);
        this.updateLine(elements.rightUpperArm, j.right_shoulder.x, j.right_shoulder.y, j.right_hand.x, j.right_hand.y);
        // forearm 不需要
        this.updateLine(elements.leftForearm, j.left_hand.x, j.left_hand.y, j.left_hand.x, j.left_hand.y);
        this.updateLine(elements.rightForearm, j.right_hand.x, j.right_hand.y, j.right_hand.x, j.right_hand.y);

        // 髋部连接: waist -> hips
        this.updateLine(elements.leftHipConnector, j.waist.x, j.waist.y, j.left_hip.x, j.left_hip.y);
        this.updateLine(elements.rightHipConnector, j.waist.x, j.waist.y, j.right_hip.x, j.right_hip.y);

        // 腿部: hip -> foot (直线，12DOF没有knee)
        this.updateLine(elements.leftThigh, j.left_hip.x, j.left_hip.y, j.left_foot.x, j.left_foot.y);
        this.updateLine(elements.rightThigh, j.right_hip.x, j.right_hip.y, j.right_foot.x, j.right_foot.y);
        // calf 不需要
        this.updateLine(elements.leftCalf, j.left_foot.x, j.left_foot.y, j.left_foot.x, j.left_foot.y);
        this.updateLine(elements.rightCalf, j.right_foot.x, j.right_foot.y, j.right_foot.x, j.right_foot.y);

        // 更新关节标记
        elements.joints.forEach(jointMarker => {
            const jointName = jointMarker.getAttribute('data-joint');
            if (j[jointName]) {
                jointMarker.setAttribute('cx', j[jointName].x);
                jointMarker.setAttribute('cy', j[jointName].y);
            }
        });
    }

    /**
     * Update line element
     */
    updateLine(lineElement, x1, y1, x2, y2) {
        lineElement.setAttribute('x1', x1);
        lineElement.setAttribute('y1', y1);
        lineElement.setAttribute('x2', x2);
        lineElement.setAttribute('y2', y2);
    }

    /**
     * Update prop transform
     */
    updateProp(propId, x, y, rotation, scale = 1, visible = true) {
        const propEl = this.propElements[propId];
        if (!propEl) return;

        propEl.group.setAttribute('transform', 
            `translate(${x}, ${y}) rotate(${rotation}) scale(${scale})`);
        propEl.group.style.display = visible ? 'block' : 'none';
    }

    /**
     * Play animation
     */
    play() {
        if (!this.animationData) {
            console.error('No animation data loaded');
            return;
        }

        if (!this.animationData.keyframes) {
            console.error('Invalid animation data: keyframes not found');
            return;
        }

        const keyframes = this.animationData.keyframes;
        
        // 检查是否是后端插值后的数据（有target_fps标记）
        const isPreInterpolated = this.animationData.target_fps !== null && 
                                  this.animationData.target_fps !== undefined;
        
        if (isPreInterpolated) {
            console.log(`Playing pre-interpolated animation: ${keyframes.length} frames at ${this.animationData.target_fps}fps`);
            this.playFrameByFrame(keyframes);
        } else {
            console.log(`Playing with GSAP interpolation: ${keyframes.length} keyframes`);
            this.playWithGSAP(keyframes);
        }
    }
    
    /**
     * Play frame-by-frame (for pre-interpolated data)
     */
    playFrameByFrame(frames) {
        if (!frames || frames.length === 0) return;
        
        this.isPlaying = true;
        
        // Initialize state
        this.frameByFrameState = {
            frames: frames,
            currentFrameIndex: 0,
            startTime: performance.now(),
            pauseTime: null
        };
        
        // 设置初始姿态
        const firstFrame = frames[0];
        if (firstFrame.characters) {
            Object.keys(firstFrame.characters).forEach(charId => {
                const charData = firstFrame.characters[charId];
                if (charData.joints) {
                    this.updateSkeletonPose(charId, charData.joints);
                }
            });
        }
        
        // 开始播放
        this.playNextFrame();
    }
    
    /**
     * Play next frame (frame-by-frame internal)
     */
    playNextFrame() {
        if (!this.isPlaying || !this.frameByFrameState) {
            return;
        }
        
        const state = this.frameByFrameState;
        const frames = state.frames;
        const i = state.currentFrameIndex;
        
        if (i >= frames.length) {
            this.isPlaying = false;
            return;
        }
        
        const frame = frames[i];
        const currentTime = performance.now() - state.startTime;
        
        // 更新角色姿态
        if (frame.characters) {
            Object.keys(frame.characters).forEach(charId => {
                const charData = frame.characters[charId];
                if (charData.joints) {
                    this.updateSkeletonPose(charId, charData.joints);
                }
            });
        }
        
        // 更新文本
        if (frame.text) {
            this.textElement.textContent = frame.text;
        }
        
        // Callback for keyframe reached (每10帧触发一次)
        if (this.onKeyframeReached && i % 10 === 0) {
            this.onKeyframeReached(i, frame);
        }
        
        state.currentFrameIndex++;
        
        // 计算下一帧的等待时间
        if (state.currentFrameIndex < frames.length) {
            const nextFrame = frames[state.currentFrameIndex];
            const waitTime = Math.max(0, nextFrame.timestamp_ms - currentTime);
            this.frameTimer = setTimeout(() => this.playNextFrame(), waitTime);
        } else {
            this.isPlaying = false;
        }
    }
    
    /**
     * Resume frame-by-frame playback
     */
    resumeFrameByFrame() {
        if (!this.frameByFrameState) return;
        
        const state = this.frameByFrameState;
        const frames = state.frames;
        const currentFrame = frames[state.currentFrameIndex];
        
        if (!currentFrame) {
            // Already finished, restart from beginning
            this.frameByFrameState.currentFrameIndex = 0;
            this.frameByFrameState.startTime = performance.now();
        } else {
            // Adjust start time for pause duration
            const pauseDuration = performance.now() - (state.pauseTime || performance.now());
            state.startTime += pauseDuration;
        }
        
        this.playNextFrame();
    }
    
    /**
     * Play with GSAP interpolation (for keyframes only)
     */
    playWithGSAP(keyframes) {
        this.isPlaying = true;
        this.timeline = gsap.timeline({
            onComplete: () => {
                this.isPlaying = false;
            }
        });

        this.addKeyframesToTimeline(keyframes);
        this.timeline.play();
    }
    
    /**
     * Add keyframes to timeline
     */
    addKeyframesToTimeline(keyframes) {
        if (!keyframes || keyframes.length === 0) return;
        
        keyframes.sort((a, b) => a.timestamp_ms - b.timestamp_ms);
        
        console.log(`Adding ${keyframes.length} keyframes to timeline`);
        
        const firstFrame = keyframes[0];
        console.log('First frame:', firstFrame);
        
        if (firstFrame.characters) {
            Object.keys(firstFrame.characters).forEach(charId => {
                const charData = firstFrame.characters[charId];
                console.log(`Setting initial pose for ${charId}:`, charData.joints);
                if (charData.joints) {
                    this.updateSkeletonPose(charId, charData.joints);
                }
            });
        }
        
        if (firstFrame.text) {
            this.textElement.textContent = firstFrame.text;
        }
        
        for (let i = 1; i < keyframes.length; i++) {
            const currentFrame = keyframes[i];
            const prevFrame = keyframes[i - 1];
            const frameDuration = (currentFrame.timestamp_ms - prevFrame.timestamp_ms) / 1000;
            const frameStartTime = prevFrame.timestamp_ms / 1000;
            
            console.log(`Frame ${i}: from ${prevFrame.timestamp_ms}ms to ${currentFrame.timestamp_ms}ms (duration: ${frameDuration}s, startTime: ${frameStartTime}s)`);
            
            if (currentFrame.characters) {
                Object.keys(currentFrame.characters).forEach(charId => {
                    const charData = currentFrame.characters[charId];
                    if (charData.joints) {
                        this.animateSkeletonToJoints(charId, charData.joints, frameDuration, frameStartTime);
                    }
                });
            }
            
            if (currentFrame.text) {
                this.timeline.call(() => {
                    this.textElement.textContent = currentFrame.text;
                }, null, frameStartTime);
            }
            
            // Callback for keyframe reached
            this.timeline.call(() => {
                if (this.onKeyframeReached) {
                    this.onKeyframeReached(i, currentFrame);
                }
            }, null, frameStartTime);
        }
        
        console.log('Timeline duration:', this.timeline.duration(), 'seconds');
    }
    
    /**
     * Animate skeleton to target joints
     */
    animateSkeletonToJoints(characterId, targetJoints, duration, startTime) {
        const elements = this.characterElements[characterId];
        if (!elements) return;
        
        const fromJoints = {};
        
        // 获取当前关节位置
        Object.keys(targetJoints).forEach(jointName => {
            if (jointName === 'head') {
                const cx = elements.head.getAttribute('cx');
                const cy = elements.head.getAttribute('cy');
                if (cx !== null && cy !== null) {
                    fromJoints[jointName] = {
                        x: parseFloat(cx),
                        y: parseFloat(cy)
                    };
                } else {
                    // 如果元素还未设置位置，使用目标位置（第一帧的情况）
                    fromJoints[jointName] = {
                        x: targetJoints[jointName].x,
                        y: targetJoints[jointName].y
                    };
                }
            } else {
                const jointMarker = elements.joints?.find(j => j.getAttribute('data-joint') === jointName);
                if (jointMarker) {
                    const cx = jointMarker.getAttribute('cx');
                    const cy = jointMarker.getAttribute('cy');
                    if (cx !== null && cy !== null) {
                        fromJoints[jointName] = {
                            x: parseFloat(cx),
                            y: parseFloat(cy)
                        };
                    } else {
                        fromJoints[jointName] = {
                            x: targetJoints[jointName].x,
                            y: targetJoints[jointName].y
                        };
                    }
                } else {
                    fromJoints[jointName] = {
                        x: targetJoints[jointName].x,
                        y: targetJoints[jointName].y
                    };
                }
            }
        });
        
        const dummy = { progress: 0 };
        
        this.timeline.to(dummy, {
            progress: 1,
            duration: duration,
            ease: 'power2.inOut',
            onUpdate: () => {
                const t = dummy.progress;
                const interpolatedJoints = {};
                
                Object.keys(targetJoints).forEach(jointName => {
                    if (fromJoints[jointName]) {
                        interpolatedJoints[jointName] = {
                            x: fromJoints[jointName].x + (targetJoints[jointName].x - fromJoints[jointName].x) * t,
                            y: fromJoints[jointName].y + (targetJoints[jointName].y - fromJoints[jointName].y) * t
                        };
                    }
                });
                
                // 更新完整的骨骼姿势
                this.updateSkeletonPose(characterId, interpolatedJoints);
            }
        }, startTime);
    }

    /**
     * Animate prop
     */
    animateProp(prop, duration, startTime) {
        const propEl = this.propElements[prop.id];
        if (!propEl) return;

        const transform = `translate(${prop.x}, ${prop.y}) rotate(${prop.rotation}) scale(${prop.scale})`;
        
        this.timeline.to(propEl.group, {
            attr: { transform: transform },
            duration: duration,
            ease: 'power2.inOut'
        }, startTime);

        if (prop.visible !== undefined) {
            this.timeline.call(() => {
                propEl.group.style.display = prop.visible ? 'block' : 'none';
            }, null, startTime);
        }
    }

    /**
     * Clear animation
     */
    clear() {
        if (this.timeline) {
            this.timeline.kill();
            this.timeline = null;
        }
        this.contentGroup.innerHTML = '';
        this.textElement.textContent = '';
        this.characterElements = {};
        this.propElements = {};
        this.isPlaying = false;
    }

    /**
     * Pause animation
     */
    pause() {
        this.isPlaying = false;
        if (this.timeline) {
            this.timeline.pause();
        }
        if (this.frameTimer) {
            clearTimeout(this.frameTimer);
            this.frameTimer = null;
            if (this.frameByFrameState) {
                this.frameByFrameState.pauseTime = performance.now();
            }
        }
        console.log('Animation paused');
    }

    /**
     * Resume animation
     */
    resume() {
        if (!this.isPlaying) {
            this.isPlaying = true;
            if (this.timeline) {
                this.timeline.resume();
            } else if (this.animationData && this.frameByFrameState) {
                // Resume frame-by-frame playback
                this.resumeFrameByFrame();
            }
            console.log('Animation resumed');
        }
    }

    /**
     * Restart animation
     */
    restart() {
        this.isPlaying = false;
        if (this.timeline) {
            this.timeline.restart();
            this.timeline.pause();
        }
        
        // Reset frame-by-frame state
        if (this.frameByFrameState) {
            this.frameByFrameState = null;
        }
        if (this.frameTimer) {
            clearTimeout(this.frameTimer);
            this.frameTimer = null;
        }
        
        // Restart playback
        setTimeout(() => {
            this.play();
        }, 10);
        console.log('Animation restarted');
    }

    /**
     * Export SVG
     */
    exportSVG() {
        const svgClone = this.svg.cloneNode(true);
        const serializer = new XMLSerializer();
        const svgString = serializer.serializeToString(svgClone);
        
        const blob = new Blob([svgString], { type: 'image/svg+xml' });
        const url = URL.createObjectURL(blob);
        
        const link = document.createElement('a');
        link.href = url;
        link.download = `${this.animationData.title || 'animation'}.svg`;
        link.click();
        
        URL.revokeObjectURL(url);
    }

    /**
     * Get state
     */
    getState() {
        if (this.timeline) {
            // GSAP mode
            return {
                isPlaying: this.isPlaying,
                hasData: !!this.animationData,
                progress: this.timeline.progress()
            };
        } else if (this.frameByFrameState) {
            // Frame-by-frame mode
            const state = this.frameByFrameState;
            const totalFrames = state.frames.length;
            const currentFrame = state.currentFrameIndex;
            const progress = currentFrame / Math.max(totalFrames - 1, 1);
            
            return {
                isPlaying: this.isPlaying,
                hasData: true,
                progress: progress,
                currentFrame: currentFrame,
                totalFrames: totalFrames
            };
        }
        
        return {
            isPlaying: this.isPlaying,
            hasData: !!this.animationData,
            progress: 0
        };
    }
}

// Export
window.StickFigureAnimator = StickFigureAnimator;
