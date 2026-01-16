"""
SQL Injection Vulnerability Templates
Generates vulnerable applications with theme variety
"""

import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from templates.base_template import BaseTemplate
from templates.theme_library import ThemeLibrary  # ← THEME SUPPORT
from typing import Dict


class SqlInjectionTemplate(BaseTemplate):
    """
    Template generator for sql injection vulnerabilities
    """

    def __init__(self, config):
        super().__init__(config)
        # Pick random theme for this machine
        self.theme_name, self.theme = ThemeLibrary.get_random_theme()
        print(f"  🎨 Theme: {self.theme['name']}")

    def generate_code(self) -> str:
        """Generate vulnerable application based on variant"""

        variant = self.config.variant

        if variant == "Error-based SQLi":
            return self._generate_error_based_sqli()
        elif variant == "Union-based SQLi":
            return self._generate_union_based_sqli()
        elif variant == "Blind SQLi":
            return self._generate_blind_sqli()
        elif variant == "Time-based Blind SQLi":
            return self._generate_time_based_blind_sqli()
        else:
            return self._generate_error_based_sqli()

    def _generate_error_based_sqli(self) -> str:
        """Generate Error-based SQLi vulnerable application with themed UI"""

        app = self.config.application
        constraints = self.config.constraints

        context = app.get('context', 'default')
        filters = constraints.get('filters', [])

        filter_code = self._generate_filter_code(filters, 'php')

        # Get theme CSS and properties
        theme_css = self.theme['css']
        fonts_import = self.theme.get('fonts_import', '')
        placeholder = self.theme.get('placeholder', 'Enter input')
        button_text = self.theme.get('button_text', 'Submit')

        php_code = f'''<?php
/**
 * Hackforge Machine: {self.machine_id}
 * Vulnerability: Error-based SQLi
 * Theme: {self.theme['name']}
 * Difficulty: {self.difficulty}/5
 */
?>
<!DOCTYPE html>
<html>
<head>
    <title>Error-based SQLi Challenge</title>
    {fonts_import}
    <style>
{theme_css}
    </style>
</head>
<body>
    <div class="container">
        <h1>Error-based SQLi</h1>
        <p>Context: {context}</p>

        <form method="GET">
            <input type="text" name="input" placeholder="{placeholder}">
            <button type="submit">{button_text}</button>
        </form>

        <?php
        if (isset($_GET['input'])) {{
            $input = $_GET['input'];
            {filter_code if filter_code else '// No filters'}
            echo '<div class="result">';
            echo '<h3>Results:</h3>';
            echo '<div>' . $input . '</div>';
            echo '</div>';
        }}
        ?>

        <div class="hint">
            <strong>💡 Hint:</strong> This is a {context} context. Can you find the vulnerability?
        </div>
    </div>
</body>
</html>'''

        return php_code

    def _generate_union_based_sqli(self) -> str:
        """Generate Union-based SQLi vulnerable application with themed UI"""

        app = self.config.application
        constraints = self.config.constraints

        context = app.get('context', 'default')
        filters = constraints.get('filters', [])

        filter_code = self._generate_filter_code(filters, 'php')

        # Get theme CSS and properties
        theme_css = self.theme['css']
        fonts_import = self.theme.get('fonts_import', '')
        placeholder = self.theme.get('placeholder', 'Enter input')
        button_text = self.theme.get('button_text', 'Submit')

        php_code = f'''<?php
/**
 * Hackforge Machine: {self.machine_id}
 * Vulnerability: Union-based SQLi
 * Theme: {self.theme['name']}
 * Difficulty: {self.difficulty}/5
 */
?>
<!DOCTYPE html>
<html>
<head>
    <title>Union-based SQLi Challenge</title>
    {fonts_import}
    <style>
{theme_css}
    </style>
</head>
<body>
    <div class="container">
        <h1>Union-based SQLi</h1>
        <p>Context: {context}</p>

        <form method="GET">
            <input type="text" name="input" placeholder="{placeholder}">
            <button type="submit">{button_text}</button>
        </form>

        <?php
        if (isset($_GET['input'])) {{
            $input = $_GET['input'];
            {filter_code if filter_code else '// No filters'}
            echo '<div class="result">';
            echo '<h3>Results:</h3>';
            echo '<div>' . $input . '</div>';
            echo '</div>';
        }}
        ?>

        <div class="hint">
            <strong>💡 Hint:</strong> This is a {context} context. Can you find the vulnerability?
        </div>
    </div>
</body>
</html>'''

        return php_code

    def _generate_blind_sqli(self) -> str:
        """Generate Blind SQLi vulnerable application with themed UI"""

        app = self.config.application
        constraints = self.config.constraints

        context = app.get('context', 'default')
        filters = constraints.get('filters', [])

        filter_code = self._generate_filter_code(filters, 'php')

        # Get theme CSS and properties
        theme_css = self.theme['css']
        fonts_import = self.theme.get('fonts_import', '')
        placeholder = self.theme.get('placeholder', 'Enter input')
        button_text = self.theme.get('button_text', 'Submit')

        php_code = f'''<?php
/**
 * Hackforge Machine: {self.machine_id}
 * Vulnerability: Blind SQLi
 * Theme: {self.theme['name']}
 * Difficulty: {self.difficulty}/5
 */
?>
<!DOCTYPE html>
<html>
<head>
    <title>Blind SQLi Challenge</title>
    {fonts_import}
    <style>
{theme_css}
    </style>
</head>
<body>
    <div class="container">
        <h1>Blind SQLi</h1>
        <p>Context: {context}</p>

        <form method="GET">
            <input type="text" name="input" placeholder="{placeholder}">
            <button type="submit">{button_text}</button>
        </form>

        <?php
        if (isset($_GET['input'])) {{
            $input = $_GET['input'];
            {filter_code if filter_code else '// No filters'}
            echo '<div class="result">';
            echo '<h3>Results:</h3>';
            echo '<div>' . $input . '</div>';
            echo '</div>';
        }}
        ?>

        <div class="hint">
            <strong>💡 Hint:</strong> This is a {context} context. Can you find the vulnerability?
        </div>
    </div>
</body>
</html>'''

        return php_code

    def _generate_time_based_blind_sqli(self) -> str:
        """Generate Time-based Blind SQLi vulnerable application with themed UI"""

        app = self.config.application
        constraints = self.config.constraints

        context = app.get('context', 'default')
        filters = constraints.get('filters', [])

        filter_code = self._generate_filter_code(filters, 'php')

        # Get theme CSS and properties
        theme_css = self.theme['css']
        fonts_import = self.theme.get('fonts_import', '')
        placeholder = self.theme.get('placeholder', 'Enter input')
        button_text = self.theme.get('button_text', 'Submit')

        php_code = f'''<?php
/**
 * Hackforge Machine: {self.machine_id}
 * Vulnerability: Time-based Blind SQLi
 * Theme: {self.theme['name']}
 * Difficulty: {self.difficulty}/5
 */
?>
<!DOCTYPE html>
<html>
<head>
    <title>Time-based Blind SQLi Challenge</title>
    {fonts_import}
    <style>
{theme_css}
    </style>
</head>
<body>
    <div class="container">
        <h1>Time-based Blind SQLi</h1>
        <p>Context: {context}</p>

        <form method="GET">
            <input type="text" name="input" placeholder="{placeholder}">
            <button type="submit">{button_text}</button>
        </form>

        <?php
        if (isset($_GET['input'])) {{
            $input = $_GET['input'];
            {filter_code if filter_code else '// No filters'}
            echo '<div class="result">';
            echo '<h3>Results:</h3>';
            echo '<div>' . $input . '</div>';
            echo '</div>';
        }}
        ?>

        <div class="hint">
            <strong>💡 Hint:</strong> This is a {context} context. Can you find the vulnerability?
        </div>
    </div>
</body>
</html>'''

        return php_code


    def _generate_filter_code(self, filters: list, language: str) -> str:
        """Generate filter code from filter list"""
        if not filters:
            return ""

        if language == 'php':
            return "\n            ".join([f['php_code'] for f in filters])
        elif language == 'python':
            return "\n    ".join([f['python_code'] for f in filters])

        return ""

    def generate_dockerfile(self) -> str:
        """Generate Dockerfile for sql injection vulnerabilities"""

        return '''FROM php:8.0-apache

RUN apt-get update && apt-get install -y \\
    iputils-ping \\
    whois \\
    dnsutils \\
    && rm -rf /var/lib/apt/lists/*

EXPOSE 80

CMD ["apache2-foreground"]
'''
