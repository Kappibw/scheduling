"""
Simplified MILP-based scheduling algorithm using only OR-Tools.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from ortools.linear_solver import pywraplp

from ..base import BaseScheduler, ScheduleResult, ScheduleStatus, ScheduledTask
from src.common.tasks import Task, TaskType
from src.common.resources import Resource, ResourceType


class SimpleMILPScheduler(BaseScheduler):
    """Simplified MILP scheduler using OR-Tools only."""
    
    def __init__(self, time_limit: int = 300):
        super().__init__("SimpleMILPScheduler")
        self.time_limit = time_limit
    
    def schedule(self, tasks: List[Task], resources: List[Resource], 
                constraints: Dict[str, Any] = None) -> ScheduleResult:
        """
        Schedule tasks using OR-Tools MILP optimization.
        
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
            
            # Get robots (resources of type ROBOT)
            robots = [r for r in resources if r.resource_type == ResourceType.ROBOT]
            
            if not robots:
                return ScheduleResult(
                    status=ScheduleStatus.FAILED,
                    schedule=[],
                    message="No robots available for scheduling"
                )
            
            # Create OR-Tools solver
            solver = pywraplp.Solver.CreateSolver('SCIP')
            if not solver:
                return ScheduleResult(
                    status=ScheduleStatus.FAILED,
                    schedule=[],
                    message="Could not create OR-Tools solver"
                )
            
            # Set time limit
            solver.SetTimeLimit(self.time_limit * 1000)  # Convert to milliseconds
            
            # Create time horizon
            time_horizon = self._calculate_time_horizon(tasks)
            
            # Decision variables
            # x[i,j,t] = 1 if task i is assigned to robot j at time t
            x = {}
            for i, task in enumerate(tasks):
                for j, robot in enumerate(robots):
                    for t in range(time_horizon):
                        x[i, j, t] = solver.IntVar(0, 1, f'x_{i}_{j}_{t}')
            
            # y[i] = start time of task i
            y = {}
            for i, task in enumerate(tasks):
                y[i] = solver.IntVar(0, time_horizon - 1, f'y_{i}')
            
            # z[i] = completion time of task i
            z = {}
            for i, task in enumerate(tasks):
                z[i] = solver.IntVar(0, time_horizon, f'z_{i}')
            
            # Makespan variable
            makespan = solver.IntVar(0, time_horizon, 'makespan')
            
            # Constraints
            # Each task must be assigned to exactly one robot
            for i, task in enumerate(tasks):
                duration = int(task.duration.total_seconds() / 60)  # Convert to minutes
                for t in range(time_horizon - duration + 1):
                    constraint = solver.Constraint(0, 1)
                    for j in range(len(robots)):
                        constraint.SetCoefficient(x[i, j, t], 1)
            
            # Task duration constraints
            for i, task in enumerate(tasks):
                duration = int(task.duration.total_seconds() / 60)
                constraint = solver.Constraint(duration, duration)
                constraint.SetCoefficient(z[i], 1)
                constraint.SetCoefficient(y[i], -1)
            
            # Resource capacity constraints
            for j, robot in enumerate(robots):
                for t in range(time_horizon):
                    constraint = solver.Constraint(0, robot.capacity)
                    for i, task in enumerate(tasks):
                        duration = int(task.duration.total_seconds() / 60)
                        for start_t in range(max(0, t - duration + 1), min(time_horizon, t + 1)):
                            if (i, j, start_t) in x:
                                constraint.SetCoefficient(x[i, j, start_t], 1)
            
            # Makespan constraint
            for i, task in enumerate(tasks):
                constraint = solver.Constraint(0, solver.infinity())
                constraint.SetCoefficient(z[i], 1)
                constraint.SetCoefficient(makespan, -1)
            
            # Task dependencies
            for i, task in enumerate(tasks):
                for dep_id in task.dependencies:
                    dep_index = next((j for j, t in enumerate(tasks) if t.id == dep_id), None)
                    if dep_index is not None:
                        constraint = solver.Constraint(0, solver.infinity())
                        constraint.SetCoefficient(y[i], 1)
                        constraint.SetCoefficient(z[dep_index], -1)
            
            # Objective: minimize makespan
            objective = solver.Objective()
            objective.SetCoefficient(makespan, 1)
            objective.SetMinimization()
            
            # Solve
            status = solver.Solve()
            
            end_time = datetime.now()
            solve_time = (end_time - start_time).total_seconds()
            
            if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
                # Extract solution
                schedule = self._extract_ortools_solution(x, y, z, tasks, robots, time_horizon)
                
                return ScheduleResult(
                    status=ScheduleStatus.SUCCESS,
                    schedule=schedule,
                    objective_value=makespan.solution_value(),
                    solve_time=solve_time,
                    message=f"Schedule created with {len(schedule)} tasks"
                )
            else:
                return ScheduleResult(
                    status=ScheduleStatus.FAILED,
                    schedule=[],
                    solve_time=solve_time,
                    message=f"Solver failed with status: {status}"
                )
                
        except Exception as e:
            return ScheduleResult(
                status=ScheduleStatus.FAILED,
                schedule=[],
                message=f"Error in MILP scheduling: {str(e)}"
            )
    
    def _extract_ortools_solution(self, x: Dict, y: Dict, z: Dict, 
                                 tasks: List[Task], robots: List[Resource], 
                                 time_horizon: int) -> List[Dict[str, Any]]:
        """Extract the solution from OR-Tools solver."""
        schedule = []
        
        for i, task in enumerate(tasks):
            # Find which robot is assigned to this task
            assigned_robot = None
            start_time = None
            
            for j, robot in enumerate(robots):
                # Check if task is assigned to this robot
                for t in range(time_horizon):
                    if (i, j, t) in x and x[i, j, t].solution_value() > 0.5:
                        assigned_robot = robot
                        start_time = t
                        break
                if assigned_robot:
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
