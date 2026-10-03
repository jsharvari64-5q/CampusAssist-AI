import streamlit as st

from priority_engine import calculate_priority, get_priority_level
from ai_explainer import (
    explain_topic,
    generate_study_plan,
    generate_recommendations,
    generate_revision
)
from database import add_task, get_tasks, mark_completed


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="CampusAssist AI",
    page_icon="🎓",
    layout="wide"
)


# --------------------------------------------------
# LOAD TASKS
# --------------------------------------------------

tasks = get_tasks()

for task in tasks:
    task["priority_score"] = calculate_priority(task)

tasks.sort(
    key=lambda task: task["priority_score"],
    reverse=True
)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("🎓 CampusAssist AI")

menu = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Dashboard",
        "📊 Analytics",
        "➕ Add Task",
        "📅 Study Planner",
        "🤖 AI Explainer",
        "💡 AI Recommendations",
        "📝 Quick Revision"
    ]
)


# ==================================================
# DASHBOARD
# ==================================================

if menu == "🏠 Dashboard":

    st.title("🎓 CampusAssist AI")
    st.caption("AI-Powered Academic Assistant for Students")
    st.divider()

    st.header("📊 Student Dashboard")

    total_tasks = len(tasks)

    completed_tasks = sum(
        1 for task in tasks
        if task.get("completed", False)
    )

    pending_tasks = total_tasks - completed_tasks

    total_hours = sum(
        task["study_time"]
        for task in tasks
        if not task.get("completed", False)
    )

    if total_tasks > 0:
        overall_progress = completed_tasks / total_tasks
    else:
        overall_progress = 0

    # Metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "📚 Total Tasks",
            total_tasks
        )

    with col2:
        st.metric(
            "⏳ Pending",
            pending_tasks
        )

    with col3:
        st.metric(
            "⏱️ Pending Hours",
            f"{total_hours:.1f}h"
        )

    with col4:
        st.metric(
            "📈 Progress",
            f"{overall_progress * 100:.0f}%"
        )

    st.divider()

    # Progress
    st.subheader("📈 Overall Progress")

    st.progress(overall_progress)

    st.write(
        f"You have completed "
        f"**{completed_tasks} out of {total_tasks} tasks**."
    )

    st.divider()

    # Task completion
    st.subheader("✅ Task Management")

    if tasks:

        for task in tasks:

            col1, col2, col3, col4 = st.columns(
                [0.5, 3, 1, 1]
            )

            with col1:

                completed = st.checkbox(
                    "",
                    value=task.get("completed", False),
                    key=f"complete_{task['id']}"
                )

                if completed != task.get("completed", False):

                    mark_completed(
                        task["id"],
                        completed
                    )

                    st.rerun()

            with col2:

                status = (
                    "~~"
                    if task.get("completed", False)
                    else ""
                )

                st.write(
                    f"**{task['subject']}** — "
                    f"{task['topic']}"
                )

            with col3:

                level = get_priority_level(
                    task["priority_score"]
                )

                st.write(
                    f"🔥 {level}"
                )

            with col4:

                st.write(
                    f"⏱️ {task['study_time']}h"
                )

    else:

        st.info(
            "No tasks yet. Add your first academic task!"
        )


# ==================================================
# ANALYTICS
# ==================================================

elif menu == "📊 Analytics":

    st.title("📊 Academic Analytics")

    st.caption(
        "Data-driven insights from your academic workload."
    )

    st.divider()

    if not tasks:

        st.info(
            "Add some academic tasks to generate analytics."
        )

    else:

        # ------------------------------------------
        # BASIC CALCULATIONS
        # ------------------------------------------

        total_tasks = len(tasks)

        completed_tasks = sum(
            1 for task in tasks
            if task.get("completed", False)
        )

        pending_tasks = total_tasks - completed_tasks

        total_study_hours = sum(
            task["study_time"]
            for task in tasks
        )

        pending_hours = sum(
            task["study_time"]
            for task in tasks
            if not task.get("completed", False)
        )

        high_priority = sum(
            1 for task in tasks
            if get_priority_level(
                task["priority_score"]
            ) == "HIGH"
            and not task.get("completed", False)
        )

        if total_tasks > 0:
            completion_rate = (
                completed_tasks / total_tasks
            ) * 100
        else:
            completion_rate = 0

        # ------------------------------------------
        # TOP METRICS
        # ------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "📚 Total Tasks",
                total_tasks
            )

        with col2:
            st.metric(
                "✅ Completed",
                completed_tasks
            )

        with col3:
            st.metric(
                "⏱️ Pending Study",
                f"{pending_hours:.1f}h"
            )

        with col4:
            st.metric(
                "🔥 High Priority",
                high_priority
            )

        st.divider()

        # ------------------------------------------
        # COMPLETION ANALYTICS
        # ------------------------------------------

        st.subheader("📈 Completion Analytics")

        completion_data = {
            "Status": [
                "Completed",
                "Pending"
            ],
            "Tasks": [
                completed_tasks,
                pending_tasks
            ]
        }

        st.bar_chart(
            completion_data,
            x="Status",
            y="Tasks"
        )

        st.write(
            f"**Completion Rate:** "
            f"{completion_rate:.1f}%"
        )

        st.divider()

        # ------------------------------------------
        # SUBJECT WORKLOAD
        # ------------------------------------------

        st.subheader("📚 Subject-wise Workload")

        subject_hours = {}

        for task in tasks:

            subject = task["subject"]

            if subject not in subject_hours:
                subject_hours[subject] = 0

            subject_hours[subject] += task["study_time"]

        if subject_hours:

            subject_data = {
                "Subject": list(
                    subject_hours.keys()
                ),
                "Study Hours": list(
                    subject_hours.values()
                )
            }

            st.bar_chart(
                subject_data,
                x="Subject",
                y="Study Hours"
            )

        st.divider()

        # ------------------------------------------
        # SUBJECT PROGRESS
        # ------------------------------------------

        st.subheader("📊 Subject-wise Progress")

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

        for subject, data in subjects.items():

            total = data["total"]

            completed = data["completed"]

            progress = completed / total

            st.write(
                f"**{subject}** — "
                f"{completed}/{total} completed "
                f"({progress * 100:.0f}%)"
            )

            st.progress(progress)

        st.divider()

        # ------------------------------------------
        # PRIORITY DISTRIBUTION
        # ------------------------------------------

        st.subheader("🔥 Priority Distribution")

        priority_counts = {
            "HIGH": 0,
            "MEDIUM": 0,
            "LOW": 0
        }

        for task in tasks:

            level = get_priority_level(
                task["priority_score"]
            )

            priority_counts[level] += 1

        priority_data = {
            "Priority": list(
                priority_counts.keys()
            ),
            "Tasks": list(
                priority_counts.values()
            )
        }

        st.bar_chart(
            priority_data,
            x="Priority",
            y="Tasks"
        )

        st.divider()

        # ------------------------------------------
        # DEADLINE RISK
        # ------------------------------------------

        st.subheader("⚠️ Deadline Risk")

        risky_tasks = []

        for task in tasks:

            if task.get("completed", False):
                continue

            if task["days_left"] <= 2:

                risky_tasks.append(task)

        if risky_tasks:

            st.warning(
                f"{len(risky_tasks)} task(s) have "
                f"deadlines within 2 days."
            )

            for task in risky_tasks:

                st.write(
                    f"⚠️ **{task['subject']}** — "
                    f"{task['topic']} | "
                    f"{task['days_left']} day(s) left | "
                    f"{task['study_time']}h"
                )

        else:

            st.success(
                "No immediate deadline risks detected."
            )

        st.divider()

        # ------------------------------------------
        # AI INSIGHT
        # ------------------------------------------

        st.subheader("🤖 Academic Insight")

        if high_priority > 0:

            st.info(
                f"You currently have **{high_priority} "
                f"high-priority pending task(s)**. "
                f"Consider addressing these before "
                f"lower-priority work."
            )

        elif pending_tasks > 0:

            st.info(
                "Your workload currently contains "
                "no high-priority pending tasks."
            )

        else:

            st.success(
                "🎉 All tasks are completed!"
            )


# ==================================================
# ADD TASK
# ==================================================

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


# ==================================================
# STUDY PLANNER
# ==================================================

elif menu == "📅 Study Planner":

    st.header("📅 AI Personalized Study Planner")

    st.write(
        "Tell CampusAssist AI how much time "
        "you have today."
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

                st.subheader(
                    "📋 Your Study Plan"
                )

                st.write(study_plan)

            except Exception as e:

                st.error(
                    "Unable to generate study plan."
                )

                st.caption(str(e))


# ==================================================
# AI EXPLAINER
# ==================================================

elif menu == "🤖 AI Explainer":

    st.header("🤖 AI Topic Explainer")

    st.write(
        "Ask CampusAssist AI to explain "
        "an academic topic."
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


# ==================================================
# AI RECOMMENDATIONS
# ==================================================

elif menu == "💡 AI Recommendations":

    st.header("💡 AI Study Recommendations")

    st.write(
        "CampusAssist AI analyzes your pending "
        "workload and provides personalized recommendations."
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


# ==================================================
# QUICK REVISION
# ==================================================

elif menu == "📝 Quick Revision":

    st.header("📝 AI Quick Revision")

    st.write(
        "Generate a 5-minute revision sheet "
        "for any academic topic."
    )

    revision_topic = st.text_input(
        "📖 Enter Topic",
        placeholder="e.g. Kirchhoff's Laws"
    )

    if st.button(
        "🧠 Generate Revision Sheet",
        use_container_width=True
    ):

        if not revision_topic:

            st.warning(
                "Please enter a topic first."
            )

        else:

            with st.spinner(
                "🧠 Creating your revision sheet..."
            ):

                try:

                    revision = generate_revision(
                        revision_topic
                    )

                    st.subheader(
                        f"📚 {revision_topic} — Quick Revision"
                    )

                    st.write(revision)

                except Exception as e:

                    st.error(
                        "Unable to generate revision sheet."
                    )

                    st.caption(str(e))


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "🎓 CampusAssist AI | "
    "Built with Python, Streamlit, SQLite & AI"
)