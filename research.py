#!/usr/bin/env python3
"""
Research script for robot scheduling algorithm development and comparison.
"""

import sys
import os
sys.path.append('/app')

from src.testing import TestCaseLoader, TestRunner, AlgorithmComparator
from src.algorithms.milp.simple_milp_scheduler import SimpleMILPScheduler
from src.common.visualization import ScheduleVisualizer, GanttChart
import matplotlib.pyplot as plt


def main():
    """Run algorithm research and comparison."""
    print("🧪 Robot Scheduling Algorithm Research")
    print("=" * 50)
    
    # Create test cases
    print("\n📋 Creating test cases...")
    test_cases = [
        TestCaseLoader.create_simple_test(),
        TestCaseLoader.create_complex_test(),
        TestCaseLoader.create_stress_test(num_tasks=10, num_robots=3)
    ]
    
    print(f"Created {len(test_cases)} test cases:")
    for i, test_case in enumerate(test_cases, 1):
        print(f"  {i}. {test_case.name}: {len(test_case.tasks)} tasks, {len(test_case.resources)} resources")
    
    # Initialize algorithms
    print("\n🤖 Initializing algorithms...")
    algorithms = [
        SimpleMILPScheduler(time_limit=60),
        # Add more algorithms here as you develop them
    ]
    
    print(f"Initialized {len(algorithms)} algorithms:")
    for i, algorithm in enumerate(algorithms, 1):
        print(f"  {i}. {algorithm.name}")
    
    # Run comparison
    print("\n🔄 Running algorithm comparison...")
    test_runner = TestRunner()
    comparator = AlgorithmComparator(test_runner)
    
    comparison_results = comparator.compare_algorithms(test_cases, algorithms)
    
    # Generate report
    print("\n📊 Generating performance report...")
    report = comparator.generate_report(comparison_results)
    print(report)
    
    # Save results
    print("\n💾 Saving results...")
    os.makedirs('/app/results', exist_ok=True)
    
    test_runner.save_results('/app/results/test_results.json')
    with open('/app/results/comparison_report.txt', 'w') as f:
        f.write(report)
    
    # Create visualizations
    print("\n📈 Creating visualizations...")
    fig = comparator.plot_performance_comparison(comparison_results, '/app/results/performance_comparison.png')
    plt.close(fig)
    
    # Test individual algorithm with visualization
    print("\n🎯 Testing individual algorithm with visualization...")
    test_case = test_cases[0]  # Simple test case
    algorithm = algorithms[0]  # SimpleMILPScheduler
    
    result = test_runner.run_test(test_case, algorithm)
    
    if result.schedule_result.status.value == "success":
        print(f"✅ Success! Scheduled {len(result.schedule_result.schedule)} tasks")
        
        # Create schedule visualization
        visualizer = ScheduleVisualizer()
        fig = visualizer.plot_schedule(result.schedule_result.schedule, 
                                     title=f"Schedule: {algorithm.name} on {test_case.name}")
        visualizer.save_plot(fig, '/app/results/sample_schedule.png')
        
        # Create interactive Gantt chart
        gantt = GanttChart()
        interactive_fig = gantt.create_gantt_chart(result.schedule_result.schedule, 
                                                 f"Interactive Schedule: {algorithm.name}")
        interactive_fig.write_html('/app/results/interactive_schedule.html')
        
        print("📊 Visualizations saved:")
        print("  - results/performance_comparison.png")
        print("  - results/sample_schedule.png")
        print("  - results/interactive_schedule.html")
    else:
        print(f"❌ Failed: {result.schedule_result.message}")
    
    print("\n✅ Research complete! Check the results/ directory for outputs.")


if __name__ == "__main__":
    main()
