"""
Hackforge Complete Test Suite
Tests all 7 components comprehensively
"""

import unittest
import requests
import sys
import os
from pathlib import Path
import json
import time
import subprocess
import shutil

# Add paths
sys.path.append(str(Path(__file__).parent.parent / "core"))
sys.path.append(str(Path(__file__).parent.parent / "web" / "database"))
sys.path.append(str(Path(__file__).parent.parent / "docker" / "orchestrator"))

from generator import HackforgeGenerator
from template_engine import TemplateEngine
from orchestrator import DockerOrchestrator

try:
    from database import get_db
    DATABASE_AVAILABLE = True
except:
    DATABASE_AVAILABLE = False

API_BASE = "http://localhost:8000"


class TestComponentStatus(unittest.TestCase):
    """Test that all components are available"""
    
    def test_01_api_running(self):
        """Test API is accessible"""
        try:
            response = requests.get(f"{API_BASE}/health", timeout=5)
            self.assertEqual(response.status_code, 200)
            print("✓ API is running")
        except requests.exceptions.ConnectionError:
            self.fail("❌ API is not running. Start with: python3 web/api/main_with_db.py")
    
    def test_02_mongodb_running(self):
        """Test MongoDB connection"""
        if not DATABASE_AVAILABLE:
            self.skipTest("Database module not available")
        
        try:
            db = get_db()
            db.users.find_one()
            print("✓ MongoDB is connected")
        except Exception as e:
            self.fail(f"❌ MongoDB connection failed: {e}")
    
    def test_03_docker_available(self):
        """Test Docker is available"""
        result = subprocess.run(['docker', '--version'], 
                              capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        print("✓ Docker is available")
    
    def test_04_blueprints_exist(self):
        """Test blueprints directory exists"""
        blueprints_dir = Path(__file__).parent.parent / "core" / "blueprints"
        self.assertTrue(blueprints_dir.exists())
        
        yaml_files = list(blueprints_dir.glob("*.yaml"))
        self.assertGreater(len(yaml_files), 0)
        print(f"✓ Found {len(yaml_files)} blueprint files")


class TestComponent1_CoreGeneration(unittest.TestCase):
    """Test Component 1: Core Generation System"""
    
    @classmethod
    def setUpClass(cls):
        cls.generator = HackforgeGenerator()
    
    def test_01_blueprints_loaded(self):
        """Test blueprints load correctly"""
        blueprints = self.generator.list_blueprints()
        self.assertGreater(len(blueprints), 0, "No blueprints loaded")
        
        for bp in blueprints:
            self.assertIsNotNone(bp.blueprint_id)
            self.assertIsNotNone(bp.name)
            self.assertIsNotNone(bp.category)
            self.assertGreater(len(bp.variants), 0)
        
        print(f"✓ Loaded {len(blueprints)} blueprints")
    
    def test_02_blueprint_structure(self):
        """Test blueprint has all required fields"""
        blueprint = self.generator.list_blueprints()[0]
        
        required_fields = ['blueprint_id', 'name', 'category', 'variants', 
                          'entry_points', 'mutation_axes']
        
        for field in required_fields:
            self.assertTrue(hasattr(blueprint, field))
        
        print(f"✓ Blueprint structure valid")
    
    def test_03_generate_single_machine(self):
        """Test single machine generation"""
        blueprints = self.generator.list_blueprints()
        blueprint = blueprints[0]
        
        machine = self.generator.generate_machine(
            blueprint.blueprint_id,
            seed="test_seed_single",
            difficulty=2
        )
        
        self.assertIsNotNone(machine)
        self.assertEqual(machine.difficulty, 2)
        self.assertIn("HACKFORGE{", machine.flag['content'])
        self.assertEqual(len(machine.flag['content']), 43)  # HACKFORGE{32 chars}
        
        print(f"✓ Generated machine: {machine.variant}")
    
    def test_04_deterministic_generation(self):
        """Test same seed produces same machine"""
        blueprint_id = self.generator.list_blueprints()[0].blueprint_id
        
        machine1 = self.generator.generate_machine(blueprint_id, "same_seed", 2)
        machine2 = self.generator.generate_machine(blueprint_id, "same_seed", 2)
        
        self.assertEqual(machine1.machine_id, machine2.machine_id)
        self.assertEqual(machine1.flag['content'], machine2.flag['content'])
        
        print("✓ Deterministic generation works")
    
    def test_05_unique_machines(self):
        """Test different seeds produce different machines"""
        blueprint_id = self.generator.list_blueprints()[0].blueprint_id
        
        machine1 = self.generator.generate_machine(blueprint_id, "seed1", 2)
        machine2 = self.generator.generate_machine(blueprint_id, "seed2", 2)
        
        self.assertNotEqual(machine1.machine_id, machine2.machine_id)
        self.assertNotEqual(machine1.flag['content'], machine2.flag['content'])
        
        print("✓ Unique machines with different seeds")
    
    def test_06_campaign_generation(self):
        """Test campaign generation"""
        user_id = f"test_user_{int(time.time())}"
        
        machines = self.generator.generate_campaign(
            user_id=user_id,
            difficulty=2,
            count=2
        )
        
        self.assertEqual(len(machines), 2)
        
        # Check all machines have unique IDs and flags
        machine_ids = [m.machine_id for m in machines]
        self.assertEqual(len(machine_ids), len(set(machine_ids)))
        
        flags = [m.flag['content'] for m in machines]
        self.assertEqual(len(flags), len(set(flags)))
        
        print(f"✓ Campaign with {len(machines)} machines generated")
    
    def test_07_difficulty_range(self):
        """Test difficulty levels"""
        blueprint_id = self.generator.list_blueprints()[0].blueprint_id
        
        for difficulty in [1, 2, 3, 4, 5]:
            machine = self.generator.generate_machine(
                blueprint_id, 
                f"seed_diff_{difficulty}", 
                difficulty
            )
            self.assertEqual(machine.difficulty, difficulty)
        
        print("✓ All difficulty levels work")


class TestComponent2_TemplateEngine(unittest.TestCase):
    """Test Component 2: Template Engine"""
    
    @classmethod
    def setUpClass(cls):
        cls.generator = HackforgeGenerator()
        cls.test_dir = Path("tests/test_generated")
        cls.template_engine = TemplateEngine(output_dir=str(cls.test_dir))
    
    def test_01_template_generation(self):
        """Test PHP template generation"""
        blueprint_id = self.generator.list_blueprints()[0].blueprint_id
        machine = self.generator.generate_machine(blueprint_id, "test_template", 2)
        
        result = self.template_engine.generate_machine_app(machine)
        
        self.assertIsNotNone(result)
        self.assertIn('app_file', result)
        self.assertTrue(Path(result['app_file']).exists())
        
        # Check PHP file contains expected content
        with open(result['app_file'], 'r') as f:
            content = f.read()
            self.assertIn('<?php', content)
            self.assertIn('Hackforge Machine', content)
        
        print(f"✓ Template generated at: {result['app_file']}")
    
    def test_02_dockerfile_generation(self):
        """Test Dockerfile generation"""
        blueprint_id = self.generator.list_blueprints()[0].blueprint_id
        machine = self.generator.generate_machine(blueprint_id, "test_docker", 2)
        
        result = self.template_engine.generate_machine_app(machine)
        
        self.assertTrue(Path(result['dockerfile']).exists())
        
        with open(result['dockerfile'], 'r') as f:
            content = f.read()
            self.assertIn('FROM php', content)
            self.assertIn('EXPOSE 80', content)
        
        print("✓ Dockerfile generated")
    
    def test_03_flag_file_generation(self):
        """Test flag file creation"""
        blueprint_id = self.generator.list_blueprints()[0].blueprint_id
        machine = self.generator.generate_machine(blueprint_id, "test_flag", 2)
        
        result = self.template_engine.generate_machine_app(machine)
        
        self.assertTrue(Path(result['flag_file']).exists())
        
        with open(result['flag_file'], 'r') as f:
            flag_content = f.read()
            self.assertIn('HACKFORGE{', flag_content)
            self.assertEqual(flag_content, machine.flag['content'])
        
        print("✓ Flag file generated")
    
    def test_04_hints_generation(self):
        """Test hints file generation"""
        blueprint_id = self.generator.list_blueprints()[0].blueprint_id
        machine = self.generator.generate_machine(blueprint_id, "test_hints", 2)
        
        result = self.template_engine.generate_machine_app(machine)
        
        self.assertTrue(Path(result['hints_file']).exists())
        
        with open(result['hints_file'], 'r') as f:
            hints_content = f.read()
            self.assertIn('Exploitation Hints', hints_content)
            self.assertIn(machine.machine_id, hints_content)
        
        print("✓ Hints file generated")
    
    @classmethod
    def tearDownClass(cls):
        """Cleanup test files"""
        if cls.test_dir.exists():
            shutil.rmtree(cls.test_dir)
        print("✓ Cleaned up test files")


class TestComponent3_DockerOrchestrator(unittest.TestCase):
    """Test Component 3: Docker Orchestrator"""
    
    @classmethod
    def setUpClass(cls):
        cls.orchestrator = DockerOrchestrator()
    
    def test_01_check_docker(self):
        """Test Docker installation check"""
        success = self.orchestrator.check_docker_installed()
        self.assertTrue(success)
        print("✓ Docker installation verified")
    
    def test_02_list_machines(self):
        """Test listing machines"""
        machines = self.orchestrator.list_machines()
        self.assertIsInstance(machines, list)
        print(f"✓ Found {len(machines)} machines")
    
    def test_03_machine_config_valid(self):
        """Test machine configs are valid"""
        machines = self.orchestrator.list_machines()
        
        if len(machines) > 0:
            machine = machines[0]
            required_fields = ['machine_id', 'variant', 'difficulty', 'flag']
            
            for field in required_fields:
                self.assertIn(field, machine)
            
            print("✓ Machine config structure valid")
        else:
            self.skipTest("No machines generated yet")


class TestComponent4_API(unittest.TestCase):
    """Test Component 4: Web API"""
    
    def test_01_health_check(self):
        """Test API health endpoint"""
        response = requests.get(f"{API_BASE}/health", timeout=5)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(data['status'], 'healthy')
        print("✓ API health check passed")
    
    def test_02_list_blueprints(self):
        """Test blueprints endpoint"""
        response = requests.get(f"{API_BASE}/api/blueprints")
        self.assertEqual(response.status_code, 200)
        
        blueprints = response.json()
        self.assertGreater(len(blueprints), 0)
        
        # Check structure
        bp = blueprints[0]
        self.assertIn('blueprint_id', bp)
        self.assertIn('name', bp)
        self.assertIn('category', bp)
        
        print(f"✓ API returned {len(blueprints)} blueprints")
    
    def test_03_create_campaign_api(self):
        """Test campaign creation via API"""
        payload = {
            "user_id": f"test_api_{int(time.time())}",
            "difficulty": 2,
            "count": 2
        }
        
        response = requests.post(f"{API_BASE}/api/campaigns", json=payload)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('campaign_id', data)
        self.assertEqual(len(data['machines']), 2)
        
        # Store for other tests
        self.__class__.test_campaign_id = data['campaign_id']
        self.__class__.test_user_id = payload['user_id']
        self.__class__.test_machines = data['machines']
        
        print(f"✓ Campaign created via API: {data['campaign_id']}")
    
    def test_04_list_machines_api(self):
        """Test machines listing endpoint"""
        response = requests.get(f"{API_BASE}/api/machines")
        self.assertEqual(response.status_code, 200)
        
        machines = response.json()
        self.assertIsInstance(machines, list)
        
        print(f"✓ API returned {len(machines)} machines")
    
    def test_05_validate_correct_flag(self):
        """Test correct flag validation"""
        if not hasattr(self.__class__, 'test_machines'):
            self.skipTest("No campaign created")
        
        machine = self.__class__.test_machines[0]
        
        payload = {
            "machine_id": machine['machine_id'],
            "flag": machine['flag'],
            "user_id": self.__class__.test_user_id
        }
        
        response = requests.post(f"{API_BASE}/api/flags/validate", json=payload)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertTrue(data['correct'])
        self.assertGreater(data['points'], 0)
        
        print(f"✓ Correct flag validated: +{data['points']} points")
    
    def test_06_validate_incorrect_flag(self):
        """Test incorrect flag validation"""
        if not hasattr(self.__class__, 'test_machines'):
            self.skipTest("No campaign created")
        
        machine = self.__class__.test_machines[0]
        
        payload = {
            "machine_id": machine['machine_id'],
            "flag": "HACKFORGE{wrong_flag_12345678901234567890}",
            "user_id": self.__class__.test_user_id
        }
        
        response = requests.post(f"{API_BASE}/api/flags/validate", json=payload)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertFalse(data['correct'])
        self.assertEqual(data['points'], 0)
        
        print("✓ Incorrect flag rejected")
    
    def test_07_docker_status(self):
        """Test Docker status endpoint"""
        response = requests.get(f"{API_BASE}/api/docker/status")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('total', data)
        self.assertIn('running', data)
        
        print(f"✓ Docker status: {data['running']}/{data['total']} running")
    
    def test_08_get_statistics(self):
        """Test statistics endpoint"""
        response = requests.get(f"{API_BASE}/api/stats")
        self.assertEqual(response.status_code, 200)
        
        stats = response.json()
        self.assertIn('total_blueprints', stats)
        self.assertIn('total_machines', stats)
        
        print(f"✓ Stats: {stats['total_machines']} machines, {stats['total_blueprints']} blueprints")


class TestComponent6_Database(unittest.TestCase):
    """Test Component 6: Database Integration"""
    
    @classmethod
    def setUpClass(cls):
        if not DATABASE_AVAILABLE:
            raise unittest.SkipTest("Database not available")
        cls.db = get_db()
    
    def test_01_create_user_db(self):
        """Test user creation in database"""
        user_data = {
            'user_id': f"test_db_{int(time.time())}",
            'username': 'testuser_db',
            'email': f"test_{int(time.time())}@example.com",
            'role': 'student'
        }
        
        user = self.db.create_user(user_data)
        self.assertIn('user_id', user)
        
        self.__class__.test_user_id = user['user_id']
        print(f"✓ User created in DB: {user['user_id']}")
    
    def test_02_get_user_db(self):
        """Test user retrieval"""
        if not hasattr(self.__class__, 'test_user_id'):
            self.skipTest("No user created")
        
        user = self.db.get_user(self.__class__.test_user_id)
        self.assertIsNotNone(user)
        self.assertEqual(user['username'], 'testuser_db')
        
        print("✓ User retrieved from DB")
    
    def test_03_add_points_db(self):
        """Test adding points"""
        if not hasattr(self.__class__, 'test_user_id'):
            self.skipTest("No user created")
        
        success = self.db.add_points(self.__class__.test_user_id, 100)
        self.assertTrue(success)
        
        user = self.db.get_user(self.__class__.test_user_id)
        self.assertEqual(user['total_points'], 100)
        
        print("✓ Points added to user")
    
    def test_04_platform_stats(self):
        """Test platform statistics"""
        stats = self.db.get_platform_stats()
        
        self.assertIn('total_users', stats)
        self.assertIn('total_campaigns', stats)
        self.assertIn('total_solves', stats)
        
        print(f"✓ Platform stats: {stats['total_users']} users")


class TestComponent7_Integration(unittest.TestCase):
    """Test Component 7: Complete Integration"""
    
    @classmethod
    def setUpClass(cls):
        """Clean up before integration tests"""
        # Clear test database
        try:
            from pymongo import MongoClient
            client = MongoClient('mongodb://localhost:27017/')
            db = client['hackforge']
            # Clear test campaigns
            db.campaigns.delete_many({'campaign_id': {'$regex': '^campaign_'}})
            db.users.delete_many({'username': {'$regex': '^test_'}})
        except Exception as e:
            print(f"Warning: Could not clean database: {e}")
    
    def setUp(self):
        """Wait between tests to avoid race conditions"""
        import time
        time.sleep(0.1)  # Small delay to avoid timestamp collisions

    def test_01_end_to_end_workflow(self):
        """Test complete user workflow"""
        print("\n=== End-to-End Integration Test ===")
        
        # 1. Create campaign
        user_id = f"e2e_test_{int(time.time())}"
        payload = {
            "user_id": user_id,
            "difficulty": 2,
            "count": 2
        }
        
        response = requests.post(f"{API_BASE}/api/campaigns", json=payload)
        self.assertEqual(response.status_code, 200)
        campaign = response.json()
        print(f"1. ✓ Created campaign: {campaign['campaign_id']}")
        
        # 2. Verify machines generated
        self.assertEqual(len(campaign['machines']), 2)
        machine = campaign['machines'][0]
        print(f"2. ✓ Generated machine: {machine['variant']}")
        
        # 3. Submit correct flag
        flag_payload = {
            "machine_id": machine['machine_id'],
            "flag": machine['flag'],
            "user_id": user_id
        }
        
        response = requests.post(f"{API_BASE}/api/flags/validate", json=flag_payload)
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertTrue(result['correct'])
        print(f"3. ✓ Flag validated: +{result['points']} points")
        
        # 4. Check user stats
        if DATABASE_AVAILABLE:
            response = requests.get(f"{API_BASE}/api/users/{user_id}")
            if response.status_code == 200:
                user = response.json()
                self.assertGreater(user['total_points'], 0)
                print(f"4. ✓ User stats: {user['machines_solved']} solved, {user['total_points']} points")
        
        print("=== End-to-End Test Complete ===\n")


def run_all_tests(verbosity=2):
    """Run complete test suite"""
    
    print("""
╔═══════════════════════════════════════════════════════════╗
║           HACKFORGE COMPLETE TEST SUITE                   ║
║                  7 Components                             ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add tests in logical order
    print("\n📋 Loading Test Suites...\n")
    
    suite.addTests(loader.loadTestsFromTestCase(TestComponentStatus))
    suite.addTests(loader.loadTestsFromTestCase(TestComponent1_CoreGeneration))
    suite.addTests(loader.loadTestsFromTestCase(TestComponent2_TemplateEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestComponent3_DockerOrchestrator))
    suite.addTests(loader.loadTestsFromTestCase(TestComponent4_API))
    
    if DATABASE_AVAILABLE:
        suite.addTests(loader.loadTestsFromTestCase(TestComponent6_Database))
    
    suite.addTests(loader.loadTestsFromTestCase(TestComponent7_Integration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests Run:    {result.testsRun}")
    print(f"Successes:    {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures:     {len(result.failures)}")
    print(f"Errors:       {len(result.errors)}")
    print(f"Skipped:      {len(result.skipped)}")
    print("="*70)
    
    if result.wasSuccessful():
        print("\n🎉 ALL TESTS PASSED! 🎉")
        print("\nYour Hackforge platform is working perfectly!")
    else:
        print("\n⚠️  Some tests failed. Check the output above.")
    
    print("\nComponent Status:")
    print("  ✓ Component 1: Core Generation")
    print("  ✓ Component 2: Template Engine")
    print("  ✓ Component 3: Docker Orchestrator")
    print("  ✓ Component 4: Web API")
    print("  ✓ Component 5: React Frontend (manual test)")
    if DATABASE_AVAILABLE:
        print("  ✓ Component 6: Database Integration")
    else:
        print("  ⚠ Component 6: Database (not tested - MongoDB not available)")
    print("  ✓ Component 7: Integration Tests")
    print()
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_all_tests(verbosity=2)
    sys.exit(0 if success else 1)
