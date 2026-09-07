from performance_agent import analyze_student
from planner_agent import create_study_plan
from recommendation_agent import get_recommendations

# Performance Agent
result = analyze_student("Akshay")
print(result)

# Weak subjects
weak_subjects = {
    "Python": 52,
    "DBMS": 55,
    "Data Mining": 50
}

# Planner Agent
plan = create_study_plan(weak_subjects)
print("\n" + plan)

# Recommendation Agent
recommendations = get_recommendations(weak_subjects)
print("\n" + recommendations)