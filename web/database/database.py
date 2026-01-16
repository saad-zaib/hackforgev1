"""
Database Connection and Operations
MongoDB connection and CRUD operations
Enhanced with campaign naming support
"""

from pymongo import MongoClient
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import os


class DatabaseManager:
    """Database manager for MongoDB operations"""
    
    def __init__(self, connection_string: str = None):
        if connection_string is None:
            connection_string = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
        
        self.client = MongoClient(connection_string)
        self.db = self.client['hackforge']
        
        # Collections
        self.users = self.db['users']
        self.campaigns = self.db['campaigns']
        self.progress = self.db['progress']
        self.submissions = self.db['flag_submissions']
        self.hints = self.db['hint_usage']
        self.achievements = self.db['achievements']
        self.user_achievements = self.db['user_achievements']
        self.sessions = self.db['sessions']
        
        self._create_indexes()
    
    def _create_indexes(self):
        """Create database indexes"""
        self.users.create_index('user_id', unique=True)
        self.users.create_index('email', unique=True)
        self.campaigns.create_index('campaign_id', unique=True)
        self.campaigns.create_index([('user_id', 1), ('created_at', -1)])  # For listing user's campaigns
        self.progress.create_index([('user_id', 1), ('machine_id', 1)], unique=True)
    
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        user_data['created_at'] = datetime.utcnow()
        result = self.users.insert_one(user_data)
        user_data['_id'] = str(result.inserted_id)
        return user_data
    
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID, excluding MongoDB _id field"""
        return self.users.find_one(
            {'user_id': user_id},
            {'_id': 0}
        )
    
    def add_points(self, user_id: str, points: int) -> bool:
        result = self.users.update_one(
            {'user_id': user_id},
            {'$inc': {'total_points': points}}
        )
        return result.modified_count > 0
    
    def increment_solved(self, user_id: str) -> bool:
        result = self.users.update_one(
            {'user_id': user_id},
            {'$inc': {'machines_solved': 1}}
        )
        return result.modified_count > 0
    
    def create_campaign(self, campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new campaign with name support"""
        campaign_data['created_at'] = datetime.utcnow()
        
        # Ensure campaign_name exists
        if 'campaign_name' not in campaign_data:
            campaign_data['campaign_name'] = f"Campaign {campaign_data.get('campaign_id', 'Unknown')}"
        
        # Set default status if not provided
        if 'status' not in campaign_data:
            campaign_data['status'] = 'active'
        
        result = self.campaigns.insert_one(campaign_data)
        campaign_data['_id'] = str(result.inserted_id)
        return campaign_data
    
    def get_campaign(self, campaign_id: str) -> Optional[Dict[str, Any]]:
        """Get campaign by ID, excluding MongoDB _id field"""
        return self.campaigns.find_one(
            {'campaign_id': campaign_id},
            {'_id': 0}
        )
    
    def get_user_campaigns(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all campaigns for a user, sorted by creation date (newest first)"""
        # Exclude _id field from results using MongoDB projection
        campaigns = list(
            self.campaigns.find(
                {'user_id': user_id},
                {'_id': 0}
            ).sort('created_at', -1)
        )
        return campaigns
    
    def update_campaign_name(self, campaign_id: str, new_name: str) -> bool:
        """Update campaign name"""
        result = self.campaigns.update_one(
            {'campaign_id': campaign_id},
            {'$set': {'campaign_name': new_name}}
        )
        return result.modified_count > 0
    
    def create_progress(self, progress_data: Dict[str, Any]) -> Dict[str, Any]:
        progress_data['started_at'] = datetime.utcnow()
        progress_data['solved'] = False
        progress_data['attempts'] = 0
        result = self.progress.insert_one(progress_data)
        progress_data['_id'] = str(result.inserted_id)
        return progress_data
    
    def get_progress(self, user_id: str, machine_id: str) -> Optional[Dict[str, Any]]:
        return self.progress.find_one({'user_id': user_id, 'machine_id': machine_id})
    
    def increment_attempts(self, user_id: str, machine_id: str) -> bool:
        result = self.progress.update_one(
            {'user_id': user_id, 'machine_id': machine_id},
            {'$inc': {'attempts': 1}}
        )
        return result.modified_count > 0
    
    def mark_solved(self, user_id: str, machine_id: str, points: int, solve_time: int) -> bool:
        result = self.progress.update_one(
            {'user_id': user_id, 'machine_id': machine_id},
            {'$set': {'solved': True, 'points_earned': points, 'solve_time': solve_time, 'completed_at': datetime.utcnow()}}
        )
        return result.modified_count > 0
    
    def get_campaign_progress(self, user_id: str, campaign_id: str) -> List[Dict[str, Any]]:
        return list(self.progress.find({'user_id': user_id, 'campaign_id': campaign_id}))
    
    def update_campaign_progress(self, campaign_id: str, solved_count: int, points: int) -> bool:
        result = self.campaigns.update_one(
            {'campaign_id': campaign_id},
            {'$set': {'machines_solved': solved_count, 'total_points': points}}
        )
        return result.modified_count > 0
    
    def complete_campaign(self, campaign_id: str) -> bool:
        result = self.campaigns.update_one(
            {'campaign_id': campaign_id},
            {'$set': {'status': 'completed', 'completed_at': datetime.utcnow()}}
        )
        
        # Also increment user's campaigns_completed counter
        campaign = self.get_campaign(campaign_id)
        if campaign:
            self.users.update_one(
                {'user_id': campaign['user_id']},
                {'$inc': {'campaigns_completed': 1}}
            )
        
        return result.modified_count > 0
    
    def record_submission(self, submission_data: Dict[str, Any]) -> Dict[str, Any]:
        submission_data['submitted_at'] = datetime.utcnow()
        result = self.submissions.insert_one(submission_data)
        submission_data['_id'] = str(result.inserted_id)
        return submission_data
    
    def get_user_submissions(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        return list(self.submissions.find({'user_id': user_id}).sort('submitted_at', -1).limit(limit))
    
    def get_leaderboard(self, limit: int = 100, timeframe: str = 'all_time') -> List[Dict[str, Any]]:
        """Get leaderboard with optional timeframe filtering"""
        
        # Build query based on timeframe
        query = {}
        if timeframe == 'weekly':
            week_ago = datetime.utcnow() - timedelta(days=7)
            query = {'created_at': {'$gte': week_ago}}
        elif timeframe == 'monthly':
            month_ago = datetime.utcnow() - timedelta(days=30)
            query = {'created_at': {'$gte': month_ago}}
        
        # Get users sorted by points
        users = list(self.users.find(query).sort('total_points', -1).limit(limit))
        
        # Add rank to each user
        for idx, user in enumerate(users, 1):
            user['rank'] = idx
        
        return users
    
    def get_user_rank(self, user_id: str) -> Optional[int]:
        """Get user's rank based on total points"""
        user = self.get_user(user_id)
        if not user:
            return None
        rank = self.users.count_documents({'total_points': {'$gt': user['total_points']}}) + 1
        return rank
    
    def get_platform_stats(self) -> Dict[str, Any]:
        """Get overall platform statistics"""
        return {
            'total_users': self.users.count_documents({}),
            'total_campaigns': self.campaigns.count_documents({}),
            'active_campaigns': self.campaigns.count_documents({'status': 'active'}),
            'completed_campaigns': self.campaigns.count_documents({'status': 'completed'}),
            'total_solves': self.progress.count_documents({'solved': True}),
            'total_flags_submitted': self.submissions.count_documents({}),
        }
    
    def get_machine_stats(self, machine_id: str) -> Dict[str, Any]:
        """Get statistics for a specific machine"""
        total_attempts = self.progress.count_documents({'machine_id': machine_id})
        unique_solvers = self.progress.count_documents({'machine_id': machine_id, 'solved': True})
        
        # Calculate average solve time
        solved_progress = list(self.progress.find({'machine_id': machine_id, 'solved': True}))
        avg_solve_time = None
        if solved_progress:
            total_time = sum(p.get('solve_time', 0) for p in solved_progress)
            avg_solve_time = total_time / len(solved_progress) if len(solved_progress) > 0 else None
        
        return {
            'machine_id': machine_id,
            'total_attempts': total_attempts,
            'unique_solvers': unique_solvers,
            'average_solve_time': avg_solve_time
        }
    
    def search_campaigns(self, user_id: str, search_term: str) -> List[Dict[str, Any]]:
        """Search user's campaigns by name"""
        query = {
            'user_id': user_id,
            'campaign_name': {'$regex': search_term, '$options': 'i'}  # Case-insensitive search
        }
        return list(self.campaigns.find(query).sort('created_at', -1))
    
    def get_campaign_statistics(self, campaign_id: str) -> Dict[str, Any]:
        """Get detailed statistics for a campaign"""
        campaign = self.get_campaign(campaign_id)
        if not campaign:
            return None
        
        progress_list = self.get_campaign_progress(campaign['user_id'], campaign_id)
        
        total_attempts = sum(p.get('attempts', 0) for p in progress_list)
        solved_count = sum(1 for p in progress_list if p.get('solved', False))
        total_points = sum(p.get('points_earned', 0) for p in progress_list)
        
        return {
            'campaign_id': campaign_id,
            'campaign_name': campaign.get('campaign_name', 'Unknown'),
            'total_machines': campaign['machine_count'],
            'solved_machines': solved_count,
            'total_attempts': total_attempts,
            'total_points': total_points,
            'completion_percentage': (solved_count / campaign['machine_count'] * 100) if campaign['machine_count'] > 0 else 0,
            'status': campaign.get('status', 'active'),
            'created_at': campaign.get('created_at')
        }


_db_manager = None

def get_db() -> DatabaseManager:
    """Get singleton database manager instance"""
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager()
    return _db_manager
