def get_recommendations(weak_subjects):
    if not weak_subjects:
        return "No specific recommendations. Keep revising all subjects regularly."

    recommendations = "🎯 Personalized Recommendations\n\n"

    # Find the weakest subject
    weakest_subject = min(weak_subjects, key=weak_subjects.get)
    weakest_mark = weak_subjects[weakest_subject]

    recommendations += f"⭐ Priority Subject: {weakest_subject}\n"
    recommendations += f"Current Score: {weakest_mark}\n\n"

    recommendations += "📌 Recommendations:\n"
    recommendations += f"1. Spend extra study time on {weakest_subject}.\n"
    recommendations += "2. Practice questions after each study session.\n"
    recommendations += "3. Revise difficult topics regularly.\n"
    recommendations += "4. Take a short test at the end of the week.\n"

    return recommendations