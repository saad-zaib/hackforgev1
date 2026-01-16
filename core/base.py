"""
Hackforge Base Classes
Core abstractions for blueprints and mutation engines
"""

from abc import ABC, abstractmethod
import random
import hashlib
from typing import Dict, List, Any
from dataclasses import dataclass, field


@dataclass
class VulnerabilityBlueprint:
    """
    Immutable blueprint defining a vulnerability class
    """
    blueprint_id: str
    name: str
    category: str
    difficulty_range: tuple
    variants: List[str]
    entry_points: List[str]
    mutation_axes: Dict[str, List[Any]]
    description: str = ""
    
    def to_dict(self) -> Dict:
        return {
            'blueprint_id': self.blueprint_id,
            'name': self.name,
            'category': self.category,
            'difficulty_range': self.difficulty_range,
            'variants': self.variants,
            'entry_points': self.entry_points,
            'mutation_axes': self.mutation_axes,
            'description': self.description
        }


@dataclass
class MachineConfig:
    """
    Complete configuration for a generated vulnerable machine
    """
    machine_id: str
    blueprint_id: str
    variant: str
    difficulty: int
    seed: str
    
    # Application details
    application: Dict[str, Any]
    
    # Constraints and filters
    constraints: Dict[str, Any]
    
    # Flag information
    flag: Dict[str, str]
    
    # Runtime behavior
    behavior: Dict[str, Any]
    
    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            'machine_id': self.machine_id,
            'blueprint_id': self.blueprint_id,
            'variant': self.variant,
            'difficulty': self.difficulty,
            'seed': self.seed,
            'application': self.application,
            'constraints': self.constraints,
            'flag': self.flag,
            'behavior': self.behavior,
            'metadata': self.metadata
        }


class MutationEngine(ABC):
    """
    Abstract base class for vulnerability mutation engines
    Each vulnerability type implements its own mutation logic
    """
    
    def __init__(self, seed: str):
        self.seed = seed
        self.rng = random.Random(seed)
    
    @abstractmethod
    def mutate(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> MachineConfig:
        """
        Generate a unique machine configuration from a blueprint
        
        Args:
            blueprint: The vulnerability blueprint to mutate
            difficulty: Difficulty level (1-5)
            
        Returns:
            MachineConfig object with complete machine specification
        """
        pass
    
    def generate_machine_id(self) -> str:
        """Generate unique machine ID from seed"""
        return hashlib.sha256(self.seed.encode()).hexdigest()[:16]
    
    def generate_flag(self, prefix: str = "HACKFORGE") -> str:
        """Generate unique flag content"""
        hash_val = hashlib.sha256(f"{self.seed}_flag".encode()).hexdigest()
        return f"{prefix}{{{hash_val[:32]}}}"
    
    def select_random(self, items: List[Any]) -> Any:
        """Select random item from list using seeded RNG"""
        return self.rng.choice(items)
    
    def select_multiple(self, items: List[Any], count: int) -> List[Any]:
        """Select multiple random items"""
        return self.rng.sample(items, min(count, len(items)))
    
    def generate_random_string(self, length: int = 16) -> str:
        """Generate random alphanumeric string"""
        chars = "abcdefghijklmnopqrstuvwxyz0123456789"
        return ''.join(self.rng.choice(chars) for _ in range(length))


class BlueprintLoader:
    """
    Loads and validates vulnerability blueprints from YAML files
    """
    
    @staticmethod
    def load_from_dict(data: Dict) -> VulnerabilityBlueprint:
        """Create blueprint from dictionary"""
        return VulnerabilityBlueprint(
            blueprint_id=data['blueprint_id'],
            name=data['name'],
            category=data['category'],
            difficulty_range=tuple(data['difficulty_range']),
            variants=data['variants'],
            entry_points=data['entry_points'],
            mutation_axes=data['mutation_axes'],
            description=data.get('description', '')
        )
    
    @staticmethod
    def validate_blueprint(blueprint: VulnerabilityBlueprint) -> bool:
        """Validate blueprint has all required fields"""
        required_fields = ['blueprint_id', 'name', 'category', 'variants', 'entry_points', 'mutation_axes']
        
        for field in required_fields:
            if not getattr(blueprint, field):
                return False
        
        if not blueprint.variants:
            return False
            
        if not blueprint.mutation_axes:
            return False
        
        return True
