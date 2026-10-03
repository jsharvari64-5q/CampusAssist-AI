import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    raise ValueError(
        "OPENAI_API_KEY is missing. "
        "Please check your .env file."
    )

client = OpenAI(api_key=API_KEY)


def ask_ai(prompt):
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text


# ==========================================
# AI TOPIC EXPLAINER
# ==========================================

def explain_topic(topic, level):

    prompt = f"""
You are CampusAssist AI, an educational assistant.

Explain the following academic topic:

Topic: {topic}
Student Level: {level}

Give the explanation in this structure:

1. Simple definition
2. Core concept
3. Step-by-step explanation
4. Easy example
5. Common mistakes
6. Quick revision points
7. Two practice questions

Keep the explanation educational, clear and appropriate
for a college student.
"""

    return ask_ai(prompt)


# ==========================================
# AI PERSONALIZED STUDY PLAN
# ==========================================

def generate_study_plan(tasks, available_hours):

    task_text = ""

    for task in tasks:

        if task.get("completed", False):
            continue

        task_text += f"""
Subject: {task['subject']}
Topic: {task['topic']}
Difficulty: {task['difficulty']}/5
Importance: {task['importance']}/5
Days Left: {task['days_left']}
Study Time: {task['study_time']} hours
Priority Score: {task.get('priority_score', 0)}
---
"""

    prompt = f"""
You are CampusAssist AI, an intelligent academic planning assistant.

The student has {available_hours} hours available today.

Here are the student's pending tasks:

{task_text}

Create a realistic personalized study plan.

Requirements:

1. Prioritize urgent and important tasks.
2. Consider difficulty.
3. Consider days remaining.
4. Do not exceed the available study time.
5. Include short breaks.
6. Give a clear timetable.
7. Explain why each task was selected.
8. Include a final quick-review session.
9. If the available time is insufficient, clearly identify
   what should be postponed.

Use this format:

## Today's Study Plan

### Session 1
Subject:
Topic:
Duration:
Reason:

### Break

### Session 2
Subject:
Topic:
Duration:
Reason:

### Final Revision
Duration:
What to revise:

### Priority for Tomorrow
List the remaining important tasks.

Keep the plan practical for a college student.
"""

    return ask_ai(prompt)


# ==========================================
# AI STUDY RECOMMENDATIONS
# ==========================================

def generate_recommendations(tasks):

    task_text = ""

    for task in tasks:

        status = (
            "Completed"
            if task.get("completed", False)
            else "Pending"
        )

        task_text += f"""
Subject: {task['subject']}
Topic: {task['topic']}
Difficulty: {task['difficulty']}/5
Importance: {task['importance']}/5
Days Left: {task['days_left']}
Study Time: {task['study_time']} hours
Status: {status}
Priority Score: {task.get('priority_score', 0)}
---
"""

    prompt = f"""
You are CampusAssist AI.

Analyze the student's academic workload:

{task_text}

Give personalized recommendations.

Analyze:

1. Most urgent task
2. Most difficult task
3. Workload balance
4. Possible deadline risks
5. What the student should study first
6. What can be postponed
7. How to improve consistency
8. One practical recommendation for tomorrow

Keep the recommendations concise and actionable.
"""

    return ask_ai(prompt)


# ==========================================
# AI TASK ANALYZER
# ==========================================

def analyze_task(subject, topic, difficulty, importance, days_left):

    prompt = f"""
You are CampusAssist AI.

Analyze this academic task:

Subject: {subject}
Topic: {topic}
Difficulty: {difficulty}/5
Importance: {importance}/5
Days Left: {days_left}

Return:

1. Urgency level
2. Difficulty assessment
3. Recommended study approach
4. Suggested number of study sessions
5. One common mistake to avoid

Keep the answer concise.
"""

    return ask_ai(prompt)


# ==========================================
# AI QUICK REVISION
# ==========================================

def generate_revision(topic):

    prompt = f"""
You are CampusAssist AI.

Create a quick revision sheet for:

Topic: {topic}

Include:

- 5 key concepts
- Important formulas or facts if applicable
- 3 common mistakes
- 3 quick questions
- One memory trick

Keep it short enough to revise in 5 minutes.
"""

    return ask_ai(prompt)