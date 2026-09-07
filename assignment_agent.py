from datetime import datetime


def check_assignments(assignments):
    today = datetime.now().date()

    urgent = []
    upcoming = []

    for assignment in assignments:
        deadline = datetime.strptime(
            assignment["deadline"],
            "%Y-%m-%d"
        ).date()

        days_left = (deadline - today).days

        if days_left < 0:
            urgent.append(
                f"{assignment['subject']} - Overdue"
            )

        elif days_left <= 3:
            urgent.append(
                f"{assignment['subject']} - Due in {days_left} day(s)"
            )

        else:
            upcoming.append(
                f"{assignment['subject']} - Due in {days_left} day(s)"
            )

    result = "📝 Assignment Status\n\n"

    if urgent:
        result += "🔴 Urgent:\n"
        for item in urgent:
            result += f"- {item}\n"

    if upcoming:
        result += "\n🟢 Upcoming:\n"
        for item in upcoming:
            result += f"- {item}\n"

    if not urgent and not upcoming:
        result += "No assignments found."

    return result