#!/usr/bin/env python3
"""
Template Engine
Converts machine configs to deployable applications
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base import MachineConfig
from templates.base_template import TemplateRenderer


class TemplateEngine:
    """
    Main template engine that converts configs to code
    """

    def __init__(self, machines_dir: str = "generated_machines"):
        self.machines_dir = Path(machines_dir)
        
        if not self.machines_dir.exists():
            print(f"⚠️  Machines directory not found: {self.machines_dir}")
            self.machines_dir.mkdir(parents=True, exist_ok=True)

    def generate_machine_app(self, config: MachineConfig, machine_dir: Path) -> Dict[str, str]:
        """
        Generate complete application from machine config

        Args:
            config: MachineConfig object
            machine_dir: Directory where machine files exist

        Returns:
            Dict with paths to generated files
        """

        print(f"\n🔨 Generating application for machine: {config.machine_id}")
        print(f"   Variant: {config.variant}")
        print(f"   Difficulty: {config.difficulty}/5")

        # Create app directory
        app_dir = machine_dir / "app"
        app_dir.mkdir(exist_ok=True)

        try:
            # Render templates
            rendered = TemplateRenderer.render(config)

            # Write application code
            app_file = app_dir / "index.php"
            app_file.write_text(rendered['code'])
            print(f"   ✓ Generated: {app_file}")

            # Write Dockerfile
            dockerfile = machine_dir / "Dockerfile"
            dockerfile.write_text(rendered['dockerfile'])
            print(f"   ✓ Generated: {dockerfile}")

            # Write flag (already exists, but update it)
            flag_file = machine_dir / "flag.txt"
            flag_file.write_text(rendered['flag'])
            print(f"   ✓ Updated: {flag_file}")

            # Write hints
            hints_file = machine_dir / "HINTS.md"
            hints_content = f"""# Exploitation Hints

**Machine ID:** `{config.machine_id}`
**Variant:** {config.variant}
**Difficulty:** {config.difficulty}/5

## Hints

"""
            for i, hint in enumerate(rendered['hints'], 1):
                hints_content += f"{i}. {hint}\n"

            hints_content += f"\n## Flag\n\n`{rendered['flag']}`\n"
            hints_file.write_text(hints_content)
            print(f"   ✓ Generated: {hints_file}")

            return {
                'machine_id': config.machine_id,
                'machine_dir': str(machine_dir),
                'app_file': str(app_file),
                'dockerfile': str(dockerfile),
                'flag_file': str(flag_file),
                'hints_file': str(hints_file),
            }

        except Exception as e:
            print(f"   ✗ Error generating machine: {e}")
            import traceback
            traceback.print_exc()
            return None

    def process_all_machines(self, start_port: int = 8080) -> List[Dict]:
        """
        Process all machine configs in the machines directory

        Args:
            start_port: Starting port number

        Returns:
            List of generated machine info
        """

        print(f"\n{'='*60}")
        print(f"Processing Machines in: {self.machines_dir}")
        print(f"{'='*60}")

        machines_generated = []
        port = start_port

        # Find all machine directories with config.json
        machine_dirs = []
        for item in self.machines_dir.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                config_file = item / "config.json"
                if config_file.exists():
                    machine_dirs.append(item)

        print(f"\nFound {len(machine_dirs)} machine(s) to process")

        for machine_dir in machine_dirs:
            config_file = machine_dir / "config.json"
            
            print(f"\nProcessing: {machine_dir.name}")

            try:
                # Load config
                with open(config_file, 'r') as f:
                    config_dict = json.load(f)

                # Convert dict to MachineConfig
                config = MachineConfig(**config_dict)

                # Generate application
                result = self.generate_machine_app(config, machine_dir)

                if result:
                    result['port'] = port
                    machines_generated.append(result)
                    port += 1

            except Exception as e:
                print(f"   ✗ Error processing {machine_dir.name}: {e}")
                import traceback
                traceback.print_exc()

        # Generate master docker-compose if we have machines
        if machines_generated:
            self._generate_master_compose(machines_generated)
            self._generate_readme(machines_generated)

        print(f"\n{'='*60}")
        print(f"✓ Generated {len(machines_generated)} application(s)")
        print(f"{'='*60}\n")

        return machines_generated

    def _generate_master_compose(self, machines: List[Dict]):
        """Generate master docker-compose.yml"""

        compose_content = "version: '3.8'\n\nservices:\n"

        for machine in machines:
            machine_dir = Path(machine['machine_dir'])
            machine_id = machine['machine_id']
            port = machine['port']

            # Read config to get flag location
            config_file = machine_dir / "config.json"
            with open(config_file, 'r') as f:
                config = json.load(f)

            # Get flag location from config, default to /var/www/html/flag.txt
            flag_location = config['flag'].get('location', '/var/www/html/flag.txt')
            
            # Clean up flag location
            flag_location = flag_location.replace(':', '_').replace('//', '/')
            if not flag_location.startswith('/'):
                flag_location = '/' + flag_location

            compose_content += f"""
  {machine_id}:
    build: ./{machine_dir.name}
    container_name: hackforge_{machine_id}
    ports:
      - "{port}:80"
    volumes:
      - ./{machine_dir.name}/app:/var/www/html
      - ./{machine_dir.name}/flag.txt:{flag_location}:ro
    environment:
      - MACHINE_ID={machine_id}
      - FLAG_LOCATION={flag_location}
    restart: unless-stopped
"""

        # Write compose file
        compose_file = self.machines_dir / "docker-compose.yml"
        compose_file.write_text(compose_content)
        print(f"\n✓ Generated: {compose_file}")

    def _generate_readme(self, machines: List[Dict]):
        """Generate README.md"""

        readme_content = f"""# Hackforge Generated Machines

Generated: {len(machines)} machine(s)

## Quick Start

```bash
# Build and start all machines
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop all machines
docker-compose down

# Rebuild specific machine
docker-compose up -d --build <machine_id>
```

## Machines

"""

        for i, machine in enumerate(machines, 1):
            machine_dir = Path(machine['machine_dir'])
            config_file = machine_dir / "config.json"

            with open(config_file, 'r') as f:
                config = json.load(f)

            readme_content += f"""### Machine {i} - http://localhost:{machine['port']}

- **Variant:** {config['variant']}
- **Difficulty:** {config['difficulty']}/5
- **Machine ID:** `{config['machine_id']}`
- **Container Name:** `hackforge_{config['machine_id']}`
- **Flag:** `{config['flag']['content']}`

**Hints:** See `{machine_dir.name}/HINTS.md`

---

"""

        readme_file = self.machines_dir / "README.md"
        readme_file.write_text(readme_content)
        print(f"✓ Generated: {readme_file}")


    def generate_campaign_apps(self, campaign_path: str, start_port: int = 8080) -> List[Dict]:
        """
        Generate apps for all machines in a campaign directory
        
        Args:
            campaign_path: Path to campaign directory (e.g., "forge/core/campaigns/campaign_123")
            start_port: Starting port number
            
        Returns:
            List of generated machine info with ports
        """
        campaign_dir = Path(campaign_path)
        
        if not campaign_dir.exists():
            print(f"✗ Campaign directory not found: {campaign_dir}")
            return []
        
        print(f"\n{'='*60}")
        print(f"Generating Apps for Campaign: {campaign_dir.name}")
        print(f"{'='*60}")
        
        machines_generated = []
        port = start_port
        
        # Find all machine directories with config.json
        machine_dirs = []
        for item in campaign_dir.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                config_file = item / "config.json"
                if config_file.exists():
                    machine_dirs.append(item)
        
        print(f"\nFound {len(machine_dirs)} machine(s) to process")
        
        for machine_dir in machine_dirs:
            config_file = machine_dir / "config.json"
            
            print(f"\nProcessing: {machine_dir.name}")
            
            try:
                # Load config
                with open(config_file, 'r') as f:
                    config_dict = json.load(f)
                
                # Convert dict to MachineConfig
                config = MachineConfig(**config_dict)
                
                # Generate application
                result = self.generate_machine_app(config, machine_dir)
                
                if result:
                    result['port'] = port
                    machines_generated.append(result)
                    port += 1
                    
            except Exception as e:
                print(f"   ✗ Error processing {machine_dir.name}: {e}")
                import traceback
                traceback.print_exc()
        
        # Generate docker-compose for this campaign
        if machines_generated:
            self._generate_campaign_compose(campaign_dir, machines_generated)
        
        print(f"\n{'='*60}")
        print(f"✓ Generated {len(machines_generated)} application(s)")
        print(f"{'='*60}\n")
        
        return machines_generated

    def _generate_campaign_compose(self, campaign_dir: Path, machines: List[Dict]):
        """Generate docker-compose.yml for a specific campaign"""
        
        compose_content = "version: '3.8'\n\nservices:\n"
        
        for machine in machines:
            machine_dir = Path(machine['machine_dir'])
            machine_id = machine['machine_id']
            port = machine['port']
            
            # Read config to get flag location
            config_file = machine_dir / "config.json"
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            flag_location = config['flag'].get('location', '/var/www/html/flag.txt')
            flag_location = flag_location.replace(':', '_').replace('//', '/')
            if not flag_location.startswith('/'):
                flag_location = '/' + flag_location
            
            # Relative path from campaign directory
            rel_path = machine_dir.relative_to(campaign_dir)
            
            compose_content += f"""
  {machine_id}:
    build: ./{rel_path}
    container_name: hackforge_{machine_id}
    ports:
      - "{port}:80"
    volumes:
      - ./{rel_path}/app:/var/www/html
      - ./{rel_path}/flag.txt:{flag_location}:ro
    environment:
      - MACHINE_ID={machine_id}
      - FLAG_LOCATION={flag_location}
    restart: unless-stopped
"""
        
        # Write compose file
        compose_file = campaign_dir / "docker-compose.yml"
        compose_file.write_text(compose_content)
        print(f"\n✓ Generated: {compose_file}")
def main():
    """Main entry point"""

    parser = argparse.ArgumentParser(description='Hackforge Template Engine')
    parser.add_argument(
        '--machines-dir',
        default='generated_machines',
        help='Directory containing machine configs (default: generated_machines)'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=8080,
        help='Starting port number (default: 8080)'
    )

    args = parser.parse_args()

    print("="*60)
    print("HACKFORGE - Template Engine")
    print("="*60)

    # Initialize template engine
    engine = TemplateEngine(machines_dir=args.machines_dir)

    # Check if machines exist
    if not engine.machines_dir.exists():
        print(f"\n✗ Machines directory not found: {engine.machines_dir}")
        print("   Run generator first: cd core && python3 generator.py")
        return

    # Check if there are any config files
    config_files = list(engine.machines_dir.glob("*/config.json"))
    
    if not config_files:
        print(f"\n✗ No machine configs found in {engine.machines_dir}")
        print("   Run generator first: cd core && python3 generator.py")
        return

    # Process all machines
    machines = engine.process_all_machines(start_port=args.port)

    if machines:
        print("\n" + "="*60)
        print("✓ SUCCESS! Docker applications generated")
        print("="*60)
        print("\nNext steps:")
        print(f"  1. cd {args.machines_dir}")
        print("  2. docker-compose up -d --build")
        print("  3. Access machines:")
        for i, machine in enumerate(machines, 1):
            print(f"     - Machine {i}: http://localhost:{machine['port']}")
        print("\n🎯 Try to exploit each machine and capture the flag!")
    else:
        print("\n✗ No machines generated")


if __name__ == "__main__":
    main()
