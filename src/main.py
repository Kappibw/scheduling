"""
Main application entry point for the robot scheduling system.
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Any

from common.tasks import Task, TaskType, TaskManager
from common.resources import Resource, ResourceType, ResourceManager
from algorithms import MILPScheduler
from common.visualization import ScheduleVisualizer, GanttChart


def create_sample_tasks() -> List[Task]:
    """Create sample tasks for demonstration."""
    tasks = []
    
    # Create some sample tasks
    tasks.append(Task.create(
        task_type=TaskType.PICKUP,
        description="Pick up package from warehouse A",
        duration=timedelta(minutes=15),
        priority=1,
        location="warehouse_a"
    ))
    
    tasks.append(Task.create(
        task_type=TaskType.DELIVERY,
        description="Deliver package to location B",
        duration=timedelta(minutes=20),
        priority=2,
        location="location_b"
    ))
    
    tasks.append(Task.create(
        task_type=TaskType.INSPECTION,
        description="Inspect equipment in zone C",
        duration=timedelta(minutes=10),
        priority=3,
        location="zone_c"
    ))
    
    tasks.append(Task.create(
        task_type=TaskType.MAINTENANCE,
        description="Perform routine maintenance",
        duration=timedelta(minutes=30),
        priority=2,
        location="maintenance_bay"
    ))
    
    return tasks


def create_sample_resources() -> List[Resource]:
    """Create sample resources for demonstration."""
    resources = []
    
    # Create robots
    resources.append(Resource.create(
        resource_type=ResourceType.ROBOT,
        name="Robot-001",
        capacity=1.0,
        capabilities=["pickup", "delivery", "inspection"],
        location="warehouse"
    ))
    
    resources.append(Resource.create(
        resource_type=ResourceType.ROBOT,
        name="Robot-002",
        capacity=1.0,
        capabilities=["pickup", "delivery", "maintenance"],
        location="warehouse"
    ))
    
    # Create tools
    resources.append(Resource.create(
        resource_type=ResourceType.TOOL,
        name="Gripper-A",
        capacity=1.0,
        capabilities=["grasping", "lifting"]
    ))
    
    resources.append(Resource.create(
        resource_type=ResourceType.TOOL,
        name="Inspection-Camera",
        capacity=1.0,
        capabilities=["imaging", "analysis"]
    ))
    
    return resources


def run_scheduling_demo():
    """Run a demonstration of the scheduling system."""
    print("🤖 Robot Scheduling System Demo")
    print("=" * 50)
    
    # Create managers
    task_manager = TaskManager()
    resource_manager = ResourceManager()
    
    # Create sample data
    tasks = create_sample_tasks()
    resources = create_sample_resources()
    
    # Add tasks and resources to managers
    for task in tasks:
        task_manager.add_task(task)
    
    for resource in resources:
        resource_manager.add_resource(resource)
    
    print(f"Created {len(tasks)} tasks and {len(resources)} resources")
    
    # Create scheduler
    scheduler = MILPScheduler(solver="CBC", time_limit=60)
    scheduler.set_managers(task_manager, resource_manager)
    
    print(f"Using {scheduler.name} with {scheduler.solver} solver")
    
    # Run scheduling
    print("\n🔄 Running scheduling algorithm...")
    result = scheduler.schedule(tasks, resources)
    
    if result.status.value == "success":
        print(f"✅ Schedule created successfully!")
        print(f"   - Tasks scheduled: {len(result.schedule)}")
        print(f"   - Solve time: {result.solve_time:.2f} seconds")
        
        # Display schedule
        print("\n📅 Generated Schedule:")
        print("-" * 80)
        for i, task_schedule in enumerate(result.schedule, 1):
            print(f"{i:2d}. Task {task_schedule['task_id'][:8]} -> Robot {task_schedule['robot_id']}")
            print(f"     Start: {task_schedule['start_time']}")
            print(f"     End:   {task_schedule['end_time']}")
            print(f"     Type:  {task_schedule['task_type']}")
            print()
        
        # Create visualizations
        print("📊 Creating visualizations...")
        visualizer = ScheduleVisualizer()
        
        # Create Gantt chart
        fig = visualizer.plot_schedule(result.schedule, title="Robot Schedule - MILP Solution")
        visualizer.save_plot(fig, "results/schedule_gantt.png")
        print("   - Gantt chart saved to results/schedule_gantt.png")
        
        # Create interactive Gantt chart
        gantt_chart = GanttChart()
        interactive_fig = gantt_chart.create_gantt_chart(result.schedule, "Interactive Robot Schedule")
        interactive_fig.write_html("results/interactive_schedule.html")
        print("   - Interactive chart saved to results/interactive_schedule.html")
        
    else:
        print(f"❌ Scheduling failed: {result.message}")
        return 1
    
    return 0


def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(description="Robot Scheduling System")
    parser.add_argument("--demo", action="store_true", help="Run demonstration")
    parser.add_argument("--tasks", type=str, help="Path to tasks JSON file")
    parser.add_argument("--resources", type=str, help="Path to resources JSON file")
    parser.add_argument("--output", type=str, default="results/schedule.json", 
                       help="Output file for schedule")
    parser.add_argument("--solver", type=str, default="CBC", 
                       choices=["GUROBI", "CBC"], help="MILP solver to use")
    parser.add_argument("--time-limit", type=int, default=300, 
                       help="Time limit for solver in seconds")
    
    args = parser.parse_args()
    
    if args.demo:
        return run_scheduling_demo()
    
    # Load tasks and resources from files
    if not args.tasks or not args.resources:
        print("Error: --tasks and --resources arguments are required")
        return 1
    
    try:
        # Load tasks
        with open(args.tasks, 'r') as f:
            tasks_data = json.load(f)
        tasks = [Task.from_dict(task_data) for task_data in tasks_data]
        
        # Load resources
        with open(args.resources, 'r') as f:
            resources_data = json.load(f)
        resources = [Resource.from_dict(resource_data) for resource_data in resources_data]
        
        # Create managers
        task_manager = TaskManager()
        resource_manager = ResourceManager()
        
        for task in tasks:
            task_manager.add_task(task)
        
        for resource in resources:
            resource_manager.add_resource(resource)
        
        # Create scheduler
        scheduler = MILPScheduler(solver=args.solver, time_limit=args.time_limit)
        scheduler.set_managers(task_manager, resource_manager)
        
        # Run scheduling
        print(f"Running {scheduler.name} with {args.solver} solver...")
        result = scheduler.schedule(tasks, resources)
        
        if result.status.value == "success":
            # Save schedule
            with open(args.output, 'w') as f:
                json.dump(result.schedule, f, indent=2)
            
            print(f"Schedule saved to {args.output}")
            print(f"Tasks scheduled: {len(result.schedule)}")
            print(f"Solve time: {result.solve_time:.2f} seconds")
            
        else:
            print(f"Scheduling failed: {result.message}")
            return 1
            
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
        return 1
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON - {e}")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
