"""
Base classes for scheduling algorithms.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

from ..common.tasks import Task, TaskManager
from ..common.resources import Resource, ResourceManager


class ScheduleStatus(Enum):
    """Status of a scheduling operation."""
    SUCCESS = "success"
    FAILED = "failed"
    PARTIAL = "partial"
    TIMEOUT = "timeout"


@dataclass
class ScheduleResult:
    """Result of a scheduling operation."""
    status: ScheduleStatus
    schedule: List[Dict[str, Any]]
    objective_value: Optional[float] = None
    solve_time: Optional[float] = None
    message: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class ScheduledTask:
    """A task that has been scheduled."""
    task_id: str
    robot_id: str
    start_time: datetime
    end_time: datetime
    resources: Dict[str, float]
    priority: int = 1
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "task_id": self.task_id,
            "robot_id": self.robot_id,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "resources": self.resources,
            "priority": self.priority
        }


class BaseScheduler(ABC):
    """Base class for all scheduling algorithms."""
    
    def __init__(self, name: str = "BaseScheduler"):
        self.name = name
        self.task_manager: Optional[TaskManager] = None
        self.resource_manager: Optional[ResourceManager] = None
    
    def set_managers(self, task_manager: TaskManager, resource_manager: ResourceManager) -> None:
        """Set the task and resource managers."""
        self.task_manager = task_manager
        self.resource_manager = resource_manager
    
    @abstractmethod
    def schedule(self, tasks: List[Task], resources: List[Resource], 
                constraints: Dict[str, Any] = None) -> ScheduleResult:
        """
        Schedule tasks using available resources.
        
        Args:
            tasks: List of tasks to schedule
            resources: List of available resources
            constraints: Additional constraints for scheduling
            
        Returns:
            ScheduleResult containing the schedule and metadata
        """
        pass
    
    @abstractmethod
    def can_schedule(self, task: Task, resources: List[Resource]) -> bool:
        """
        Check if a task can be scheduled with the given resources.
        
        Args:
            task: Task to check
            resources: Available resources
            
        Returns:
            True if the task can be scheduled
        """
        pass
    
    def validate_schedule(self, schedule: List[ScheduledTask]) -> bool:
        """
        Validate a schedule for conflicts and constraints.
        
        Args:
            schedule: List of scheduled tasks
            
        Returns:
            True if the schedule is valid
        """
        # Check for resource conflicts
        resource_usage = {}
        
        for scheduled_task in schedule:
            for resource_id, amount in scheduled_task.resources.items():
                if resource_id not in resource_usage:
                    resource_usage[resource_id] = []
                
                resource_usage[resource_id].append({
                    'start': scheduled_task.start_time,
                    'end': scheduled_task.end_time,
                    'amount': amount
                })
        
        # Check for overlapping resource usage
        for resource_id, usage_list in resource_usage.items():
            # Sort by start time
            usage_list.sort(key=lambda x: x['start'])
            
            for i in range(len(usage_list) - 1):
                current = usage_list[i]
                next_usage = usage_list[i + 1]
                
                # Check for overlap
                if current['end'] > next_usage['start']:
                    # Check if total usage exceeds capacity
                    resource = self.resource_manager.get_resource(resource_id) if self.resource_manager else None
                    if resource and current['amount'] + next_usage['amount'] > resource.capacity:
                        return False
        
        return True
    
    def get_schedule_statistics(self, schedule: List[ScheduledTask]) -> Dict[str, Any]:
        """
        Get statistics about a schedule.
        
        Args:
            schedule: List of scheduled tasks
            
        Returns:
            Dictionary containing schedule statistics
        """
        if not schedule:
            return {
                "total_tasks": 0,
                "total_duration": 0,
                "makespan": 0,
                "resource_utilization": {},
                "robot_utilization": {}
            }
        
        # Calculate makespan
        makespan = max(task.end_time for task in schedule) - min(task.start_time for task in schedule)
        
        # Calculate total duration
        total_duration = sum((task.end_time - task.start_time).total_seconds() for task in schedule)
        
        # Calculate resource utilization
        resource_utilization = {}
        for task in schedule:
            for resource_id, amount in task.resources.items():
                if resource_id not in resource_utilization:
                    resource_utilization[resource_id] = 0
                resource_utilization[resource_id] += amount * (task.end_time - task.start_time).total_seconds()
        
        # Calculate robot utilization
        robot_utilization = {}
        for task in schedule:
            if task.robot_id not in robot_utilization:
                robot_utilization[task.robot_id] = 0
            robot_utilization[task.robot_id] += (task.end_time - task.start_time).total_seconds()
        
        return {
            "total_tasks": len(schedule),
            "total_duration": total_duration,
            "makespan": makespan.total_seconds(),
            "resource_utilization": resource_utilization,
            "robot_utilization": robot_utilization
        }
    
    def optimize_schedule(self, schedule: List[ScheduledTask], 
                         objective: str = "makespan") -> List[ScheduledTask]:
        """
        Optimize an existing schedule.
        
        Args:
            schedule: Current schedule
            objective: Optimization objective ("makespan", "resource_utilization", "cost")
            
        Returns:
            Optimized schedule
        """
        # Default implementation returns the original schedule
        # Subclasses should override this method
        return schedule
