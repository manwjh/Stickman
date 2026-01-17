/**
 * Animator.js - SVG Animation Engine
 * Handles rendering and animating stick figures
 */

class StickFigureAnimator {
    constructor(svgElement, contentGroup, textElement) {
        this.svg = svgElement;
        this.contentGroup = contentGroup;
        this.textElement = textElement;
        this.animationData = null;
        this.timeline = null;
        this.isPlaying = false;
        this.characterElements = {};
    }

    /**
     * Load animation data
     */
    loadAnimation(data) {
        this.animationData = data;
        this.clear();
        this.createCharacterElements();
    }

    /**
     * Clear all animations and content
     */
    clear() {
        if (this.timeline) {
            this.timeline.kill();
            this.timeline = null;
        }
        this.contentGroup.innerHTML = '';
        this.textElement.textContent = '';
        this.characterElements = {};
        this.isPlaying = false;
    }

    /**
     * Create SVG elements for each character
     */
    createCharacterElements() {
        const characters = this.animationData.characters;
        
        characters.forEach(char => {
            const group = document.createElementNS('http://www.w3.org/2000/svg', 'g');
            group.id = `char_${char.id}`;
            group.classList.add('stick-figure');
            
            // Create body parts
            const head = this.createCircle(char.color);
            const body = this.createLine(char.color);
            const leftArm = this.createLine(char.color);
            const rightArm = this.createLine(char.color);
            const leftLeg = this.createLine(char.color);
            const rightLeg = this.createLine(char.color);
            
            // Append in order (legs first, then body, then arms, then head for proper layering)
            group.appendChild(leftLeg);
            group.appendChild(rightLeg);
            group.appendChild(body);
            group.appendChild(leftArm);
            group.appendChild(rightArm);
            group.appendChild(head);
            
            this.contentGroup.appendChild(group);
            
            // Store references
            this.characterElements[char.id] = {
                group,
                head,
                body,
                leftArm,
                rightArm,
                leftLeg,
                rightLeg,
                color: char.color
            };
        });
    }

    /**
     * Create SVG circle element
     */
    createCircle(color) {
        const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        circle.classList.add('stick-figure-head');
        circle.setAttribute('stroke', color);
        circle.setAttribute('fill', 'none');
        circle.setAttribute('stroke-width', '3');
        return circle;
    }

    /**
     * Create SVG line element
     */
    createLine(color) {
        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        line.classList.add('stick-figure-part');
        line.setAttribute('stroke', color);
        line.setAttribute('stroke-width', '3');
        line.setAttribute('stroke-linecap', 'round');
        return line;
    }

    /**
     * Update character pose
     */
    updatePose(characterId, pose) {
        const elements = this.characterElements[characterId];
        if (!elements) return;

        // Update head
        elements.head.setAttribute('cx', pose.head.cx);
        elements.head.setAttribute('cy', pose.head.cy);
        elements.head.setAttribute('r', pose.head.r);

        // Update body
        elements.body.setAttribute('x1', pose.body.x1);
        elements.body.setAttribute('y1', pose.body.y1);
        elements.body.setAttribute('x2', pose.body.x2);
        elements.body.setAttribute('y2', pose.body.y2);

        // Update limbs
        this.updateLine(elements.leftArm, pose.left_arm);
        this.updateLine(elements.rightArm, pose.right_arm);
        this.updateLine(elements.leftLeg, pose.left_leg);
        this.updateLine(elements.rightLeg, pose.right_leg);
    }

    /**
     * Update line element attributes
     */
    updateLine(lineElement, lineData) {
        lineElement.setAttribute('x1', lineData.x1);
        lineElement.setAttribute('y1', lineData.y1);
        lineElement.setAttribute('x2', lineData.x2);
        lineElement.setAttribute('y2', lineData.y2);
    }

    /**
     * Play animation
     */
    play() {
        if (!this.animationData) {
            console.error('No animation data loaded');
            return;
        }

        this.isPlaying = true;
        this.timeline = gsap.timeline({
            onComplete: () => {
                this.isPlaying = false;
            }
        });

        let currentTime = 0;

        // Process each scene
        this.animationData.scenes.forEach(scene => {
            this.addSceneToTimeline(scene, currentTime);
            currentTime += scene.duration / 1000; // Convert to seconds
        });

        this.timeline.play();
    }

    /**
     * Add scene to GSAP timeline
     */
    addSceneToTimeline(scene, startTime) {
        const frames = scene.frames;
        if (frames.length === 0) return;

        // Sort frames by timestamp
        frames.sort((a, b) => a.timestamp - b.timestamp);

        // Set initial pose (first frame)
        const firstFrame = frames[0];
        Object.keys(firstFrame.characters).forEach(charId => {
            this.updatePose(charId, firstFrame.characters[charId]);
        });

        // Update text for first frame
        if (firstFrame.text) {
            this.textElement.textContent = firstFrame.text;
        }

        // Animate between frames
        for (let i = 1; i < frames.length; i++) {
            const prevFrame = frames[i - 1];
            const currentFrame = frames[i];
            const frameDuration = (currentFrame.timestamp - prevFrame.timestamp) / 1000;
            const frameStartTime = startTime + prevFrame.timestamp / 1000;

            // Animate each character
            Object.keys(currentFrame.characters).forEach(charId => {
                const pose = currentFrame.characters[charId];
                const elements = this.characterElements[charId];
                
                if (!elements) return;

                // Animate head
                this.timeline.to(elements.head, {
                    attr: {
                        cx: pose.head.cx,
                        cy: pose.head.cy,
                        r: pose.head.r
                    },
                    duration: frameDuration,
                    ease: 'power2.inOut'
                }, frameStartTime);

                // Animate body
                this.timeline.to(elements.body, {
                    attr: {
                        x1: pose.body.x1,
                        y1: pose.body.y1,
                        x2: pose.body.x2,
                        y2: pose.body.y2
                    },
                    duration: frameDuration,
                    ease: 'power2.inOut'
                }, frameStartTime);

                // Animate limbs
                ['leftArm', 'rightArm', 'leftLeg', 'rightLeg'].forEach(part => {
                    const partData = pose[part.replace(/([A-Z])/g, '_$1').toLowerCase()];
                    this.timeline.to(elements[part], {
                        attr: {
                            x1: partData.x1,
                            y1: partData.y1,
                            x2: partData.x2,
                            y2: partData.y2
                        },
                        duration: frameDuration,
                        ease: 'power2.inOut'
                    }, frameStartTime);
                });
            });

            // Update text
            if (currentFrame.text) {
                this.timeline.call(() => {
                    this.textElement.textContent = currentFrame.text;
                }, null, frameStartTime);
            }
        }
    }

    /**
     * Pause animation
     */
    pause() {
        if (this.timeline) {
            this.timeline.pause();
            this.isPlaying = false;
        }
    }

    /**
     * Resume animation
     */
    resume() {
        if (this.timeline) {
            this.timeline.resume();
            this.isPlaying = true;
        }
    }

    /**
     * Restart animation
     */
    restart() {
        if (this.timeline) {
            this.timeline.restart();
            this.isPlaying = true;
        }
    }

    /**
     * Export animation as SVG
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
     * Get animation state
     */
    getState() {
        return {
            isPlaying: this.isPlaying,
            hasData: !!this.animationData,
            progress: this.timeline ? this.timeline.progress() : 0
        };
    }
}

// Export for use in app.js
window.StickFigureAnimator = StickFigureAnimator;
