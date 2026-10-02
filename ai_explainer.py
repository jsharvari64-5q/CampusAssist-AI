import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)


# ==========================================
# AI TOPIC EXPLAINER
# ==========================================

def explain_topic(topic, level):

    prompt = f"""
Explain the following academic topic to a student.

Topic: {topic}
Student level: {level}

Give:
1. Simple explanation
2. Important points
3. One simple example
4. Three quick revision points

Keep the explanation educational and easy to understand.
"""

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )

    return response.output_text


# ==========================================
# AI PERSONALIZED STUDY PLAN
# ==========================================

def generate_study_plan(tasks, available_hours):

    task_text = ""

    for task in tasks:

        if not task.get("completed", False):

            task_text += f"""
Subject: {task['subject']}
Topic: {task['topic']}
Difficulty: {task['difficulty']}/5
Importance: {task['importance']}/5
Days left: {task['days_left']}
Study time needed: {task['study_time']} hour(s)
Priority score: {task['priority_score']}
---
"""

    prompt = f"""
You are CampusAssist AI, an academic planning assistant.

Create a realistic personalized study plan for a student.

Available study time today: {available_hours} hours.

Pending academic tasks:
{task_text}

Create a plan that:
1. Prioritizes urgent and important tasks.
2. Considers difficulty.
3. Fits within the available study time.
4. Gives approximate time for each task.
5. Includes short breaks when appropriate.
6. Explains why the highest-priority tasks come first.
7. Ends with 3 short recommendations.

Do not invent subjects or tasks that are not provided.
Keep the plan practical and easy to follow.
"""

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )

    return response.output_text


# ==========================================
# AI STUDY RECOMMENDATIONS
# ==========================================

def generate_recommendations(tasks):

    pending_tasks = [
        task for task in tasks
        if not task.get("completed", False)
    ]

    if not pending_tasks:
        return "🎉 All your current tasks are completed!"

    task_text = ""

    for task in pending_tasks:

        task_text += f"""
Subject: {task['subject']}
Topic: {task['topic']}
Difficulty: {task['difficulty']}/5
Importance: {task['importance']}/5
Days left: {task['days_left']}
Study time: {task['study_time']} hour(s)
Priority score: {task['priority_score']}
---
"""

    prompt = f"""
You are CampusAssist AI, an academic assistant.

Analyze the student's pending academic workload:

{task_text}

Give personalized recommendations.

Include:
1. The task that needs attention first and the factual reason based on
   deadline, importance, difficulty, or priority score.
2. One task that can reasonably be scheduled later.
3. Advice for managing today's workload.
4. One suggestion for improving consistency.
5. A short motivational closing.

Use only the information provided.
Do not invent tasks or deadlines.
Keep the recommendations concise and practical.
"""

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )

    return response.output_text