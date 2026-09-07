def explain_topic(topic):
    explanations = {
        "python": "Python is a programming language used to build applications, automate tasks, analyze data, and develop AI systems.",
        "dbms": "A DBMS is software used to store, organize, retrieve, and manage data in databases.",
        "ai": "Artificial Intelligence is the field of creating systems that can perform tasks that normally require human intelligence.",
        "data mining": "Data Mining is the process of discovering useful patterns and information from large datasets."
    }

    topic_key = topic.lower().strip()

    if topic_key in explanations:
        return explanations[topic_key]

    return f"I can help you learn about {topic}. Please ask me a specific question about the topic."