"""
Cross-Site Scripting Mutation Engine
Generates unique variants of cross-site scripting vulnerabilities
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base import MutationEngine, VulnerabilityBlueprint, MachineConfig
from typing import Dict, List, Any


class CrossSiteScriptingMutation(MutationEngine):
    """
    Mutation engine for Cross-Site Scripting vulnerabilities
    """

    def mutate(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> MachineConfig:
        """Generate unique cross-site scripting machine configuration"""

        # Select variant based on difficulty
        variant = self._select_variant(blueprint.variants, difficulty)

        # Generate machine ID
        machine_id = self.generate_machine_id()

        # Generate configuration based on variant
        if variant == "Reflected XSS":
            config = self._generate_reflected_xss(blueprint, difficulty)
        elif variant == "Stored XSS":
            config = self._generate_stored_xss(blueprint, difficulty)
        elif variant == "DOM-based XSS":
            config = self._generate_dom_based_xss(blueprint, difficulty)
        else:
            config = self._generate_reflected_xss(blueprint, difficulty)

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

    def _generate_reflected_xss(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> Dict:
        """Generate Reflected XSS vulnerability configuration"""

        context = self.select_random(blueprint.mutation_axes.get('contexts', ['search_box']))
        sink = self.select_random(blueprint.mutation_axes.get('sinks', ['innerHTML']))
        output_context = self.select_random(blueprint.mutation_axes.get('output_contexts', ['html_body']))
        entry_point = self.select_random(blueprint.entry_points)

        # Select filters based on difficulty
        if difficulty == 1:
            filters = []
        elif difficulty == 2:
            filters = self._get_filter_codes(blueprint.mutation_axes.get('filters', {}).get('basic', []))
        elif difficulty == 3:
            filters = self._get_filter_codes(blueprint.mutation_axes.get('filters', {}).get('medium', []))
        else:
            filters = self._get_filter_codes(blueprint.mutation_axes.get('filters', {}).get('advanced', []))

        flag_content = self.generate_flag()
        hints = self._generate_hints(filters, context, difficulty)

        return {
            'application': {
                'context': context,
                'variant': 'Reflected XSS',
                'entry_point': entry_point,
            },
            'constraints': {
                'filters': filters,
            },
            'flag': {
                'content': flag_content,
                'location': '/var/www/html/flag.txt',
            },
            'behavior': {
                'output': 'direct_echo',
            },
            'metadata': {
                'exploit_hints': hints,
                'vulnerability_type': 'Reflected XSS',
                'estimated_solve_time': f"{difficulty * 10}-{difficulty * 15} minutes",
            }
        }

    def _generate_stored_xss(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> Dict:
        """Generate Stored XSS vulnerability configuration"""

        context = self.select_random(blueprint.mutation_axes.get('contexts', ['comment_section']))
        sink = self.select_random(blueprint.mutation_axes.get('sinks', ['innerHTML']))
        storage = self.select_random(blueprint.mutation_axes.get('storage_types', ['database']))
        entry_point = self.select_random(blueprint.entry_points)

        # Select filters based on difficulty
        if difficulty == 1:
            filters = []
        elif difficulty == 2:
            filters = self._get_filter_codes(blueprint.mutation_axes.get('filters', {}).get('basic', []))
        elif difficulty == 3:
            filters = self._get_filter_codes(blueprint.mutation_axes.get('filters', {}).get('medium', []))
        else:
            filters = self._get_filter_codes(blueprint.mutation_axes.get('filters', {}).get('advanced', []))

        flag_content = self.generate_flag()
        hints = self._generate_hints(filters, context, difficulty)

        return {
            'application': {
                'context': context,
                'variant': 'Stored XSS',
                'entry_point': entry_point,
            },
            'constraints': {
                'filters': filters,
            },
            'flag': {
                'content': flag_content,
                'location': '/var/www/html/flag.txt',
            },
            'behavior': {
                'output': 'direct_echo',
            },
            'metadata': {
                'exploit_hints': hints,
                'vulnerability_type': 'Stored XSS',
                'estimated_solve_time': f"{difficulty * 10}-{difficulty * 15} minutes",
            }
        }

    def _generate_dom_based_xss(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> Dict:
        """Generate DOM-based XSS vulnerability configuration"""

        context = self.select_random(blueprint.mutation_axes.get('contexts', ['user_profile']))
        sink = self.select_random(blueprint.mutation_axes.get('sinks', ['location_href']))
        entry_point = self.select_random(blueprint.entry_points)

        # Select filters based on difficulty
        if difficulty == 1:
            filters = []
        elif difficulty == 2:
            filters = self._get_filter_codes(blueprint.mutation_axes.get('filters', {}).get('basic', []))
        elif difficulty == 3:
            filters = self._get_filter_codes(blueprint.mutation_axes.get('filters', {}).get('medium', []))
        else:
            filters = self._get_filter_codes(blueprint.mutation_axes.get('filters', {}).get('advanced', []))

        flag_content = self.generate_flag()
        hints = self._generate_hints(filters, context, difficulty)

        return {
            'application': {
                'context': context,
                'variant': 'DOM-based XSS',
                'entry_point': entry_point,
            },
            'constraints': {
                'filters': filters,
            },
            'flag': {
                'content': flag_content,
                'location': '/var/www/html/flag.txt',
            },
            'behavior': {
                'output': 'direct_echo',
            },
            'metadata': {
                'exploit_hints': hints,
                'vulnerability_type': 'DOM-based XSS',
                'estimated_solve_time': f"{difficulty * 10}-{difficulty * 15} minutes",
            }
        }


    def _get_filter_codes(self, filter_names: List[str]) -> List[Dict]:
        """Convert filter names to filter code objects"""
        filter_map = {
            'script_tag': {
                'type': 'script_tag',
                'description': 'Script_tag filtering',
                'php_code': "$input = str_replace('s', '', $input);",
                'python_code': "input = input.replace('s', '')",
            },
            'onerror': {
                'type': 'onerror',
                'description': 'Onerror filtering',
                'php_code': "$input = str_replace('o', '', $input);",
                'python_code': "input = input.replace('o', '')",
            },
            'onclick': {
                'type': 'onclick',
                'description': 'Onclick filtering',
                'php_code': "$input = str_replace('o', '', $input);",
                'python_code': "input = input.replace('o', '')",
            },
            'javascript_protocol': {
                'type': 'javascript_protocol',
                'description': 'Javascript_protocol filtering',
                'php_code': "$input = str_replace('j', '', $input);",
                'python_code': "input = input.replace('j', '')",
            },
            'angle_brackets': {
                'type': 'angle_brackets',
                'description': 'Angle_brackets filtering',
                'php_code': "$input = str_replace('a', '', $input);",
                'python_code': "input = input.replace('a', '')",
            },
            'quotes': {
                'type': 'quotes',
                'description': 'Quotes filtering',
                'php_code': "$input = str_replace('q', '', $input);",
                'python_code': "input = input.replace('q', '')",
            }
        }

        return [filter_map[f] for f in filter_names if f in filter_map]

    def _generate_hints(self, filters: List[Dict], context: str, difficulty: int) -> List[str]:
        """Generate context-specific hints"""
        hints = [
            f"Context: {context}",
            f"Difficulty: {difficulty}/5",
        ]

        if not filters:
            hints.append("✓ No input filtering - direct attack possible")
        else:
            hints.append(f"⚠️ Filters active: {', '.join([f['type'] for f in filters])}")

        if difficulty <= 2:
            hints.append("💡 Try basic payloads first")

        return hints
