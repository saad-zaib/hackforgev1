"""
Database Models
MongoDB schemas for users, campaigns, progress, and leaderboards
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class DifficultyLevel(str, Enum):
    """Difficulty levels"""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"
    INSANE = "insane"


class UserRole(str, Enum):
    """User roles"""
    STUDENT = "student"
    INSTRUCTOR = "instructor"
    ADMIN = "admin"


# ============================================================================
# User Models
# ============================================================================

class User(BaseModel):
    """User model"""
    user_id: str = Field(..., description="Unique user identifier")
    username: str = Field(..., description="Username")
    email: str = Field(..., description="Email address")
    role: UserRole = Field(default=UserRole.STUDENT, description="User role")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Stats
    total_points: int = Field(default=0, description="Total points earned")
    machines_solved: int = Field(default=0, description="Total machines solved")
    campaigns_completed: int = Field(default=0, description="Campaigns completed")
    current_streak: int = Field(default=0, description="Current solving streak")
    longest_streak: int = Field(default=0, description="Longest solving streak")
    
    # Preferences
    preferences: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user_123",
                "username": "hacker123",
                "email": "hacker@example.com",
                "role": "student",
                "total_points": 500,
                "machines_solved": 5
            }
        }


class UserProgress(BaseModel):
    """User progress for a specific machine"""
    user_id: str
    machine_id: str
    campaign_id: str
    
    # Status
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    solved: bool = Field(default=False)
    
    # Attempts
    attempts: int = Field(default=0, description="Number of flag submission attempts")
    hints_used: int = Field(default=0, description="Number of hints used")
    
    # Time tracking
    time_spent: int = Field(default=0, description="Time spent in seconds")
    solve_time: Optional[int] = None
    
    # Points
    points_earned: int = Field(default=0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user_123",
                "machine_id": "abc123",
                "campaign_id": "campaign_001",
                "solved": True,
                "attempts": 3,
                "points_earned": 200
            }
        }


# ============================================================================
# Campaign Models
# ============================================================================

class CampaignStatus(str, Enum):
    """Campaign status"""
    ACTIVE = "active"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class Campaign(BaseModel):
    """Campaign model"""
    campaign_id: str
    user_id: str
    
    # Configuration
    difficulty: int = Field(ge=1, le=5)
    machine_count: int
    
    # Machines
    machines: List[Dict[str, Any]]
    
    # Status
    status: CampaignStatus = Field(default=CampaignStatus.ACTIVE)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    # Progress
    machines_solved: int = Field(default=0)
    total_points: int = Field(default=0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "campaign_id": "campaign_001",
                "user_id": "user_123",
                "difficulty": 2,
                "machine_count": 5,
                "status": "active",
                "machines_solved": 2
            }
        }


# ============================================================================
# Flag Submission Models
# ============================================================================

class FlagSubmission(BaseModel):
    """Flag submission record"""
    submission_id: str
    user_id: str
    machine_id: str
    campaign_id: str
    
    # Submission
    submitted_flag: str
    correct: bool
    submitted_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Context
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    
    # Points
    points_awarded: int = Field(default=0)


# ============================================================================
# Hint Models
# ============================================================================

class HintUsage(BaseModel):
    """Hint usage record"""
    user_id: str
    machine_id: str
    campaign_id: str
    
    hint_number: int
    hint_content: str
    used_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Cost
    points_cost: int = Field(default=0)


# ============================================================================
# Achievement Models
# ============================================================================

class AchievementType(str, Enum):
    """Achievement types"""
    FIRST_BLOOD = "first_blood"
    SPEED_DEMON = "speed_demon"
    PERFECTIONIST = "perfectionist"
    STREAK_MASTER = "streak_master"
    CATEGORY_MASTER = "category_master"


class Achievement(BaseModel):
    """Achievement model"""
    achievement_id: str
    name: str
    description: str
    achievement_type: AchievementType
    
    # Requirements
    criteria: Dict[str, Any]
    
    # Rewards
    points: int = Field(default=0)
    badge_url: Optional[str] = None


class UserAchievement(BaseModel):
    """User's earned achievement"""
    user_id: str
    achievement_id: str
    earned_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Context
    related_machine_id: Optional[str] = None
    related_campaign_id: Optional[str] = None


# ============================================================================
# Leaderboard Models
# ============================================================================

class LeaderboardEntry(BaseModel):
    """Leaderboard entry"""
    user_id: str
    username: str
    
    # Stats
    total_points: int
    machines_solved: int
    campaigns_completed: int
    average_solve_time: Optional[float] = None
    
    # Ranking
    rank: int
    
    # Timestamps
    last_activity: datetime


class LeaderboardType(str, Enum):
    """Leaderboard types"""
    ALL_TIME = "all_time"
    MONTHLY = "monthly"
    WEEKLY = "weekly"
    DAILY = "daily"
    CATEGORY = "category"


# ============================================================================
# Analytics Models
# ============================================================================

class MachineStats(BaseModel):
    """Statistics for a specific machine"""
    machine_id: str
    variant: str
    difficulty: int
    
    # Solve stats
    total_attempts: int = 0
    unique_solvers: int = 0
    solve_rate: float = 0.0
    
    # Time stats
    average_solve_time: Optional[float] = None
    fastest_solve_time: Optional[int] = None
    
    # Hints
    average_hints_used: float = 0.0


class PlatformStats(BaseModel):
    """Overall platform statistics"""
    
    # Users
    total_users: int
    active_users_today: int
    active_users_week: int
    
    # Campaigns
    total_campaigns: int
    active_campaigns: int
    completed_campaigns: int
    
    # Machines
    total_machines: int
    total_solves: int
    
    # Engagement
    average_session_time: float
    total_flags_submitted: int
    total_hints_used: int
    
    # Updated
    last_updated: datetime = Field(default_factory=datetime.utcnow)


# ============================================================================
# Session Models
# ============================================================================

class UserSession(BaseModel):
    """User session tracking"""
    session_id: str
    user_id: str
    
    # Session info
    started_at: datetime = Field(default_factory=datetime.utcnow)
    last_activity: datetime = Field(default_factory=datetime.utcnow)
    ended_at: Optional[datetime] = None
    
    # Context
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    
    # Activity
    machines_visited: List[str] = Field(default_factory=list)
    flags_submitted: int = 0
    hints_requested: int = 0
