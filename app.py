import streamlit as st

from priority_engine import tasks, calculate_priority, get_priority_level
from ai_explainer import (
    explain_topic,
    generate_study_plan,
    generate_recommendations
)


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="CampusAssist AI",
    page_icon="🎓",
    layout="wide"
)


# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 0;
}

.subtitle {
    font-size: 18px;
    color: #666;
    margin-top: 0;
}

.metric-card {
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #ddd;
    background-color: #ffffff;
    text-align: center;
}

.task-card {
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #ddd;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# HEADER
# ==========================================

st.markdown(
    '<p class="main-title">🎓 CampusAssist AI</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">Your AI-powered academic assistant</p>',
    unsafe_allow_html=True
)

st.divider()


# ==========================================
# INITIALIZE TASKS
# ==========================================

for task in tasks:
    if "completed" not in task:
        task["completed"] = False

    task["priority_score"] = calculate_priority(task)


# Sort by priority
tasks.sort(
    key=lambda task: task["priority_score"],
    reverse=True
)


# ==========================================
# DASHBOARD STATISTICS
# ==========================================

total_tasks = len(tasks)

completed_tasks = sum(
    1 for task in tasks
    if task["completed"]
)

pending_tasks = total_tasks - completed_tasks

if total_tasks > 0:
    progress = completed_tasks / total_tasks
else:
    progress = 0


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📚 Total Tasks", total_tasks)

with col2:
    st.metric("✅ Completed", completed_tasks)

with col3:
    st.metric("⏳ Pending", pending_tasks)

with col4:
    st.metric("📈 Progress", f"{progress * 100:.0f}%")


st.progress(progress)

st.divider()

# ==========================================
# SUBJECT-WISE PROGRESS
# ==========================================

st.subheader("📚 Subject-wise Progress")

subjects = {}

for task in tasks:
    subject = task["subject"]

    if subject not in subjects:
        subjects[subject] = {
            "total": 0,
            "completed": 0
        }

    subjects[subject]["total"] += 1

    if task["completed"]:
        subjects[subject]["completed"] += 1


if subjects:

    columns = st.columns(len(subjects))

    for column, (subject, data) in zip(
        columns,
        subjects.items()
    ):

        total = data["total"]
        completed = data["completed"]

        subject_progress = completed / total

        with column:

            st.markdown(f"### 📖 {subject}")

            st.progress(subject_progress)

            st.write(
                f"{completed}/{total} tasks completed"
            )

            st.write(
                f"Progress: {subject_progress * 100:.0f}%"
            )

else:

    st.info("Add some tasks to see subject progress.")

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("🎓 CampusAssist AI")

st.sidebar.write("Academic Assistant")

st.sidebar.divider()

menu = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Dashboard",
        "➕ Add Task",
        "📅 Study Planner",
        "🤖 AI Explainer",
        "💡 AI Recommendations"
    ]
)

# ==========================================
# DASHBOARD
# ==========================================

if menu == "🏠 Dashboard":

    st.header("📊 Academic Dashboard")

    if not tasks:
        st.info("No tasks available. Add your first task!")

    else:

        st.subheader("🔥 Priority Tasks")

        for i, task in enumerate(tasks):

            level = get_priority_level(
                task["priority_score"]
            )

            if task["completed"]:
                status = "✅"
            else:
                status = "⏳"

            with st.container(border=True):

                col1, col2 = st.columns([4, 1])

                with col1:

                    st.write(
                        f"### {status} {task['subject']} — {task['topic']}"
                    )

                    st.write(
                        f"Priority Score: **{task['priority_score']}**"
                    )

                    st.write(
                        f"Deadline: **{task['days_left']} day(s)**"
                    )

                    st.write(
                        f"Study Time: **{task['study_time']} hour(s)**"
                    )

                with col2:

                    st.write(f"**{level}**")

                    completed = st.checkbox(
                        "Completed",
                        value=task["completed"],
                        key=f"completed_{i}"
                    )

                    task["completed"] = completed


# ==========================================
# ADD TASK
# ==========================================

elif menu == "➕ Add Task":

    st.header("➕ Add New Task")

    subject = st.text_input(
        "Subject",
        placeholder="Example: Physics"
    )

    topic = st.text_input(
        "Topic",
        placeholder="Example: Current Electricity"
    )

    col1, col2 = st.columns(2)

    with col1:

        difficulty = st.slider(
            "Difficulty",
            1,
            5,
            3
        )

        importance = st.slider(
            "Importance",
            1,
            5,
            3
        )

    with col2:

        days_left = st.number_input(
            "Days Until Deadline",
            min_value=0,
            value=3
        )

        study_time = st.number_input(
            "Study Time (hours)",
            min_value=0.5,
            value=1.0,
            step=0.5
        )

    if st.button(
        "🚀 Add Task",
        use_container_width=True
    ):

        if subject and topic:

            new_task = {
                "subject": subject,
                "topic": topic,
                "difficulty": difficulty,
                "importance": importance,
                "days_left": days_left,
                "study_time": study_time,
                "completed": False
            }

            new_task["priority_score"] = calculate_priority(
                new_task
            )

            tasks.append(new_task)

            st.success(
                f"✅ {subject} — {topic} added successfully!"
            )

        else:

            st.warning(
                "Please enter both subject and topic."
            )


# ==========================================
# STUDY PLANNER
# ==========================================

elif menu == "📅 Study Planner":

    st.header("📅 AI Personalized Study Planner")

    st.write(
        "Tell CampusAssist AI how much time you have today, "
        "and it will create a personalized study strategy."
    )

    available_hours = st.number_input(
        "⏰ Available study time today (hours)",
        min_value=0.5,
        value=3.0,
        step=0.5
    )

    pending_tasks = [
        task for task in tasks
        if not task.get("completed", False)
    ]

    if not pending_tasks:

        st.success(
            "🎉 You have completed all your current tasks!"
        )

    else:

        st.subheader("📚 Pending Work")

        for task in pending_tasks:

            st.write(
                f"• **{task['subject']} — {task['topic']}** "
                f"| Priority: {task['priority_score']} "
                f"| Deadline: {task['days_left']} day(s)"
            )

        st.divider()

        if st.button(
            "🤖 Generate AI Study Plan",
            use_container_width=True
        ):

            with st.spinner(
                "🤖 CampusAssist AI is creating your plan..."
            ):

                try:

                    study_plan = generate_study_plan(
                        tasks,
                        available_hours
                    )

                    st.subheader(
                        "🧠 Your Personalized Study Plan"
                    )

                    st.write(study_plan)

                except Exception as e:

                    st.error(
                        "Unable to generate the AI study plan."
                    )

                    st.caption(str(e))

# ==========================================
# AI EXPLAINER
# ==========================================

elif menu == "🤖 AI Explainer":

    st.header("🤖 AI Topic Explainer")

    st.write(
        "Enter a topic and CampusAssist AI will explain it "
        "according to your learning level."
    )

    topic = st.text_input(
        "📖 What topic do you want to understand?",
        placeholder="Example: Kirchhoff's Voltage Law"
    )

    level = st.selectbox(
        "🎓 Select your level",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

    if st.button(
        "✨ Explain Topic",
        use_container_width=True
    ):

        if topic:

            with st.spinner(
                "🤖 CampusAssist AI is thinking..."
            ):

                try:

                    explanation = explain_topic(
                        topic,
                        level
                    )

                    st.subheader("📖 Explanation")

                    st.write(explanation)

                except Exception as e:

                    st.error(
                        "Something went wrong while "
                        "connecting to the AI."
                    )

                    st.caption(str(e))

        else:

            st.warning(
                "Please enter a topic first."
            )
# ==========================================
# AI RECOMMENDATIONS
# ==========================================

elif menu == "💡 AI Recommendations":

    st.header("💡 AI Study Recommendations")

    st.write(
        "CampusAssist AI analyzes your pending workload "
        "and provides personalized recommendations."
    )

    if st.button(
        "🤖 Analyze My Workload",
        use_container_width=True
    ):

        with st.spinner(
            "🤖 Analyzing your academic workload..."
        ):

            try:

                recommendations = generate_recommendations(
                    tasks
                )

                st.subheader(
                    "📋 Your Recommendations"
                )

                st.write(recommendations)

            except Exception as e:

                st.error(
                    "Unable to generate recommendations."
                )

                st.caption(str(e))

# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "CampusAssist AI • Built with Python + Streamlit + AI"
)