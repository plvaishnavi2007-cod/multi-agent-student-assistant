from performance_agent import analyze_student
from planner_agent import create_study_plan


student_name = "Sneha"

# Agent 1: Analyze performance
weak_subjects, analysis = analyze_student(student_name)

print("===== PERFORMANCE AGENT =====")
print(analysis)

# Agent 2: Create study plan
print("\n===== PLANNER AGENT =====")

if weak_subjects is not None:
    plan = create_study_plan(weak_subjects)
    print(plan)