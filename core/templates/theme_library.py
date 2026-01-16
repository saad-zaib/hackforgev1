"""
Complete Theme Library with Integration Guide
Save as: core/templates/theme_library.py
"""

import random


class ThemeLibrary:
    """
    Centralized theme library for generating diverse UIs
    Each machine randomly picks a theme for unique appearance
    """
    
    THEMES = {
        'cyberpunk': {
            'name': 'Cyberpunk Neon',
            'description': 'Futuristic neon-lit interface',
            'primary_color': '#ff0080',
            'secondary_color': '#00ff9f',
            'background': 'linear-gradient(135deg, #0a0a0a 0%, #1a0a2e 100%)',
            'font': "'Orbitron', monospace",
            'style': 'neon',
            'fonts_import': '<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap" rel="stylesheet">',
            'css': '''
body {
    font-family: 'Orbitron', monospace;
    background: linear-gradient(135deg, #0a0a0a 0%, #1a0a2e 100%);
    background-attachment: fixed;
    color: #00ff9f;
    margin: 0;
    padding: 0;
    min-height: 100vh;
}

.container {
    max-width: 1200px;
    margin: 50px auto;
    padding: 40px;
    background: rgba(10, 10, 30, 0.9);
    border: 2px solid #ff0080;
    border-radius: 10px;
    box-shadow: 0 0 30px rgba(255, 0, 128, 0.5), inset 0 0 20px rgba(255, 0, 128, 0.1);
}

h1 {
    color: #ff0080;
    text-shadow: 0 0 10px rgba(255, 0, 128, 0.8), 0 0 20px rgba(255, 0, 128, 0.5);
    margin-top: 0;
    font-size: 2.5em;
    text-transform: uppercase;
    letter-spacing: 3px;
}

input {
    background: #000;
    border: 2px solid #00ff9f;
    color: #00ff9f;
    padding: 15px;
    font-family: 'Orbitron', monospace;
    width: 100%;
    box-sizing: border-box;
    border-radius: 5px;
    font-size: 16px;
    box-shadow: 0 0 10px rgba(0, 255, 159, 0.3);
    transition: all 0.3s;
}

input:focus {
    outline: none;
    box-shadow: 0 0 20px rgba(0, 255, 159, 0.6);
    border-color: #ff0080;
}

button {
    background: linear-gradient(45deg, #ff0080, #ff00ff);
    border: none;
    color: #fff;
    padding: 15px 40px;
    font-weight: bold;
    cursor: pointer;
    text-transform: uppercase;
    border-radius: 5px;
    font-family: 'Orbitron', monospace;
    box-shadow: 0 0 20px rgba(255, 0, 128, 0.6);
    transition: all 0.3s;
    margin-top: 15px;
}

button:hover {
    box-shadow: 0 0 30px rgba(255, 0, 255, 0.8);
    transform: translateY(-2px);
}

.result {
    margin-top: 30px;
    padding: 20px;
    background: rgba(0, 255, 159, 0.05);
    border: 1px solid #00ff9f;
    border-radius: 5px;
}

.hint {
    margin-top: 20px;
    padding: 15px;
    background: rgba(255, 0, 128, 0.1);
    border-left: 4px solid #ff0080;
    border-radius: 5px;
}
''',
            'placeholder': 'Enter your query...',
            'button_text': 'Execute'
        },
        
        'retro_terminal': {
            'name': 'Retro Terminal',
            'description': 'Classic green screen terminal',
            'primary_color': '#00ff00',
            'secondary_color': '#33ff33',
            'background': '#000',
            'font': "'Courier New', monospace",
            'style': 'terminal',
            'fonts_import': '',
            'css': '''
body {
    font-family: 'Courier New', monospace;
    background: #000;
    color: #00ff00;
    margin: 0;
    padding: 20px;
    min-height: 100vh;
}

.container {
    max-width: 800px;
    margin: 20px auto;
    padding: 20px;
    background: #001100;
    border: 3px solid #00ff00;
    font-size: 14px;
    box-shadow: inset 0 0 50px rgba(0, 255, 0, 0.1);
}

.terminal-header {
    background: #003300;
    padding: 10px;
    margin: -20px -20px 20px -20px;
    border-bottom: 2px solid #00ff00;
    font-weight: bold;
    text-transform: uppercase;
}

h1 {
    color: #00ff00;
    margin-top: 0;
    font-size: 24px;
    font-weight: normal;
}

.prompt::before {
    content: "root@hackforge:~$ ";
    color: #33ff33;
    font-weight: bold;
}

input {
    background: #000;
    border: 1px solid #00ff00;
    color: #00ff00;
    padding: 10px;
    font-family: 'Courier New', monospace;
    width: 100%;
    box-sizing: border-box;
    font-size: 14px;
}

input:focus {
    outline: none;
    background: #001100;
}

button {
    background: #003300;
    border: 1px solid #00ff00;
    color: #00ff00;
    padding: 10px 30px;
    cursor: pointer;
    font-family: 'Courier New', monospace;
    margin-top: 10px;
    text-transform: uppercase;
}

button:hover {
    background: #00ff00;
    color: #000;
}

.result {
    margin-top: 20px;
    padding: 15px;
    border: 1px solid #00ff00;
    background: rgba(0, 255, 0, 0.05);
}

.hint {
    margin-top: 20px;
    padding: 10px;
    border-left: 3px solid #00ff00;
    background: rgba(0, 255, 0, 0.05);
}
''',
            'placeholder': '_',
            'button_text': '[EXECUTE]'
        },
        
        'modern_glass': {
            'name': 'Modern Glassmorphism',
            'description': 'Sleek glass-effect design',
            'primary_color': '#667eea',
            'secondary_color': '#764ba2',
            'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            'font': "'Inter', sans-serif",
            'style': 'glass',
            'fonts_import': '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">',
            'css': '''
body {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    background-attachment: fixed;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0;
    padding: 20px;
}

.container {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 40px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    max-width: 600px;
    width: 100%;
}

h1 {
    color: #fff;
    margin-top: 0;
    font-weight: 600;
    font-size: 32px;
}

p {
    color: rgba(255, 255, 255, 0.9);
}

input {
    background: rgba(255, 255, 255, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.3);
    color: #fff;
    padding: 15px;
    border-radius: 10px;
    width: 100%;
    box-sizing: border-box;
    font-size: 16px;
    font-family: 'Inter', sans-serif;
}

input::placeholder {
    color: rgba(255, 255, 255, 0.6);
}

input:focus {
    outline: none;
    background: rgba(255, 255, 255, 0.25);
    border-color: rgba(255, 255, 255, 0.5);
}

button {
    background: rgba(255, 255, 255, 0.9);
    color: #667eea;
    border: none;
    padding: 15px 40px;
    border-radius: 10px;
    font-weight: 600;
    cursor: pointer;
    margin-top: 15px;
    font-size: 16px;
    transition: all 0.3s;
}

button:hover {
    background: #fff;
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.result {
    margin-top: 30px;
    padding: 20px;
    background: rgba(255, 255, 255, 0.15);
    border-radius: 10px;
}

.hint {
    margin-top: 20px;
    padding: 15px;
    background: rgba(255, 255, 255, 0.1);
    border-left: 4px solid rgba(255, 255, 255, 0.5);
    border-radius: 5px;
}
''',
            'placeholder': 'What are you looking for?',
            'button_text': 'Search'
        },
        
        'dark_hacker': {
            'name': 'Dark Hacker',
            'description': 'Professional hacker aesthetic',
            'primary_color': '#ff7300',
            'secondary_color': '#ff9500',
            'background': '#0a0a0a',
            'font': "'Fira Code', monospace",
            'style': 'dark',
            'fonts_import': '<link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">',
            'css': '''
body {
    font-family: 'Fira Code', monospace;
    background: #0a0a0a;
    color: #e0e0e0;
    margin: 0;
    padding: 20px;
    min-height: 100vh;
}

.container {
    max-width: 900px;
    margin: 50px auto;
    background: #1a1a1a;
    border-radius: 15px;
    padding: 40px;
    border: 1px solid #333;
    box-shadow: 0 10px 50px rgba(0, 0, 0, 0.5);
}

h1 {
    color: #ff7300;
    border-bottom: 2px solid #ff7300;
    padding-bottom: 10px;
    margin-top: 0;
    font-size: 28px;
}

input {
    background: #0a0a0a;
    border: 2px solid #333;
    color: #e0e0e0;
    padding: 15px;
    border-radius: 5px;
    width: 100%;
    box-sizing: border-box;
    font-family: 'Fira Code', monospace;
    font-size: 14px;
    transition: all 0.3s;
}

input:focus {
    border-color: #ff7300;
    outline: none;
    box-shadow: 0 0 10px rgba(255, 115, 0, 0.3);
}

button {
    background: #ff7300;
    color: #000;
    border: none;
    padding: 15px 40px;
    border-radius: 5px;
    font-weight: bold;
    cursor: pointer;
    text-transform: uppercase;
    font-family: 'Fira Code', monospace;
    margin-top: 15px;
    transition: all 0.3s;
}

button:hover {
    background: #ff9500;
    transform: translateY(-1px);
    box-shadow: 0 5px 15px rgba(255, 115, 0, 0.4);
}

.result {
    margin-top: 30px;
    padding: 20px;
    background: rgba(255, 115, 0, 0.05);
    border-left: 3px solid #ff7300;
    border-radius: 5px;
}

.hint {
    background: rgba(255, 115, 0, 0.1);
    border-left: 4px solid #ff7300;
    padding: 15px;
    margin-top: 20px;
    border-radius: 5px;
}
''',
            'placeholder': 'Enter search query...',
            'button_text': 'Execute'
        },
        
        'minimal_nordic': {
            'name': 'Minimal Nordic',
            'description': 'Clean Scandinavian design',
            'primary_color': '#5e81ac',
            'secondary_color': '#88c0d0',
            'background': '#eceff4',
            'font': "'Source Sans Pro', sans-serif",
            'style': 'minimal',
            'fonts_import': '<link href="https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@400;600&display=swap" rel="stylesheet">',
            'css': '''
body {
    font-family: 'Source Sans Pro', sans-serif;
    background: #eceff4;
    color: #2e3440;
    margin: 0;
    padding: 20px;
    min-height: 100vh;
}

.container {
    max-width: 700px;
    margin: 80px auto;
    background: #fff;
    padding: 50px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
}

h1 {
    color: #2e3440;
    font-weight: 600;
    font-size: 32px;
    margin-top: 0;
    margin-bottom: 30px;
}

p {
    color: #4c566a;
    line-height: 1.6;
}

input {
    background: #f9f9f9;
    border: 2px solid #d8dee9;
    color: #2e3440;
    padding: 15px;
    border-radius: 4px;
    width: 100%;
    box-sizing: border-box;
    font-size: 16px;
    font-family: 'Source Sans Pro', sans-serif;
    transition: all 0.3s;
}

input:focus {
    border-color: #5e81ac;
    outline: none;
    background: #fff;
}

button {
    background: #5e81ac;
    color: #fff;
    border: none;
    padding: 15px 35px;
    border-radius: 4px;
    cursor: pointer;
    margin-top: 15px;
    font-size: 16px;
    font-family: 'Source Sans Pro', sans-serif;
    transition: all 0.3s;
}

button:hover {
    background: #81a1c1;
}

.result {
    margin-top: 30px;
    padding: 20px;
    background: #e5e9f0;
    border-radius: 4px;
}

.hint {
    margin-top: 20px;
    padding: 15px;
    background: #ebcb8b20;
    border-left: 4px solid #ebcb8b;
    border-radius: 4px;
}
''',
            'placeholder': 'Search here...',
            'button_text': 'Search'
        },
        
        'matrix': {
            'name': 'Matrix Code',
            'description': 'Green code rain aesthetic',
            'primary_color': '#0f0',
            'secondary_color': '#0d0',
            'background': '#000',
            'font': "'Courier New', monospace",
            'style': 'matrix',
            'fonts_import': '',
            'css': '''
body {
    font-family: 'Courier New', monospace;
    background: #000;
    color: #0f0;
    margin: 0;
    padding: 0;
    overflow-x: hidden;
    min-height: 100vh;
}

.container {
    max-width: 800px;
    margin: 50px auto;
    padding: 30px;
    background: rgba(0, 20, 0, 0.8);
    border: 2px solid #0f0;
    position: relative;
    animation: glitch 3s infinite;
}

@keyframes glitch {
    0%, 100% { transform: translate(0); }
    20% { transform: translate(-2px, 2px); }
    40% { transform: translate(2px, -2px); }
    60% { transform: translate(-2px, -2px); }
    80% { transform: translate(2px, 2px); }
}

h1 {
    color: #0f0;
    text-shadow: 0 0 5px #0f0;
    animation: flicker 1.5s infinite alternate;
    text-transform: uppercase;
    letter-spacing: 5px;
    margin-top: 0;
}

@keyframes flicker {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.8; }
}

p {
    color: #0d0;
}

input {
    background: #001100;
    border: 1px solid #0f0;
    color: #0f0;
    padding: 12px;
    width: 100%;
    box-sizing: border-box;
    font-family: 'Courier New', monospace;
    font-size: 14px;
}

input:focus {
    outline: none;
    box-shadow: 0 0 10px #0f0;
}

button {
    background: transparent;
    border: 2px solid #0f0;
    color: #0f0;
    padding: 12px 30px;
    cursor: pointer;
    font-family: 'Courier New', monospace;
    text-transform: uppercase;
    margin-top: 10px;
    transition: all 0.3s;
}

button:hover {
    background: #0f0;
    color: #000;
    box-shadow: 0 0 15px #0f0;
}

.result {
    margin-top: 30px;
    border: 1px solid #0f0;
    padding: 15px;
    background: rgba(0, 255, 0, 0.05);
}

.hint {
    margin-top: 20px;
    padding: 15px;
    border: 1px dashed #0f0;
    background: rgba(0, 255, 0, 0.03);
}
''',
            'placeholder': '_ ',
            'button_text': '[ EXECUTE QUERY ]'
        },
        
        'sunset_gradient': {
            'name': 'Sunset Gradient',
            'description': 'Warm sunset colors',
            'primary_color': '#ff6b6b',
            'secondary_color': '#feca57',
            'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%)',
            'font': "'Poppins', sans-serif",
            'style': 'gradient',
            'fonts_import': '<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">',
            'css': '''
body {
    font-family: 'Poppins', sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    background-attachment: fixed;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0;
    padding: 20px;
}

.container {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 25px;
    padding: 50px;
    max-width: 650px;
    width: 100%;
    box-shadow: 0 15px 50px rgba(0, 0, 0, 0.2);
}

h1 {
    background: linear-gradient(135deg, #667eea, #764ba2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-top: 0;
    font-size: 36px;
    font-weight: 600;
}

p {
    color: #555;
}

input {
    background: #f8f9fa;
    border: 2px solid #e9ecef;
    color: #333;
    padding: 15px;
    border-radius: 12px;
    width: 100%;
    box-sizing: border-box;
    font-size: 16px;
    font-family: 'Poppins', sans-serif;
    transition: all 0.3s;
}

input:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

button {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: #fff;
    border: none;
    padding: 15px 40px;
    border-radius: 12px;
    font-weight: 600;
    cursor: pointer;
    margin-top: 15px;
    font-size: 16px;
    transition: all 0.3s;
}

button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
}

.result {
    margin-top: 30px;
    padding: 20px;
    background: linear-gradient(135deg, #f093fb15, #667eea15);
    border-radius: 12px;
    border-left: 4px solid #667eea;
}

.hint {
    margin-top: 20px;
    padding: 15px;
    background: #fff3cd;
    border-left: 4px solid #feca57;
    border-radius: 8px;
    color: #856404;
}
''',
            'placeholder': 'Type your query...',
            'button_text': 'Submit'
        },
        
        'dark_purple': {
            'name': 'Dark Purple',
            'description': 'Deep purple professional theme',
            'primary_color': '#9b59b6',
            'secondary_color': '#8e44ad',
            'background': '#1a1a2e',
            'font': "'Roboto', sans-serif",
            'style': 'dark',
            'fonts_import': '<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap" rel="stylesheet">',
            'css': '''
body {
    font-family: 'Roboto', sans-serif;
    background: #1a1a2e;
    color: #eee;
    margin: 0;
    padding: 20px;
    min-height: 100vh;
}

.container {
    max-width: 850px;
    margin: 60px auto;
    background: #16213e;
    border-radius: 12px;
    padding: 45px;
    border: 1px solid #9b59b6;
    box-shadow: 0 8px 40px rgba(155, 89, 182, 0.3);
}

h1 {
    color: #9b59b6;
    margin-top: 0;
    font-size: 32px;
    font-weight: 500;
}

p {
    color: #ccc;
}

input {
    background: #0f1624;
    border: 2px solid #2a2a4e;
    color: #fff;
    padding: 15px;
    border-radius: 8px;
    width: 100%;
    box-sizing: border-box;
    font-size: 16px;
    transition: all 0.3s;
}

input:focus {
    outline: none;
    border-color: #9b59b6;
    box-shadow: 0 0 15px rgba(155, 89, 182, 0.4);
}

button {
    background: linear-gradient(135deg, #9b59b6, #8e44ad);
    color: #fff;
    border: none;
    padding: 15px 40px;
    border-radius: 8px;
    font-weight: 500;
    cursor: pointer;
    margin-top: 15px;
    transition: all 0.3s;
}

button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(155, 89, 182, 0.5);
}

.result {
    margin-top: 30px;
    padding: 20px;
    background: rgba(155, 89, 182, 0.1);
    border-left: 3px solid #9b59b6;
    border-radius: 5px;
}

.hint {
    margin-top: 20px;
    padding: 15px;
    background: rgba(155, 89, 182, 0.15);
    border-left: 4px solid #9b59b6;
    border-radius: 5px;
}
''',
            'placeholder': 'Search...',
            'button_text': 'Submit Query'
        }
    }
    
    @classmethod
    def get_random_theme(cls):
        """Get a random theme"""
        theme_name = random.choice(list(cls.THEMES.keys()))
        return theme_name, cls.THEMES[theme_name]
    
    @classmethod
    def get_theme(cls, name):
        """Get specific theme by name"""
        return cls.THEMES.get(name, cls.THEMES['dark_hacker'])
    
    @classmethod
    def list_themes(cls):
        """List all available themes"""
        return [
            {
                'id': key,
                'name': theme['name'],
                'description': theme['description'],
                'style': theme['style']
            }
            for key, theme in cls.THEMES.items()
        ]
    
    @classmethod
    def add_custom_theme(cls, theme_id, theme_config):
        """
        Add a custom theme dynamically
        
        Usage:
            ThemeLibrary.add_custom_theme('my_theme', {
                'name': 'My Custom Theme',
                'description': 'Custom description',
                'primary_color': '#123456',
                'css': '...'
            })
        """
        cls.THEMES[theme_id] = theme_config
        print(f"✓ Added custom theme: {theme_config['name']}")


# ============================================================================
# HOW TO ADD MORE THEMES
# ============================================================================

"""
To add a new theme, simply copy this template and fill in your colors/CSS:

'your_theme_name': {
    'name': 'Display Name',
    'description': 'Short description',
    'primary_color': '#HEXCODE',
    'secondary_color': '#HEXCODE',
    'background': 'color or gradient',
    'font': "'Font Name', fallback",
    'style': 'category (dark/light/neon/etc)',
    'fonts_import': '<link...> or empty string',
    'css': '''
    Your complete CSS here
    Include all styles for:
    - body
    - .container
    - h1, p
    - input, button
    - .result, .hint
    ''',
    'placeholder': 'Input placeholder text',
    'button_text': 'Button label'
}

Then add it to the THEMES dictionary above.
"""


# ============================================================================
# EXAMPLE: How to add a new "Ocean Blue" theme
# ============================================================================

OCEAN_BLUE_THEME = {
    'name': 'Ocean Blue',
    'description': 'Calm ocean-inspired design',
    'primary_color': '#0077be',
    'secondary_color': '#00a8e8',
    'background': 'linear-gradient(135deg, #0077be 0%, #00a8e8 100%)',
    'font': "'Nunito', sans-serif",
    'style': 'light',
    'fonts_import': '<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;700&display=swap" rel="stylesheet">',
    'css': '''
body {
    font-family: 'Nunito', sans-serif;
    background: linear-gradient(135deg, #0077be 0%, #00a8e8 100%);
    background-attachment: fixed;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
}

.container {
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 40px;
    border: 1px solid rgba(255, 255, 255, 0.3);
    max-width: 700px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

h1 {
    color: #fff;
    margin-top: 0;
    font-weight: 700;
}

input {
    background: rgba(255, 255, 255, 0.2);
    border: 2px solid rgba(255, 255, 255, 0.3);
    color: #fff;
    padding: 15px;
    border-radius: 10px;
    width: 100%;
    box-sizing: border-box;
    font-size: 16px;
}

input::placeholder {
    color: rgba(255, 255, 255, 0.7);
}

input:focus {
    outline: none;
    background: rgba(255, 255, 255, 0.25);
}

button {
    background: #fff;
    color: #0077be;
    border: none;
    padding: 15px 40px;
    border-radius: 10px;
    font-weight: 700;
    cursor: pointer;
    margin-top: 15px;
}

button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 20px rgba(255, 255, 255, 0.3);
}

.result {
    margin-top: 30px;
    padding: 20px;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 10px;
}

.hint {
    margin-top: 20px;
    padding: 15px;
    background: rgba(255, 255, 255, 0.1);
    border-left: 4px solid rgba(255, 255, 255, 0.5);
    border-radius: 5px;
}
''',
    'placeholder': 'Dive into search...',
    'button_text': 'Explore'
}

# Uncomment to add Ocean Blue theme:
# ThemeLibrary.THEMES['ocean_blue'] = OCEAN_BLUE_THEME
