from performance_agent import analyze_student
from planner_agent import create_study_plan
from study_agent import explain_topic
from assignment_agent import check_assignments


def coordinator(request, student_name="Sneha"):

    request_lower = request.lower()

    # 1. Performance Agent
    if (
        "mark" in request_lower
        or "performance" in request_lower
        or "score" in request_lower
    ):
        weak_subjects, analysis = analyze_student(student_name)
        return analysis

    # 2. Planner Agent
    elif (
        "plan" in request_lower
        or "schedule" in request_lower
        or "timetable" in request_lower
    ):
        weak_subjects, analysis = analyze_student(student_name)

        if weak_subjects is not None:
            return create_study_plan(weak_subjects)

        return "I couldn't find the student's performance data."

    # 3. Study Agent
    elif (
        "explain" in request_lower
        or "learn" in request_lower
        or "study" in request_lower
    ):
        topic = (
            request_lower
            .replace("explain", "")
            .replace("learn", "")
            .replace("study", "")
            .strip()
        )

        if not topic:
            return "Please tell me which topic you want to learn."

        return explain_topic(topic)

    # 4. Assignment Agent
    elif (
        "assignment" in request_lower
        or "deadline" in request_lower
        or "due" in request_lower
    ):

        assignments = [
            {
                "subject": "Python",
                "deadline": "2026-08-15"
            },
            {
                "subject": "DBMS",
                "deadline": "2026-08-25"
            },
            {
                "subject": "AI",
                "deadline": "2026-08-30"
            }
        ]

        return check_assignments(assignments)

    # Unknown request
    else:
        return (
            "I can help you with:\n"
            "📊 Performance analysis\n"
            "📅 Study planning\n"
            "📚 Topic explanations\n"
            "📝 Assignment deadlines"
        )