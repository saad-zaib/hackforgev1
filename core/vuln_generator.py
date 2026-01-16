"""
UPDATED vuln_generator.py - Now includes theme variety support
Replace your existing core/vuln_generator.py with this version
"""

#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path


class VulnerabilityGenerator:

    def __init__(self, config_path: str):
        with open(config_path, 'r') as f:
            self.config = json.load(f)

        self.vuln_id = self.config['vulnerability_id']
        self.vuln_name = self.config['name']
        self.category = self.config['category']

    def generate_all(self, base_dir: str = "."):
        """Generate all three components in their respective directories"""

        # Create directories if they don't exist
        blueprint_dir = os.path.join(base_dir, "blueprints")
        mutation_dir = os.path.join(base_dir, "mutations")
        template_dir = os.path.join(base_dir, "templates")

        os.makedirs(blueprint_dir, exist_ok=True)
        os.makedirs(mutation_dir, exist_ok=True)
        os.makedirs(template_dir, exist_ok=True)

        # Use category for all filenames for consistency
        blueprint_path = os.path.join(blueprint_dir, f"{self.category}_blueprint.yaml")
        mutation_path = os.path.join(mutation_dir, f"{self.category}_mutation.py")
        template_path = os.path.join(template_dir, f"{self.category}_templates.py")

        with open(blueprint_path, 'w') as f:
            f.write(self.generate_blueprint())

        with open(mutation_path, 'w') as f:
            f.write(self.generate_mutation())

        with open(template_path, 'w') as f:
            f.write(self.generate_template())

        print(f"✅ Blueprint: {blueprint_path}")
        print(f"✅ Mutation:  {mutation_path}")
        print(f"✅ Template:  {template_path}")
        print(f"\n💡 All files use category '{self.category}' for consistency")

    def generate_blueprint(self) -> str:
        """Generate blueprint YAML content"""

        variants = self.config.get('variants', [])
        entry_points = self.config.get('entry_points', [])
        mutation_axes = self.config.get('mutation_axes', {})

        blueprint = f"""blueprint_id: {self.vuln_id}

name: {self.vuln_name}

category: {self.category}

difficulty_range: {self.config.get('difficulty_range', [1, 5])}

description: |
  {self.config.get('description', 'Vulnerability description')}

variants:
{self._format_list(variants)}

entry_points:
{self._format_list(entry_points)}

mutation_axes:
{self._format_mutation_axes(mutation_axes)}
"""
        return blueprint

    def generate_mutation(self) -> str:
        """Generate mutation engine Python code"""

        class_name = self._to_class_name(self.vuln_name) + "Mutation"
        variants = self.config.get('variants', [])

        # Generate variant methods
        variant_methods = []
        for variant in variants:
            method_name = self._to_method_name(variant)
            variant_methods.append(self._generate_variant_method(variant, method_name))

        mutation_code = f'''"""
{self.vuln_name} Mutation Engine
Generates unique variants of {self.vuln_name.lower()} vulnerabilities
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base import MutationEngine, VulnerabilityBlueprint, MachineConfig
from typing import Dict, List, Any


class {class_name}(MutationEngine):
    """
    Mutation engine for {self.vuln_name} vulnerabilities
    """

    def mutate(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> MachineConfig:
        """Generate unique {self.vuln_name.lower()} machine configuration"""

        # Select variant based on difficulty
        variant = self._select_variant(blueprint.variants, difficulty)

        # Generate machine ID
        machine_id = self.generate_machine_id()

        # Generate configuration based on variant
{self._generate_variant_dispatch(variants)}

        # Create machine config
        return MachineConfig(
            machine_id=machine_id,
            blueprint_id=blueprint.blueprint_id,
            variant=variant,
            difficulty=difficulty,
            seed=self.seed,
            application=config['application'],
            constraints=config['constraints'],
            flag=config['flag'],
            behavior=config['behavior'],
            metadata=config['metadata']
        )

    def _select_variant(self, variants: List[str], difficulty: int) -> str:
        """Select variant based on difficulty level"""
        if difficulty <= 2:
            easy_variants = variants[:len(variants)//2] if len(variants) > 2 else variants
            return self.select_random(easy_variants)
        else:
            return self.select_random(variants)

{chr(10).join(variant_methods)}

    def _get_filter_codes(self, filter_names: List[str]) -> List[Dict]:
        """Convert filter names to filter code objects"""
        filter_map = {{
{self._generate_filter_map()}
        }}

        return [filter_map[f] for f in filter_names if f in filter_map]

    def _generate_hints(self, filters: List[Dict], context: str, difficulty: int) -> List[str]:
        """Generate context-specific hints"""
        hints = [
            f"Context: {{context}}",
            f"Difficulty: {{difficulty}}/5",
        ]

        if not filters:
            hints.append("✓ No input filtering - direct attack possible")
        else:
            hints.append(f"⚠️ Filters active: {{', '.join([f['type'] for f in filters])}}")

        if difficulty <= 2:
            hints.append("💡 Try basic payloads first")

        return hints
'''
        return mutation_code

    def generate_template(self) -> str:
        """Generate template Python code WITH THEME SUPPORT"""

        class_name = self._to_class_name(self.vuln_name) + "Template"
        variants = self.config.get('variants', [])

        # Generate variant template methods
        variant_templates = []
        for variant in variants:
            method_name = self._to_method_name(variant)
            variant_templates.append(self._generate_template_method(variant, method_name))

        template_code = f'''"""
{self.vuln_name} Vulnerability Templates
Generates vulnerable applications with theme variety
"""

import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from templates.base_template import BaseTemplate
from templates.theme_library import ThemeLibrary  # ← THEME SUPPORT
from typing import Dict


class {class_name}(BaseTemplate):
    """
    Template generator for {self.vuln_name.lower()} vulnerabilities
    """

    def __init__(self, config):
        super().__init__(config)
        # Pick random theme for this machine
        self.theme_name, self.theme = ThemeLibrary.get_random_theme()
        print(f"  🎨 Theme: {{self.theme['name']}}")

    def generate_code(self) -> str:
        """Generate vulnerable application based on variant"""

        variant = self.config.variant

{self._generate_template_dispatch(variants)}

{chr(10).join(variant_templates)}

    def _generate_filter_code(self, filters: list, language: str) -> str:
        """Generate filter code from filter list"""
        if not filters:
            return ""

        if language == 'php':
            return "\\n            ".join([f['php_code'] for f in filters])
        elif language == 'python':
            return "\\n    ".join([f['python_code'] for f in filters])

        return ""

    def generate_dockerfile(self) -> str:
        """Generate Dockerfile for {self.vuln_name.lower()} vulnerabilities"""

        return \'\'\'FROM php:8.0-apache

RUN apt-get update && apt-get install -y \\\\
    iputils-ping \\\\
    whois \\\\
    dnsutils \\\\
    && rm -rf /var/lib/apt/lists/*

EXPOSE 80

CMD ["apache2-foreground"]
\'\'\'
'''
        return template_code

    # Helper methods

    def _format_list(self, items: list) -> str:
        """Format list for YAML"""
        return '\n'.join([f"  - {item}" for item in items])

    def _format_mutation_axes(self, axes: dict) -> str:
        """Format mutation axes for YAML"""
        result = []
        for key, value in axes.items():
            result.append(f"  {key}:")
            if isinstance(value, dict):
                for subkey, subvalue in value.items():
                    result.append(f"    {subkey}:")
                    if isinstance(subvalue, list):
                        for item in subvalue:
                            result.append(f"      - {item}")
            elif isinstance(value, list):
                for item in value:
                    result.append(f"    - {item}")
        return '\n'.join(result)

    def _to_class_name(self, name: str) -> str:
        """Convert name to class name"""
        return ''.join(word.capitalize() for word in name.replace('-', ' ').split())

    def _to_method_name(self, name: str) -> str:
        """Convert name to method name"""
        return '_generate_' + name.lower().replace(' ', '_').replace('-', '_')

    def _generate_variant_dispatch(self, variants: list) -> str:
        """Generate if-elif chain for variant dispatch"""
        lines = []
        for i, variant in enumerate(variants):
            method_name = self._to_method_name(variant)
            if i == 0:
                lines.append(f'        if variant == "{variant}":')
            else:
                lines.append(f'        elif variant == "{variant}":')
            lines.append(f'            config = self.{method_name}(blueprint, difficulty)')
        lines.append('        else:')
        lines.append(f'            config = self.{self._to_method_name(variants[0])}(blueprint, difficulty)')
        return '\n'.join(lines)

    def _generate_template_dispatch(self, variants: list) -> str:
        """Generate if-elif chain for template dispatch"""
        lines = []
        for i, variant in enumerate(variants):
            method_name = self._to_method_name(variant)
            if i == 0:
                lines.append(f'        if variant == "{variant}":')
            else:
                lines.append(f'        elif variant == "{variant}":')
            lines.append(f'            return self.{method_name}()')
        lines.append('        else:')
        lines.append(f'            return self.{self._to_method_name(variants[0])}()')
        return '\n'.join(lines)

    def _generate_variant_method(self, variant: str, method_name: str) -> str:
        """Generate a variant mutation method"""

        variant_config = next((v for v in self.config.get('variant_configs', []) if v['name'] == variant), None)

        if not variant_config:
            # Default template
            return f'''    def {method_name}(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> Dict:
        """Generate {variant} vulnerability configuration"""

        context = self.select_random(blueprint.mutation_axes.get('contexts', ['default_context']))
        entry_point = self.select_random(blueprint.entry_points)

        # Select filters based on difficulty
        if difficulty == 1:
            filters = []
        elif difficulty == 2:
            filters = self._get_filter_codes(blueprint.mutation_axes.get('filters', {{}}).get('basic', []))
        elif difficulty == 3:
            filters = self._get_filter_codes(blueprint.mutation_axes.get('filters', {{}}).get('medium', []))
        else:
            filters = self._get_filter_codes(blueprint.mutation_axes.get('filters', {{}}).get('advanced', []))

        flag_content = self.generate_flag()
        hints = self._generate_hints(filters, context, difficulty)

        return {{
            'application': {{
                'context': context,
                'variant': '{variant}',
                'entry_point': entry_point,
            }},
            'constraints': {{
                'filters': filters,
            }},
            'flag': {{
                'content': flag_content,
                'location': '/var/www/html/flag.txt',
            }},
            'behavior': {{
                'output': 'direct_echo',
            }},
            'metadata': {{
                'exploit_hints': hints,
                'vulnerability_type': '{variant}',
                'estimated_solve_time': f"{{difficulty * 10}}-{{difficulty * 15}} minutes",
            }}
        }}
'''

        # Custom configuration
        params = variant_config.get('parameters', [])
        param_setup = '\n        '.join([f"{p['name']} = self.select_random(blueprint.mutation_axes.get('{p['axis']}', ['{p.get('default', 'default')}']))" for p in params])

        return f'''    def {method_name}(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> Dict:
        """Generate {variant} vulnerability configuration"""

        {param_setup}
        entry_point = self.select_random(blueprint.entry_points)

        # Select filters based on difficulty
        if difficulty == 1:
            filters = []
        elif difficulty == 2:
            filters = self._get_filter_codes(blueprint.mutation_axes.get('filters', {{}}).get('basic', []))
        elif difficulty == 3:
            filters = self._get_filter_codes(blueprint.mutation_axes.get('filters', {{}}).get('medium', []))
        else:
            filters = self._get_filter_codes(blueprint.mutation_axes.get('filters', {{}}).get('advanced', []))

        flag_content = self.generate_flag()
        hints = self._generate_hints(filters, context, difficulty)

        return {{
            'application': {{
                'context': context,
                'variant': '{variant}',
                'entry_point': entry_point,
            }},
            'constraints': {{
                'filters': filters,
            }},
            'flag': {{
                'content': flag_content,
                'location': '/var/www/html/flag.txt',
            }},
            'behavior': {{
                'output': 'direct_echo',
            }},
            'metadata': {{
                'exploit_hints': hints,
                'vulnerability_type': '{variant}',
                'estimated_solve_time': f"{{difficulty * 10}}-{{difficulty * 15}} minutes",
            }}
        }}
'''


    def _generate_template_method(self, variant: str, method_name: str) -> str:
        """Generate a variant template method WITH THEME SUPPORT"""

        # This generates themed HTML templates
        # FIXED: Use proper brace escaping for multi-level string generation
        return f'''    def {method_name}(self) -> str:
        """Generate {variant} vulnerable application with themed UI"""

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

        php_code = f\'\'\'<?php
/**
 * Hackforge Machine: {{self.machine_id}}
 * Vulnerability: {variant}
 * Theme: {{self.theme['name']}}
 * Difficulty: {{self.difficulty}}/5
 */
?>
<!DOCTYPE html>
<html>
<head>
    <title>{variant} Challenge</title>
    {{fonts_import}}
    <style>
{{theme_css}}
    </style>
</head>
<body>
    <div class="container">
        <h1>{variant}</h1>
        <p>Context: {{context}}</p>

        <form method="GET">
            <input type="text" name="input" placeholder="{{placeholder}}">
            <button type="submit">{{button_text}}</button>
        </form>

        <?php
        if (isset($_GET['input'])) {{{{
            $input = $_GET['input'];
            {{filter_code if filter_code else '// No filters'}}
            echo '<div class="result">';
            echo '<h3>Results:</h3>';
            echo '<div>' . $input . '</div>';
            echo '</div>';
        }}}}
        ?>

        <div class="hint">
            <strong>💡 Hint:</strong> This is a {{context}} context. Can you find the vulnerability?
        </div>
    </div>
</body>
</html>\'\'\'

        return php_code
'''

    def _generate_filter_map(self) -> str:
        """Generate filter mapping code"""
        filters = self.config.get('mutation_axes', {}).get('filters', {})

        filter_entries = []
        for category, filter_list in filters.items():
            if category in ['basic', 'medium', 'advanced']:
                for filter_name in filter_list:
                    if filter_name not in [e.split(':')[0].strip().strip("'") for e in filter_entries]:
                        filter_entries.append(f"""            '{filter_name}': {{
                'type': '{filter_name}',
                'description': '{filter_name.capitalize()} filtering',
                'php_code': "$input = str_replace('{filter_name[0]}', '', $input);",
                'python_code': "input = input.replace('{filter_name[0]}', '')",
            }}""")

        return ',\n'.join(filter_entries) if filter_entries else "            # No filters defined"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python vuln_generator.py <config.json>")
        print("Example: python vuln_generator.py xss_config.json")
        sys.exit(1)

    config_path = sys.argv[1]

    generator = VulnerabilityGenerator(config_path)
    generator.generate_all(".")

    print(f"\n✨ Done! Templates will now use random themes for variety!")
