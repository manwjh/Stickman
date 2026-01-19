/**
 * i18n.js - Internationalization Support
 * Simple i18n implementation for multilingual support
 */

const i18n = {
    // Current language
    currentLang: 'en',
    
    // Translation data
    translations: {
        en: {
            // Hero
            'hero.title': 'Type Your Story\nInstantly Animated',
            'hero.subtitle': 'AI draws stick figures and brings your stories to life ✨',
            
            // Quick examples
            'quick.label': '👇 Try These',
            
            // Input
            'input.label': 'Tell Your Story',
            'input.placeholder': 'Describe your story in detail...\n\nExample:\nA person walks in from the left side of the stage, suddenly spots a colorful ball on the ground. Their eyes light up with excitement! They sprint towards the ball, jump high into the air with joy, then land and carefully pick up the ball with both hands, raising it triumphantly above their head while spinning around in celebration.',
            'input.clear': 'Clear',
            
            // Mode selector
            'mode.professional': 'Professional',
            'mode.professional_desc': '16 joints, precise control',
            'mode.simple': 'Simple',
            'mode.simple_desc': '6 params, fast generation',
            
            // Examples
            'examples.simple': 'A person walks in from the left, waves enthusiastically, then bows politely to greet everyone.',
            'examples.run': 'Someone sprints from left to right with determination, suddenly leaps high into the air, and lands with both arms raised in victory celebration.',
            'examples.pickup': 'A person strolls in casually, spots a mysterious box on the ground, bends down carefully to pick it up, examines it with curiosity, then excitedly raises it high above their head.',
            'examples.duo': 'Two friends stand on opposite sides of the stage. They notice each other, smile broadly, and walk towards each other with open arms. They meet in the middle and enthusiastically high-five, jumping for joy.',
            'examples.dance': 'A person grooves to the music, moving their body rhythmically. They spin around gracefully, wave their arms in flowing motions, and strike a cool final pose with one hand pointing to the sky.',
            'examples.kungfu': 'A martial arts master walks in slowly from the right, assumes a fighting stance. Suddenly performs a spectacular flying kick, spins in mid-air, lands steadily, throws rapid punches, then bows respectfully.',
            'examples.celebrate': 'Someone receives great news, freezes in shock for a moment, then explodes with joy! They jump up and down, pump their fists vigorously, spin around in excitement, and finish with enthusiastic applause.',
            
            // Action
            'action.generate': 'Generate Animation',
            'action.hint': '💡 Ctrl+Enter for quick generation',
            
            // Preview
            'preview.loading': 'AI is creating magic...',
            'preview.empty_title': 'Start Creating!',
            'preview.empty_text': 'Enter your story and let AI animate it',
            
            // Controls
            'control.play': 'Play',
            'control.pause': 'Pause',
            'control.restart': 'Restart',
            'control.share': 'Share',
            'control.download': 'Download',
            'control.video': 'Export Video',
            
            // Share
            'share.title': 'Share Animation',
            'share.copy': 'Copy Link',
            'share.download': 'Download Animation',
            'share.video': 'Export Video',
            
            // Toast
            'toast.empty_story': 'Please enter story content',
            'toast.generate_failed': 'Generation failed',
            'toast.generate_success': 'Animation generated successfully!',
            'toast.download_success': 'Animation downloaded',
            'toast.download_failed': 'Download failed',
            
            // Footer
            'footer.made': 'Made with',
            'footer.powered': 'by AI',
            
            // Console
            'console.initialized': '🎬 AI Stickman Animator initialized'
        },
        
        'zh-CN': {
            // Hero
            'hero.title': '输入文字\n秒变动画',
            'hero.subtitle': 'AI帮你画火柴人，让故事动起来 ✨',
            
            // Quick examples
            'quick.label': '👇 点击试试',
            
            // Input
            'input.label': '说说你的故事',
            'input.placeholder': '请详细描述你的故事...\n\n示例：\n小明从舞台左边慢慢走进来，突然发现地上有一个五彩缤纷的足球。他的眼睛瞬间亮了起来！激动地向球冲过去，兴奋地跳起来欢呼，然后落地弯腰用双手小心翼翼地捡起球，高高举过头顶，开心地转圈庆祝这个意外的发现。',
            'input.clear': '清空',
            
            // Mode selector
            'mode.professional': '专业模式',
            'mode.professional_desc': '16关节精确控制',
            'mode.simple': '简单模式',
            'mode.simple_desc': '6参数快速生成',
            
            // Examples
            'examples.simple': '一个人从左边走进来，热情地挥动双手打招呼，然后礼貌地鞠躬问好。',
            'examples.run': '小明从左边飞快地跑过来，突然用力向上跳跃，在空中做出胜利的姿势，落地后双臂高举庆祝成功。',
            'examples.pickup': '一个人悠闲地走进来，看到地上有个神秘的箱子，好奇地蹲下去仔细查看，然后兴奋地把箱子高高举起展示给大家。',
            'examples.duo': '小明站在左边，小红站在右边。他们互相看到对方后露出笑容，激动地向彼此跑去，在中间相遇后用力击掌，然后一起跳起来庆祝。',
            'examples.dance': '一个人跟随音乐的节奏开始跳舞，身体自然摆动。然后优雅地转圈，双臂像波浪一样流畅挥动，最后摆出酷炫的造型，单手指向天空。',
            'examples.kungfu': '武术大师从右侧缓缓走来，摆出起手式。突然一个凌空飞踢，在空中旋转，稳稳落地后迅速出拳，最后收势抱拳致礼。',
            'examples.celebrate': '一个人收到好消息后，先是愣了一下，然后激动地跳起来，双手握拳用力向下挥动，接着兴奋地转圈，最后开心地拍手庆祝。',
            
            // Action
            'action.generate': '生成动画',
            'action.hint': '💡 Ctrl+Enter 快速生成',
            
            // Preview
            'preview.loading': 'AI正在创作中...',
            'preview.empty_title': '开始创作吧！',
            'preview.empty_text': '输入你的故事，让AI帮你变成动画',
            
            // Controls
            'control.play': '播放',
            'control.pause': '暂停',
            'control.restart': '重新播放',
            'control.share': '分享',
            'control.download': '下载',
            'control.video': '导出视频',
            
            // Share
            'share.title': '分享动画',
            'share.copy': '复制链接',
            'share.download': '下载动画',
            'share.video': '导出视频',
            
            // Toast
            'toast.empty_story': '请输入故事内容',
            'toast.generate_failed': '生成失败',
            'toast.generate_success': '动画生成成功！',
            'toast.download_success': '动画已下载',
            'toast.download_failed': '下载失败',
            
            // Footer
            'footer.made': 'Made with',
            'footer.powered': 'by AI',
            
            // Console
            'console.initialized': '🎬 AI火柴人动画生成器已初始化'
        }
    },
    
    /**
     * Initialize i18n with browser language or specified language
     */
    init(lang = null) {
        // Detect browser language
        if (!lang) {
            const browserLang = navigator.language || navigator.userLanguage;
            lang = browserLang.startsWith('zh') ? 'zh-CN' : 'en';
        }
        
        // Load language from localStorage if available
        const savedLang = localStorage.getItem('language');
        if (savedLang && this.translations[savedLang]) {
            lang = savedLang;
        }
        
        this.setLanguage(lang);
    },
    
    /**
     * Set current language
     */
    setLanguage(lang) {
        if (!this.translations[lang]) {
            console.warn(`Language ${lang} not supported, falling back to English`);
            lang = 'en';
        }
        
        this.currentLang = lang;
        localStorage.setItem('language', lang);
        
        // Update HTML lang attribute
        document.documentElement.lang = lang;
        
        // Update all text on page
        this.updatePageText();
    },
    
    /**
     * Get translation for key
     */
    t(key, defaultValue = '') {
        const translation = this.translations[this.currentLang][key];
        return translation !== undefined ? translation : defaultValue || key;
    },
    
    /**
     * Update all text elements on the page
     */
    updatePageText() {
        // Update elements with data-i18n attribute
        document.querySelectorAll('[data-i18n]').forEach(element => {
            const key = element.getAttribute('data-i18n');
            element.textContent = this.t(key);
        });
        
        // Update elements with data-i18n-placeholder attribute
        document.querySelectorAll('[data-i18n-placeholder]').forEach(element => {
            const key = element.getAttribute('data-i18n-placeholder');
            element.placeholder = this.t(key);
        });
        
        // Update elements with data-i18n-title attribute
        document.querySelectorAll('[data-i18n-title]').forEach(element => {
            const key = element.getAttribute('data-i18n-title');
            element.title = this.t(key);
        });
        
        // Update page title
        document.title = this.t('page.title');
    },
    
    /**
     * Get current language
     */
    getCurrentLanguage() {
        return this.currentLang;
    },
    
    /**
     * Toggle between languages
     */
    toggleLanguage() {
        const newLang = this.currentLang === 'en' ? 'zh-CN' : 'en';
        this.setLanguage(newLang);
    }
};

// Auto-initialize on load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => i18n.init());
} else {
    i18n.init();
}

// Export for global use
window.i18n = i18n;
