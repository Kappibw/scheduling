"""
Base scheduler class for Endurance robot scheduling algorithms.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime

from ..common.tasks.endurance_task import EnduranceTask
from ..common.tasks.endurance_task_manager import EnduranceTaskManager
from ..common.resources.endurance_resource import EnduranceResource
from ..common.resources.endurance_resource_manager import EnduranceResourceManager
from .endurance_schedule_result import EnduranceScheduleResult, ScheduleStatus


class EnduranceBaseScheduler(ABC):
    """Base class for all Endurance robot scheduling algorithms."""
    
    def __init__(self, name: str, time_limit: float = 300.0):
        self.name = name
        self.time_limit = time_limit
        self.task_manager: Optional[EnduranceTaskManager] = None
        self.resource_manager: Optional[EnduranceResourceManager] = None
    
    def set_managers(
        self,
        task_manager: EnduranceTaskManager,
        resource_manager: EnduranceResourceManager
    ) -> None:
        """Set the task and resource managers."""
        self.task_manager = task_manager
        self.resource_manager = resource_manager
    
    @abstractmethod
    def schedule(
        self,
        tasks: List[EnduranceTask],
        resources: List[EnduranceResource]
    ) -> EnduranceScheduleResult:
        """
        Schedule tasks for the Endurance robot.
        
        Args:
            tasks: List of tasks to schedule
            resources: List of available resources
            
        Returns:
            EnduranceScheduleResult with the scheduling outcome
        """
        pass
    
    def validate_inputs(
        self,
        tasks: List[EnduranceTask],
        resources: List[EnduranceResource]
    ) -> List[str]:
        """Validate input tasks and resources."""
        errors = []
        
        if not tasks:
            errors.append("No tasks provided")
        
        if not resources:
            errors.append("No resources provided")
        
        # Validate individual tasks
        for task in tasks:
            try:
                # Check if task has valid time constraints
                if task.start_time >= task.end_time:
                    errors.append(f"Task {task.id} has invalid time window")
                
                # Check if task has valid duration constraints
                if task.min_duration > task.max_duration:
                    errors.append(f"Task {task.id} has invalid duration constraints")
                
                # Check if preferred duration is within bounds
                if not (task.min_duration <= task.preferred_duration <= task.max_duration):
                    errors.append(f"Task {task.id} preferred duration out of bounds")
                
                # Check if max duration fits in time window
                max_possible_duration = task.end_time - task.start_time
                if task.max_duration > max_possible_duration:
                    errors.append(f"Task {task.id} max duration exceeds time window")
                
            except Exception as e:
                errors.append(f"Error validating task {task.id}: {str(e)}")
        
        # Validate individual resources
        for resource in resources:
            try:
                if resource.resource_type.value == "integer" and resource.max_capacity is None:
                    errors.append(f"Integer resource {resource.id} missing max_capacity")
                
                if resource.resource_type.value == "cumulative_rate" and resource.initial_value is None:
                    errors.append(f"Cumulative rate resource {resource.id} missing initial_value")
                
            except Exception as e:
                errors.append(f"Error validating resource {resource.id}: {str(e)}")
        
        return errors
    
    def check_task_constraints(
        self,
        task: EnduranceTask,
        scheduled_tasks: List[Dict[str, Any]]
    ) -> List[str]:
        """Check if a task's constraints can be satisfied."""
        errors = []
        
        for constraint in task.task_constraints:
            if constraint.constraint_type.value == "start_after_end":
                # Find the target task in scheduled tasks
                target_task = None
                for scheduled in scheduled_tasks:
                    if scheduled["task_id"] == constraint.target_task_id:
                        target_task = scheduled
                        break
                
                if not target_task:
                    errors.append(f"Task {task.id} depends on unscheduled task {constraint.target_task_id}")
                    continue
                
                # Check if this task can start after the target task ends
                if task.start_time < target_task["end_time"]:
                    errors.append(f"Task {task.id} cannot start after task {constraint.target_task_id} ends")
            
            elif constraint.constraint_type.value == "contained":
                # Find the target task in scheduled tasks
                target_task = None
                for scheduled in scheduled_tasks:
                    if scheduled["task_id"] == constraint.target_task_id:
                        target_task = scheduled
                        break
                
                if not target_task:
                    errors.append(f"Task {task.id} depends on unscheduled task {constraint.target_task_id}")
                    continue
                
                # Check if this task is contained within the target task
                if (task.start_time < target_task["start_time"] or 
                    task.end_time > target_task["end_time"]):
                    errors.append(f"Task {task.id} is not contained within task {constraint.target_task_id}")
        
        return errors
    
    def check_resource_constraints(
        self,
        task: EnduranceTask,
        scheduled_tasks: List[Dict[str, Any]]
    ) -> List[str]:
        """Check if a task's resource constraints can be satisfied."""
        errors = []
        
        if not self.resource_manager:
            return errors
        
        # Calculate current resource usage
        current_usage = {}
        for scheduled in scheduled_tasks:
            for resource_id, amount in scheduled.get("resource_allocations", {}).items():
                if resource_id not in current_usage:
                    current_usage[resource_id] = 0.0
                current_usage[resource_id] += amount
        
        # Check each resource constraint
        for constraint in task.resource_constraints:
            resource_id = constraint.resource_id
            resource = self.resource_manager.get_resource(resource_id)
            
            if not resource:
                errors.append(f"Resource {resource_id} not found")
                continue
            
            # Check if resource can provide the required amount
            available = resource.available_capacity - current_usage.get(resource_id, 0.0)
            
            if constraint.min_amount > available:
                errors.append(f"Resource {resource_id} cannot provide "
                             f"minimum amount {constraint.min_amount}")
            
            if constraint.max_amount > resource.max_capacity:
                errors.append(f"Resource {resource_id} max amount "
                             f"{constraint.max_amount} exceeds capacity")
        
        return errors
    
    def create_schedule_result(
        self,
        status: ScheduleStatus,
        schedule: List[Dict[str, Any]] = None,
        unscheduled_tasks: List[str] = None,
        solve_time: float = 0.0,
        message: str = "",
        metadata: Dict[str, Any] = None
    ) -> EnduranceScheduleResult:
        """Create a schedule result object."""
        if schedule is None:
            schedule = []
        if unscheduled_tasks is None:
            unscheduled_tasks = []
        if metadata is None:
            metadata = {}
        
        return EnduranceScheduleResult(
            status=status,
            schedule=schedule,
            unscheduled_tasks=unscheduled_tasks,
            solve_time=solve_time,
            message=message,
            metadata=metadata
        )
    
    def get_scheduler_info(self) -> Dict[str, Any]:
        """Get information about this scheduler."""
        return {
            "name": self.name,
            "time_limit": self.time_limit,
            "type": self.__class__.__name__
        }
