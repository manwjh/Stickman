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
            // Page title
            'page.title': '🎬 AI Stick Figure Story Animator',
            'page.subtitle': 'Describe your story in natural language, let AI generate smooth stick figure animations',
            
            // Input section
            'input.title': '📝 Story Input',
            'input.placeholder': 'Enter your story here...\n\nExample:\nA person walks in from the left, sees a ball, jumps excitedly, then bends down to pick up the ball and celebrates by raising it high.',
            'input.generate': 'Generate Animation',
            'input.clear': 'Clear',
            
            // Examples
            'examples.title': '💡 Example Stories',
            'examples.simple': 'A person stands and waves hello',
            'examples.run': 'Someone runs from left to right, then jumps to celebrate',
            'examples.pickup': 'A person walks in, bends down to pick something up, then raises it happily',
            'examples.duo': 'Two people stand on opposite sides, walk towards each other, and high-five to celebrate',
            
            // Preview section
            'preview.title': '🎥 Animation Preview',
            'preview.play': 'Play',
            'preview.pause': 'Pause',
            'preview.restart': 'Restart',
            'preview.download': 'Download',
            'preview.loading': 'AI is generating animation...',
            'preview.empty': 'Enter a story and click "Generate Animation" to start creating',
            
            // Animation info
            'info.title': 'Title:',
            'info.description': 'Description:',
            'info.scenes': 'Scenes:',
            'info.characters': 'Characters:',
            'info.untitled': 'Untitled',
            'info.no_description': 'No description',
            
            // Toast messages
            'toast.empty_story': 'Please enter story content',
            'toast.generate_failed': 'Generation failed',
            'toast.generate_success': 'Animation generated successfully!',
            'toast.download_success': 'Animation downloaded',
            'toast.download_failed': 'Download failed',
            
            // Footer
            'footer.text': 'Powered by AI | Made with ❤️',
            
            // Console
            'console.initialized': '🎬 AI Stick Figure Story Animator initialized'
        },
        
        'zh-CN': {
            // Page title
            'page.title': '🎬 AI火柴人故事动画生成器',
            'page.subtitle': '用自然语言描述故事，让AI自动生成流畅的火柴人动画',
            
            // Input section
            'input.title': '📝 故事输入',
            'input.placeholder': '在这里输入你的故事...\n\n示例：\n小明从左边走进来，看到一个球，兴奋地跳起来，然后弯腰捡起球，高兴地举起球庆祝。',
            'input.generate': '生成动画',
            'input.clear': '清空',
            
            // Examples
            'examples.title': '💡 示例故事',
            'examples.simple': '一个人站着，然后挥手打招呼',
            'examples.run': '小明从左边跑到右边，然后跳起来庆祝',
            'examples.pickup': '一个人走进来，弯腰捡起东西，然后高兴地举起来',
            'examples.duo': '小明站在左边，小红站在右边，他们走向对方，最后击掌庆祝',
            
            // Preview section
            'preview.title': '🎥 动画预览',
            'preview.play': '播放',
            'preview.pause': '暂停',
            'preview.restart': '重新开始',
            'preview.download': '下载',
            'preview.loading': 'AI正在生成动画...',
            'preview.empty': '输入故事并点击"生成动画"开始创作',
            
            // Animation info
            'info.title': '标题：',
            'info.description': '描述：',
            'info.scenes': '场景数：',
            'info.characters': '角色数：',
            'info.untitled': '未命名',
            'info.no_description': '无描述',
            
            // Toast messages
            'toast.empty_story': '请输入故事内容',
            'toast.generate_failed': '生成失败',
            'toast.generate_success': '动画生成成功！',
            'toast.download_success': '动画已下载',
            'toast.download_failed': '下载失败',
            
            // Footer
            'footer.text': 'Powered by AI | Made with ❤️',
            
            // Console
            'console.initialized': '🎬 AI火柴人故事动画生成器已初始化'
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
