def create_study_plan(weak_subjects):
    if not weak_subjects:
        return "No weak subjects found. Focus on revision and practice."

    plan = "📅 7-Day Personalized Study Plan\n\n"

    subjects = list(weak_subjects.keys())

    for day in range(1, 8):
        subject = subjects[(day - 1) % len(subjects)]
        plan += f"Day {day} → Study {subject}\n"

    return plan