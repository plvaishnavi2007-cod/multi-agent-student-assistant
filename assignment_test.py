from assignment_agent import check_assignments

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

result = check_assignments(assignments)

print(result)