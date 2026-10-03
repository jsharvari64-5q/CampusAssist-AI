import streamlit as st

from priority_engine import calculate_priority, get_priority_level
from ai_explainer import (
    explain_topic,
    generate_study_plan,
    generate_recommendations
)
from database import add_task, get_tasks, mark_completed


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="CampusAssist AI",
    page_icon="🎓",
    layout="wide"
)


# ==========================================
# LOAD TASKS FROM DATABASE
# ==========================================

tasks = get_tasks()

for task in tasks:
    task["priority_score"] = calculate_priority(task)

tasks.sort(
    key=lambda task: task["priority_score"],
    reverse=True
)


# ==========================================
# HEADER
# ==========================================

st.title("🎓 CampusAssist AI")
st.caption("AI-Powered Academic Assistant for Students")

st.divider()


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("📚 CampusAssist AI")

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

    st.header("📊 Student Dashboard")

    total_tasks = len(tasks)

    completed_tasks = sum(
        1 for task in tasks
        if task.get("completed", False)
    )

    pending_tasks = total_tasks - completed_tasks

    if total_tasks > 0:
        overall_progress = completed_tasks / total_tasks
    else:
        overall_progress = 0

    # Metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📚 Total Tasks", total_tasks)

    with col2:
        st.metric("⏳ Pending", pending_tasks)

    with col3:
        st.metric("✅ Completed", completed_tasks)

    with col4:
        st.metric(
            "📈 Progress",
            f"{overall_progress * 100:.0f}%"
        )

    st.divider()

    # Overall progress
    st.subheader("📈 Overall Progress")

    st.progress(overall_progress)

    st.write(
        f"You have completed {completed_tasks} "
        f"out of {total_tasks} tasks."
    )

    st.divider()

    # Subject-wise progress
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

        if task.get("completed", False):
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
                    f"Progress: "
                    f"{subject_progress * 100:.0f}%"
                )

    else:

        st.info(
            "No tasks yet. Add your first task!"
        )

    st.divider()

    # Priority tasks
    st.subheader("🔥 Priority Tasks")

    if tasks:

        for task in tasks:

            if task.get("completed", False):
                status = "✅"
            else:
                status = "⏳"

            level = get_priority_level(
                task["priority_score"]
            )

            st.write(
                f"{status} **{task['subject']}** — "
                f"{task['topic']} | "
                f"Priority: **{level}** | "
                f"Score: **{task['priority_score']}**"
            )

    else:

        st.info(
            "No tasks available."
        )


# ==========================================
# ADD TASK
# ==========================================

elif menu == "➕ Add Task":

    st.header("➕ Add New Academic Task")

    st.write(
        "Add a task and CampusAssist AI will "
        "save it permanently."
    )

    subject = st.text_input(
        "📚 Subject",
        placeholder="e.g. Physics"
    )

    topic = st.text_input(
        "📖 Topic",
        placeholder="e.g. Current Electricity"
    )

    difficulty = st.slider(
        "🔥 Difficulty",
        min_value=1,
        max_value=5,
        value=3
    )

    importance = st.slider(
        "⭐ Importance",
        min_value=1,
        max_value=5,
        value=3
    )

    days_left = st.number_input(
        "📅 Days Left",
        min_value=0,
        value=5
    )

    study_time = st.number_input(
        "⏱️ Study Time Required (hours)",
        min_value=0.5,
        value=1.0,
        step=0.5
    )

    if st.button(
        "➕ Add Task",
        use_container_width=True
    ):

        if not subject or not topic:

            st.error(
                "❌ Please enter both subject and topic."
            )

        else:

            add_task(
                subject,
                topic,
                difficulty,
                importance,
                days_left,
                study_time
            )

            st.success(
                "✅ Task added and saved permanently!"
            )

            st.rerun()


# ==========================================
# STUDY PLANNER
# ==========================================

elif menu == "📅 Study Planner":

    st.header("📅 AI Personalized Study Planner")

    st.write(
        "Tell CampusAssist AI how much time you "
        "have today."
    )

    available_hours = st.number_input(
        "⏱️ Available Study Hours",
        min_value=0.5,
        value=3.0,
        step=0.5
    )

    if st.button(
        "🤖 Generate My Study Plan",
        use_container_width=True
    ):

        with st.spinner(
            "🤖 Creating your personalized study plan..."
        ):

            try:

                study_plan = generate_study_plan(
                    tasks,
                    available_hours
                )

                st.subheader("📋 Your Study Plan")

                st.write(study_plan)

            except Exception as e:

                st.error(
                    "Unable to generate study plan."
                )

                st.caption(str(e))


# ==========================================
# AI EXPLAINER
# ==========================================

elif menu == "🤖 AI Explainer":

    st.header("🤖 AI Topic Explainer")

    st.write(
        "Ask CampusAssist AI to explain an "
        "academic topic."
    )

    topic = st.text_input(
        "📖 Enter Topic",
        placeholder="e.g. Kirchhoff's Voltage Law"
    )

    level = st.selectbox(
        "🎓 Your Learning Level",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

    if st.button(
        "🤖 Explain Topic",
        use_container_width=True
    ):

        if not topic:

            st.warning(
                "Please enter a topic first."
            )

        else:

            with st.spinner(
                "🤖 Preparing your explanation..."
            ):

                try:

                    explanation = explain_topic(
                        topic,
                        level
                    )

                    st.subheader(
                        f"📖 Explanation: {topic}"
                    )

                    st.write(explanation)

                except Exception as e:

                    st.error(
                        "Unable to explain the topic."
                    )

                    st.caption(str(e))


# ==========================================
# AI RECOMMENDATIONS
# ==========================================

elif menu == "💡 AI Recommendations":

    st.header("💡 AI Study Recommendations")

    st.write(
        "CampusAssist AI analyzes your pending "
        "workload and provides personalized "
        "recommendations."
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
    "🎓 CampusAssist AI | "
    "Built with Python, Streamlit, SQLite & AI"
)