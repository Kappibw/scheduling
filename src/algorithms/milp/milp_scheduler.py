"""
MILP-based scheduling algorithm for robot task scheduling.
"""

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
import numpy as np
import cvxpy as cp
from ortools.linear_solver import pywraplp

from ..base import BaseScheduler, ScheduleResult, ScheduleStatus, ScheduledTask
from ...common.tasks import Task, TaskType
from ...common.resources import Resource, ResourceType


class MILPScheduler(BaseScheduler):
    """Mixed Integer Linear Programming scheduler for robot tasks."""
    
    def __init__(self, solver: str = "CBC", time_limit: int = 300):
        super().__init__("MILPScheduler")
        self.solver = solver
        self.time_limit = time_limit
        self.solver_instance = None
    
    def schedule(self, tasks: List[Task], resources: List[Resource], 
                constraints: Dict[str, Any] = None) -> ScheduleResult:
        """
        Schedule tasks using MILP optimization.
        
        Args:
            tasks: List of tasks to schedule
            resources: List of available resources
            constraints: Additional constraints for scheduling
            
        Returns:
            ScheduleResult containing the schedule and metadata
        """
        if not tasks or not resources:
            return ScheduleResult(
                status=ScheduleStatus.FAILED,
                schedule=[],
                message="No tasks or resources provided"
            )
        
        try:
            start_time = datetime.now()
            
            # Create MILP model
            model, variables = self._create_milp_model(tasks, resources, constraints)
            
            # Solve the model
            solve_time = self._solve_model(model, variables)
            
            # Extract solution
            schedule = self._extract_solution(variables, tasks, resources)
            
            end_time = datetime.now()
            total_time = (end_time - start_time).total_seconds()
            
            return ScheduleResult(
                status=ScheduleStatus.SUCCESS,
                schedule=schedule,
                solve_time=total_time,
                message=f"Schedule created with {len(schedule)} tasks"
            )
            
        except Exception as e:
            return ScheduleResult(
                status=ScheduleStatus.FAILED,
                schedule=[],
                message=f"Error in MILP scheduling: {str(e)}"
            )
    
    def _create_milp_model(self, tasks: List[Task], resources: List[Resource], 
                          constraints: Dict[str, Any] = None) -> Tuple[Any, Dict[str, Any]]:
        """Create the MILP model for scheduling."""
        if constraints is None:
            constraints = {}
        
        # Get robots (resources of type ROBOT)
        robots = [r for r in resources if r.resource_type == ResourceType.ROBOT]
        
        if not robots:
            raise ValueError("No robots available for scheduling")
        
        # Create time horizon
        time_horizon = self._calculate_time_horizon(tasks)
        time_slots = list(range(time_horizon))
        
        # Decision variables
        variables = {}
        
        # x[i,j,t] = 1 if task i is assigned to robot j at time t
        for i, task in enumerate(tasks):
            for j, robot in enumerate(robots):
                for t in time_slots:
                    variables[f'x_{i}_{j}_{t}'] = cp.Variable(boolean=True)
        
        # y[i] = start time of task i
        for i, task in enumerate(tasks):
            variables[f'y_{i}'] = cp.Variable(integer=True, nonneg=True)
        
        # z[i] = completion time of task i
        for i, task in enumerate(tasks):
            variables[f'z_{i}'] = cp.Variable(integer=True, nonneg=True)
        
        # Objective: minimize makespan
        makespan = cp.Variable(integer=True, nonneg=True)
        variables['makespan'] = makespan
        
        # Constraints
        constraints_list = []
        
        # Each task must be assigned to exactly one robot
        for i, task in enumerate(tasks):
            for t in time_slots:
                constraint = sum(variables[f'x_{i}_{j}_{t}'] for j in range(len(robots))) <= 1
                constraints_list.append(constraint)
        
        # Task duration constraints
        for i, task in enumerate(tasks):
            duration = int(task.duration.total_seconds() / 60)  # Convert to minutes
            constraint = variables[f'z_{i}'] == variables[f'y_{i}'] + duration
            constraints_list.append(constraint)
        
        # Resource capacity constraints
        for j, robot in enumerate(robots):
            for t in time_slots:
                total_usage = sum(
                    variables[f'x_{i}_{j}_{t}'] for i in range(len(tasks))
                )
                constraint = total_usage <= robot.capacity
                constraints_list.append(constraint)
        
        # Makespan constraint
        for i, task in enumerate(tasks):
            constraint = variables[f'z_{i}'] <= makespan
            constraints_list.append(constraint)
        
        # Task dependencies
        for i, task in enumerate(tasks):
            for dep_id in task.dependencies:
                dep_index = next((j for j, t in enumerate(tasks) if t.id == dep_id), None)
                if dep_index is not None:
                    constraint = variables[f'y_{i}'] >= variables[f'z_{dep_index}']
                    constraints_list.append(constraint)
        
        # Priority constraints
        for i, task in enumerate(tasks):
            for j, other_task in enumerate(tasks):
                if i != j and task.priority > other_task.priority:
                    # Higher priority tasks should start earlier
                    constraint = variables[f'y_{i}'] <= variables[f'y_{j}']
                    constraints_list.append(constraint)
        
        # Create and solve the problem
        objective = cp.Minimize(makespan)
        problem = cp.Problem(objective, constraints_list)
        
        return problem, variables
    
    def _solve_model(self, model: Any, variables: Dict[str, Any]) -> float:
        """Solve the MILP model."""
        start_time = datetime.now()
        
        try:
            if self.solver == "GUROBI":
                try:
                    model.solve(solver=cp.GUROBI, verbose=True)
                except Exception:
                    print("Gurobi not available, falling back to CBC")
                    model.solve(solver=cp.CBC, verbose=True)
            elif self.solver == "CBC":
                model.solve(solver=cp.CBC, verbose=True)
            else:
                model.solve(verbose=True)
            
            end_time = datetime.now()
            return (end_time - start_time).total_seconds()
            
        except Exception as e:
            raise RuntimeError(f"Failed to solve MILP model: {str(e)}")
    
    def _extract_solution(self, variables: Dict[str, Any], tasks: List[Task], 
                         resources: List[Resource]) -> List[Dict[str, Any]]:
        """Extract the solution from the solved model."""
        schedule = []
        robots = [r for r in resources if r.resource_type == ResourceType.ROBOT]
        
        for i, task in enumerate(tasks):
            # Find which robot is assigned to this task
            assigned_robot = None
            start_time = None
            
            for j, robot in enumerate(robots):
                # Check if task is assigned to this robot
                assigned = False
                for t in range(1000):  # Assume max 1000 time slots
                    var_name = f'x_{i}_{j}_{t}'
                    if var_name in variables and variables[var_name].value > 0.5:
                        assigned = True
                        if start_time is None:
                            start_time = t
                        break
                
                if assigned:
                    assigned_robot = robot
                    break
            
            if assigned_robot and start_time is not None:
                start_datetime = datetime.now() + timedelta(minutes=start_time)
                end_datetime = start_datetime + task.duration
                
                scheduled_task = {
                    "task_id": task.id,
                    "robot_id": assigned_robot.id,
                    "start_time": start_datetime.isoformat(),
                    "end_time": end_datetime.isoformat(),
                    "task_type": task.task_type.value,
                    "priority": task.priority,
                    "resources": {assigned_robot.id: 1.0}
                }
                schedule.append(scheduled_task)
        
        return schedule
    
    def _calculate_time_horizon(self, tasks: List[Task]) -> int:
        """Calculate the time horizon for scheduling."""
        total_duration = sum(task.duration.total_seconds() for task in tasks)
        # Add some buffer time
        time_horizon = int(total_duration * 1.5 / 60)  # Convert to minutes
        return max(time_horizon, 100)  # Minimum 100 minutes
    
    def can_schedule(self, task: Task, resources: List[Resource]) -> bool:
        """Check if a task can be scheduled with the given resources."""
        robots = [r for r in resources if r.resource_type == ResourceType.ROBOT]
        
        if not robots:
            return False
        
        # Check if any robot can handle the task
        for robot in robots:
            if robot.status.value == "available" and robot.capacity >= 1.0:
                return True
        
        return False
    
    def optimize_schedule(self, schedule: List[ScheduledTask], 
                         objective: str = "makespan") -> List[ScheduledTask]:
        """Optimize an existing schedule using MILP."""
        # Convert ScheduledTask objects to Task objects for optimization
        tasks = []
        for scheduled_task in schedule:
            task = Task(
                id=scheduled_task.task_id,
                task_type=TaskType.TRANSPORT,  # Default type
                description="Optimization task",
                duration=scheduled_task.end_time - scheduled_task.start_time
            )
            tasks.append(task)
        
        # Get resources from resource manager
        resources = self.resource_manager.get_all_resources() if self.resource_manager else []
        
        # Create constraints based on objective
        constraints = {"objective": objective}
        
        # Run scheduling
        result = self.schedule(tasks, resources, constraints)
        
        if result.status == ScheduleStatus.SUCCESS:
            # Convert back to ScheduledTask objects
            optimized_schedule = []
            for task_data in result.schedule:
                scheduled_task = ScheduledTask(
                    task_id=task_data["task_id"],
                    robot_id=task_data["robot_id"],
                    start_time=datetime.fromisoformat(task_data["start_time"]),
                    end_time=datetime.fromisoformat(task_data["end_time"]),
                    resources=task_data["resources"],
                    priority=task_data.get("priority", 1)
                )
                optimized_schedule.append(scheduled_task)
            
            return optimized_schedule
        
        return schedule  # Return original schedule if optimization fails
