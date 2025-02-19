import requests

# Your OpenRouter API key (Make sure to keep it secure)
OPENROUTER_API_KEY = "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"

def analyze_marks_with_ai(name, subjects_marks):
    """
    Sends student marks to OpenRouter Gemini AI for analysis.

    Args:
        name (str): Student's name
        subjects_marks (dict): Dictionary of subject names and marks (e.g., {"Math": 85, "Science": 78})

    Returns:
        str: AI-generated feedback on student performance
    """
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    # Format subject-wise marks for prompt
    marks_text = "\n".join([f"{sub}: {marks}" for sub, marks in subjects_marks.items()])
    
    prompt = (
        f"Analyze the academic performance of {name}. "
        f"Here are the student's subject-wise scores:\n{marks_text}\n"
        f"Provide feedback on strengths, areas of improvement, and study strategies."
    )

    data = {
        "model": "google/gemini-2.0-flash-lite-preview-02-05:free",
        "messages": [
            {"role": "system", "content": "You are an AI tutor providing performance analysis."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "Analysis unavailable due to AI service error."


def generate_report_card(student_name, subjects_marks, analysis):
    """
    Generates a formatted report card with student's marks and AI analysis.

    Args:
        student_name (str): Name of the student
        subjects_marks (dict): Dictionary of subjects and their marks
        analysis (str): AI-generated feedback

    Returns:
        str: Formatted report card as a string
    """
    report = f"📜 **Student Report Card** 📜\n\n"
    report += f"**Name:** {student_name}\n"
    report += "-------------------------\n"
    
    for subject, marks in subjects_marks.items():
        report += f"📌 {subject}: {marks}/100\n"

    report += "-------------------------\n\n"
    report += f"🔍 **Performance Analysis:**\n{analysis}\n"
    
    return report
