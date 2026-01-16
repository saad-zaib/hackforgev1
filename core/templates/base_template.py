"""
Base Template Classes
Abstract interfaces for code generation
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
import sys
import os
import importlib

# Add paths for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from base import MachineConfig


class BaseTemplate(ABC):
    """
    Abstract base class for all templates
    """

    def __init__(self, config: MachineConfig):
        self.config = config
        self.machine_id = config.machine_id
        self.variant = config.variant
        self.difficulty = config.difficulty

    @abstractmethod
    def generate_code(self) -> str:
        """Generate the vulnerable application code"""
        pass

    @abstractmethod
    def generate_dockerfile(self) -> str:
        """Generate Dockerfile for the application"""
        pass

    def generate_docker_compose(self, port: int) -> str:
        """Generate docker-compose.yml entry"""
        flag_location = self.config.flag.get('location', '/var/www/html/flag.txt')

        return f"""
  machine_{self.machine_id}:
    build: ./machines/{self.machine_id}
    container_name: hackforge_{self.machine_id}
    ports:
      - "{port}:80"
    volumes:
      - ./machines/{self.machine_id}/app:/var/www/html
      - ./machines/{self.machine_id}/flag.txt:{flag_location}:ro
    environment:
      - MACHINE_ID={self.machine_id}
      - DIFFICULTY={self.difficulty}
"""

    def get_flag_content(self) -> str:
        """Get flag content"""
        return self.config.flag['content']

    def get_hints(self) -> list:
        """Get exploitation hints"""
        return self.config.metadata.get('exploit_hints', [])


class TemplateRenderer:
    """
    Factory class for rendering templates based on vulnerability type
    """

    @staticmethod
    def _get_category_from_blueprint(blueprint_id: str) -> str:
        """
        Load blueprint and extract category
        
        Args:
            blueprint_id: Blueprint identifier (e.g., 'xss_001')
            
        Returns:
            Category name (e.g., 'cross_site_scripting')
        """
        import yaml
        from pathlib import Path
        
        # Look for blueprint file in blueprints directory
        blueprints_dir = Path(parent_dir) / "blueprints"
        
        # Try to find blueprint by ID
        for blueprint_file in blueprints_dir.glob("*_blueprint.yaml"):
            try:
                with open(blueprint_file, 'r') as f:
                    data = yaml.safe_load(f)
                    if data.get('blueprint_id') == blueprint_id:
                        return data.get('category')
            except Exception as e:
                continue
        
        # If not found, return blueprint_id as fallback
        return blueprint_id

    @staticmethod
    def get_template_class(config: MachineConfig):
        """
        Dynamically load template class based on category
        
        Args:
            config: MachineConfig object
            
        Returns:
            Template class for the vulnerability category
        """
        
        # Get category from blueprint
        category = TemplateRenderer._get_category_from_blueprint(config.blueprint_id)
        
        # Convert category to template module name
        # e.g., 'cross_site_scripting' -> 'cross_site_scripting_templates'
        template_module_name = f"{category}_templates"
        
        # Convert category to class name
        # e.g., 'cross_site_scripting' -> 'CrossSiteScriptingTemplate'
        class_name = ''.join(word.capitalize() for word in category.split('_')) + 'Template'
        
        try:
            # Try to import the template module dynamically
            module = importlib.import_module(f"templates.{template_module_name}")
            
            # Get the template class from the module
            template_class = getattr(module, class_name)
            
            return template_class
            
        except ImportError as e:
            raise ValueError(
                f"No template module found for category: {category}\n"
                f"Expected module: templates/{template_module_name}.py\n"
                f"Expected class: {class_name}\n"
                f"Error: {e}"
            )
        except AttributeError as e:
            raise ValueError(
                f"Template class not found in module\n"
                f"Module: templates/{template_module_name}.py\n"
                f"Expected class: {class_name}\n"
                f"Error: {e}"
            )

    @staticmethod
    def render(config: MachineConfig) -> Dict[str, str]:
        """
        Render machine config to code

        Args:
            config: MachineConfig object

        Returns:
            Dict with 'code', 'dockerfile', 'docker_compose', 'flag', 'hints'
        """

        template_class = TemplateRenderer.get_template_class(config)
        template = template_class(config)

        return {
            'code': template.generate_code(),
            'dockerfile': template.generate_dockerfile(),
            'docker_compose': template.generate_docker_compose(8080),
            'flag': template.get_flag_content(),
            'hints': template.get_hints(),
        }
