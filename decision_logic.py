def is_flagged_question(user_input):
    flagged_keywords = ["sensitive", "restricted", "flagged"]
    return any(keyword in user_input.lower() for keyword in flagged_keywords)
