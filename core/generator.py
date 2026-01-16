#!/usr/bin/env python3
"""
Hackforge Dynamic Generator
Automatically discovers and loads all mutation engines and blueprints
"""

import os
import sys
import yaml
import json
import time
import importlib
from pathlib import Path
from typing import Dict, List, Optional

# Import base classes
from base import VulnerabilityBlueprint, MachineConfig, BlueprintLoader


class DynamicHackforgeGenerator:
    """
    Generator that automatically discovers mutations and blueprints
    No hardcoded imports needed!
    """

    def __init__(self, core_dir: str = None):
        import os

        if core_dir is None:
            # FIXED: Find core directory based on generator.py location
            # generator.py is in forge/core/generator.py
            generator_file = os.path.abspath(__file__)
            core_dir = os.path.dirname(generator_file)

        self.core_dir = Path(core_dir)
        self.blueprints_dir = self.core_dir / "blueprints"
        self.mutations_dir = self.core_dir / "mutations"

        print(f"\n{'='*60}")
        print(f"GENERATOR INITIALIZATION")
        print(f"{'='*60}")
        print(f"Core directory: {self.core_dir}")
        print(f"Blueprints directory: {self.blueprints_dir}")
        print(f"Mutations directory: {self.mutations_dir}")
        print(f"Blueprints exists: {self.blueprints_dir.exists()}")
        print(f"Mutations exists: {self.mutations_dir.exists()}")
        print(f"{'='*60}\n")

        self.blueprints: Dict[str, VulnerabilityBlueprint] = {}
        self.mutation_engines: Dict[str, type] = {}

        # Auto-discover everything
        self._discover_blueprints()
        self._discover_mutations()

        print(f"✓ Loaded {len(self.blueprints)} blueprints")
        print(f"✓ Loaded {len(self.mutation_engines)} mutation engines\n")

        # DIAGNOSTIC: Print what was loaded
        if self.blueprints:
            print("Blueprints loaded:")
            for bp_id, bp in self.blueprints.items():
                print(f"  - {bp_id}: {bp.name} (category: {bp.category})")
        else:
            print("⚠️  WARNING: No blueprints loaded!")

        if self.mutation_engines:
            print("\nMutation engines loaded:")
            for cat, eng in self.mutation_engines.items():
                print(f"  - {cat}: {eng.__name__}")
        else:
            print("⚠️  WARNING: No mutation engines loaded!")
        print()

    def _discover_blueprints(self):
        """Automatically discover all blueprint YAML files"""

        if not self.blueprints_dir.exists():
            print(f"⚠️  Blueprints directory not found: {self.blueprints_dir}")
            return

        for yaml_file in self.blueprints_dir.glob("*_blueprint.yaml"):
            try:
                with open(yaml_file, 'r') as f:
                    data = yaml.safe_load(f)

                blueprint = BlueprintLoader.load_from_dict(data)

                if BlueprintLoader.validate_blueprint(blueprint):
                    self.blueprints[blueprint.blueprint_id] = blueprint
                    print(f"  ✓ Loaded blueprint: {blueprint.name} (category: {blueprint.category})")

            except Exception as e:
                print(f"  ✗ Error loading {yaml_file.name}: {e}")

    def _discover_mutations(self):
        """Automatically discover all mutation engine Python files"""

        if not self.mutations_dir.exists():
            print(f"⚠️  Mutations directory not found: {self.mutations_dir}")
            return

        # Add mutations directory to Python path
        sys.path.insert(0, str(self.mutations_dir.parent))

        for py_file in self.mutations_dir.glob("*_mutation.py"):
            try:
                # Import the module dynamically
                module_name = f"mutations.{py_file.stem}"
                module = importlib.import_module(module_name)

                # Find the mutation class (should end with "Mutation")
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)

                    # Check if it's a class and ends with "Mutation"
                    if (isinstance(attr, type) and
                        attr_name.endswith("Mutation") and
                        attr_name != "MutationEngine"):

                        # FIXED: Extract category from filename instead of class name
                        # Filename: cross_site_scripting_mutation.py -> cross_site_scripting
                        category = py_file.stem.replace('_mutation', '')

                        self.mutation_engines[category] = attr
                        print(f"  ✓ Loaded mutation: {attr_name} (category: {category})")
                        break

            except Exception as e:
                print(f"  ✗ Error loading {py_file.name}: {e}")
                import traceback
                traceback.print_exc()

    def _camel_to_snake(self, name: str) -> str:
        """Convert CamelCase to snake_case"""
        import re
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

    def list_all_blueprints(self) -> List[Dict]:
        """List all available blueprints"""
        result = []

        for bp in self.blueprints.values():
            result.append({
                'blueprint_id': bp.blueprint_id,
                'name': bp.name,
                'category': bp.category,
                'difficulty_range': bp.difficulty_range,
                'variants': bp.variants,
                'description': bp.description,
            })

        return result

    def get_blueprint(self, blueprint_id: str) -> Optional[VulnerabilityBlueprint]:
        """Get specific blueprint by ID"""
        return self.blueprints.get(blueprint_id)

    def generate_machine(self, blueprint_id: str, seed: str, difficulty: int) -> Optional[MachineConfig]:
        """Generate a machine from blueprint"""

        blueprint = self.blueprints.get(blueprint_id)
        if not blueprint:
            print(f"✗ Blueprint not found: {blueprint_id}")
            return None

        # Get mutation engine for this category
        engine_class = self.mutation_engines.get(blueprint.category)
        if not engine_class:
            print(f"✗ No mutation engine for category: {blueprint.category}")
            print(f"  Available engines: {list(self.mutation_engines.keys())}")
            print(f"  Blueprint category: '{blueprint.category}'")
            return None

        # Generate machine
        try:
            engine = engine_class(seed)
            config = engine.mutate(blueprint, difficulty)
            return config
        except Exception as e:
            print(f"✗ Error generating machine: {e}")
            import traceback
            traceback.print_exc()
            return None

    def generate_single_machine(self, blueprint_id: str = None, difficulty: int = 2, 
                                user_id: str = "user") -> Optional[MachineConfig]:
        """Generate a single machine and export to generated_machines directory"""
        
        # If no blueprint specified, pick a random one
        if blueprint_id is None:
            if not self.blueprints:
                print("✗ No blueprints available!")
                return None
            import random
            blueprint_id = random.choice(list(self.blueprints.keys()))
        
        blueprint = self.blueprints.get(blueprint_id)
        if not blueprint:
            print(f"✗ Blueprint not found: {blueprint_id}")
            print(f"Available blueprints: {list(self.blueprints.keys())}")
            return None

        timestamp = int(time.time())
        seed = f"{user_id}_{blueprint_id}_{timestamp}"

        print(f"\n{'='*60}")
        print(f"Generating Single Machine")
        print(f"{'='*60}")
        print(f"Blueprint: {blueprint.name}")
        print(f"Category: {blueprint.category}")
        print(f"Difficulty: {difficulty}/5")
        print(f"User ID: {user_id}")
        print()

        machine = self.generate_machine(blueprint_id, seed, difficulty)

        if machine:
            print(f"✓ Machine ID: {machine.machine_id}")
            print(f"✓ Variant: {machine.variant}")
            print(f"✓ Flag: {machine.flag['content'][:30]}...")
            
            # Export to generated_machines directory
            output_path = self.export_single_machine(machine)
            
            print(f"\n{'='*60}")
            print(f"✓ Machine exported to: {output_path}")
            print(f"{'='*60}\n")
            
            return machine
        else:
            print("✗ Failed to generate machine")
            return None

    def export_single_machine(self, machine: MachineConfig) -> str:
        """Export a single machine to generated_machines directory"""
        
        # Create generated_machines directory structure
        output_dir = self.core_dir / "generated_machines" / machine.machine_id
        output_dir.mkdir(parents=True, exist_ok=True)

        print(f"\nExporting to: {output_dir}")
        print("-"*60)

        # Export config
        config_file = output_dir / "config.json"
        with open(config_file, 'w') as f:
            json.dump(machine.to_dict(), f, indent=2)
        print(f"✓ Config: {config_file}")

        # Export flag
        flag_file = output_dir / "flag.txt"
        with open(flag_file, 'w') as f:
            f.write(machine.flag['content'])
        print(f"✓ Flag: {flag_file}")

        # Export hints
        hints_file = output_dir / "hints.txt"
        with open(hints_file, 'w') as f:
            hints = machine.metadata.get('exploit_hints', [])
            f.write(f"Machine: {machine.machine_id}\n")
            f.write(f"Name: {machine.metadata.get('vuln_name', 'Unknown')}\n")
            f.write(f"Variant: {machine.variant}\n")
            f.write(f"Difficulty: {machine.difficulty}/5\n\n")
            f.write("Hints:\n")
            for hint in hints:
                f.write(f"  • {hint}\n")
        print(f"✓ Hints: {hints_file}")

        # Export README
        readme_file = output_dir / "README.md"
        with open(readme_file, 'w') as f:
            f.write(f"# {machine.metadata.get('vuln_name', 'Unknown')}\n\n")
            f.write(f"**Machine ID:** `{machine.machine_id}`\n")
            f.write(f"**Variant:** {machine.variant}\n")
            f.write(f"**Difficulty:** {machine.difficulty}/5\n")
            f.write(f"**Category:** {machine.metadata.get('category', 'Unknown')}\n\n")
            f.write(f"## Description\n\n")
            f.write(f"{machine.metadata.get('description', 'No description available')}\n\n")
            f.write(f"## Flag\n\n")
            f.write(f"Flag location: `flag.txt`\n\n")
            f.write(f"## Next Steps\n\n")
            f.write(f"1. Generate vulnerable app with template_engine.py\n")
            f.write(f"2. Deploy with Docker\n")
        print(f"✓ README: {readme_file}")

        return str(output_dir)

    def generate_campaign(self, user_id: str, difficulty: int = 2, count: int = None) -> List[MachineConfig]:
        """Generate a campaign with multiple machines"""

        if not self.blueprints:
            print("✗ No blueprints available!")
            return []

        if count is None:
            count = min(len(self.blueprints), 5)

        machines = []
        timestamp = int(time.time())

        print(f"\n{'='*60}")
        print(f"Generating Campaign")
        print(f"{'='*60}")
        print(f"User ID: {user_id}")
        print(f"Difficulty: {difficulty}/5")
        print(f"Machines: {count}")
        print()

        # Select random blueprints
        import random
        selected_ids = random.sample(list(self.blueprints.keys()),
                                     min(count, len(self.blueprints)))

        for i, blueprint_id in enumerate(selected_ids, 1):
            seed = f"{user_id}_{blueprint_id}_{timestamp}_{i}"

            blueprint = self.blueprints[blueprint_id]
            print(f"[{i}/{count}] Generating: {blueprint.name}")

            machine = self.generate_machine(blueprint_id, seed, difficulty)

            if machine:
                machines.append(machine)
                print(f"  ✓ Machine ID: {machine.machine_id}")
                print(f"  ✓ Variant: {machine.variant}")
                print(f"  ✓ Flag: {machine.flag['content'][:30]}...")
            else:
                print(f"  ✗ Failed to generate")

            print()

        print(f"{'='*60}")
        print(f"✓ Generated {len(machines)}/{count} machines")
        print(f"{'='*60}\n")

        return machines

    def export_campaign(self, machines: List[MachineConfig], output_dir: str = None) -> str:
        """Export campaign to directory"""

        if not machines:
            print("✗ No machines to export!")
            return None

        # FIXED: Create campaign-specific directory
        if output_dir is None:
            campaign_id = f"campaign_{int(time.time())}"
            output_dir = f"campaigns/{campaign_id}"

        output_path = self.core_dir / output_dir
        output_path.mkdir(parents=True, exist_ok=True)

        print(f"\nExporting to: {output_path}")
        print("="*60)

        # Export each machine
        for machine in machines:
            machine_dir = output_path / machine.machine_id
            machine_dir.mkdir(parents=True, exist_ok=True)

            # Export config
            config_file = machine_dir / "config.json"
            with open(config_file, 'w') as f:
                json.dump(machine.to_dict(), f, indent=2)

            # Export flag
            flag_file = machine_dir / "flag.txt"
            with open(flag_file, 'w') as f:
                f.write(machine.flag['content'])

            # Export hints
            hints_file = machine_dir / "hints.txt"
            with open(hints_file, 'w') as f:
                hints = machine.metadata.get('exploit_hints', [])
                f.write(f"Machine: {machine.machine_id}\n")
                f.write(f"Variant: {machine.variant}\n")
                f.write(f"Difficulty: {machine.difficulty}/5\n\n")
                f.write("Hints:\n")
                for hint in hints:
                    f.write(f"  • {hint}\n")

            print(f"  ✓ {machine.machine_id}")

        # Export manifest with campaign_id
        campaign_id = output_path.name  # Get campaign_id from directory name
        manifest = {
            'campaign_id': campaign_id,
            'created_at': time.strftime('%Y-%m-%d %H:%M:%S'),
            'machines': [m.to_dict() for m in machines],
            'total': len(machines),
        }

        manifest_file = output_path / "manifest.json"
        with open(manifest_file, 'w') as f:
            json.dump(manifest, f, indent=2)

        print(f"\n✓ Manifest: {manifest_file}")
        print(f"✓ Exported {len(machines)} machines")

        return str(output_path)


def main():
    """Main entry point"""

    print("\n" + "="*60)
    print("HACKFORGE DYNAMIC GENERATOR")
    print("="*60 + "\n")

    # Initialize generator
    generator = DynamicHackforgeGenerator()

    if not generator.blueprints:
        print("\n✗ No blueprints found!")
        print("  Make sure you have .yaml files in blueprints/")
        print("  Generate them with: python3 vuln_generator.py <config.json>")
        return

    if not generator.mutation_engines:
        print("\n✗ No mutation engines found!")
        print("  Make sure you have *_mutation.py files in mutations/")
        print("  Generate them with: python3 vuln_generator.py <config.json>")
        return

    # List available vulnerabilities
    print("\nAvailable Vulnerabilities:")
    print("-"*60)
    for i, bp in enumerate(generator.list_all_blueprints(), 1):
        print(f"{i}. {bp['name']} ({bp['category']})")
        print(f"   Variants: {', '.join(bp['variants'])}")
        print()

    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description='Hackforge Machine Generator')
    parser.add_argument('--mode', choices=['single', 'campaign', 'all'], default='all',
                       help='Generation mode: single machine, campaign, or all blueprints')
    parser.add_argument('--blueprint', type=str, help='Blueprint ID for single machine')
    parser.add_argument('--difficulty', type=int, default=2, choices=[1,2,3,4,5],
                       help='Difficulty level (1-5)')
    parser.add_argument('--count', type=int, default=3,
                       help='Number of machines for campaign')
    parser.add_argument('--user', type=str, default='demo_user',
                       help='User ID for generation')

    args = parser.parse_args()

    if args.mode == 'single':
        # Generate single machine
        machine = generator.generate_single_machine(
            blueprint_id=args.blueprint,
            difficulty=args.difficulty,
            user_id=args.user
        )

        if machine:
            print("\n" + "="*60)
            print("NEXT STEPS")
            print("="*60)
            print(f"\n1. Machine exported to: generated_machines/{machine.machine_id}")
            print(f"2. Generate vulnerable app:")
            print(f"   python3 template_engine.py")
            print(f"\n3. Start Docker container:")
            print(f"   cd generated_machines/{machine.machine_id} && docker-compose up -d")
            print()

    elif args.mode == 'all':
        # NEW: Generate one machine for EACH blueprint
        print("\n" + "="*60)
        print("GENERATING ALL MACHINES")
        print("="*60)
        print(f"Total blueprints: {len(generator.blueprints)}")
        print(f"Difficulty: {args.difficulty}/5")
        print(f"User ID: {args.user}\n")

        generated_machines = []
        timestamp = int(time.time())

        for i, (blueprint_id, blueprint) in enumerate(generator.blueprints.items(), 1):
            print(f"\n[{i}/{len(generator.blueprints)}] Generating: {blueprint.name}")
            print("-"*60)

            # Generate unique seed for this blueprint
            seed = f"{args.user}_{blueprint_id}_{timestamp}_{i}"

            machine = generator.generate_machine(blueprint_id, seed, args.difficulty)

            if machine:
                # Export this machine
                output_path = generator.export_single_machine(machine)
                generated_machines.append(machine)
                
                print(f"✓ Machine ID: {machine.machine_id}")
                print(f"✓ Variant: {machine.variant}")
                print(f"✓ Flag: {machine.flag['content'][:30]}...")
                print(f"✓ Exported to: {output_path}")
            else:
                print(f"✗ Failed to generate machine for {blueprint.name}")

        # Summary
        print("\n" + "="*60)
        print("GENERATION COMPLETE")
        print("="*60)
        print(f"✓ Generated {len(generated_machines)}/{len(generator.blueprints)} machines\n")

        if generated_machines:
            print("Generated Machines:")
            for m in generated_machines:
                print(f"  • {m.machine_id} - {m.metadata.get('vuln_name', 'Unknown')} ({m.variant})")

            print("\n" + "="*60)
            print("NEXT STEPS")
            print("="*60)
            print(f"\n1. All machines exported to: generated_machines/")
            print(f"2. Generate vulnerable apps:")
            print(f"   python3 template_engine.py")
            print(f"\n3. Start all Docker containers:")
            print(f"   cd generated_machines && for dir in */; do (cd \"$dir\" && docker-compose up -d); done")
            print()

    else:
        # Generate campaign
        machines = generator.generate_campaign(
            user_id=args.user,
            difficulty=args.difficulty,
            count=args.count
        )

        if machines:
            # Export campaign
            output_path = generator.export_campaign(machines)

            print("\n" + "="*60)
            print("NEXT STEPS")
            print("="*60)
            print(f"\n1. Machines exported to: {output_path}")
            print(f"2. Generate vulnerable apps:")
            print(f"   python3 template_engine.py")
            print(f"\n3. Start Docker containers:")
            print(f"   cd {output_path} && docker-compose up -d")
            print()


if __name__ == "__main__":
    main()
