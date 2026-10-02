# ==========================================
#       CAMPUSASSIST AI - VERSION 1
# ==========================================

# ---------- TASK DATA ----------

tasks = [
    {
        "subject": "Physics",
        "topic": "Current Electricity",
        "difficulty": 3,
        "importance": 3,
        "days_left": 2,
        "study_time": 2
    },
    {
        "subject": "Maths",
        "topic": "Quadratic Equations",
        "difficulty": 2,
        "importance": 3,
        "days_left": 5,
        "study_time": 2
    },
    {
        "subject": "Chemistry",
        "topic": "Thermodynamics",
        "difficulty": 2,
        "importance": 2,
        "days_left": 1,
        "study_time": 2
    },
    {
        "subject": "Python",
        "topic": "Functions",
        "difficulty": 1,
        "importance": 2,
        "days_left": 7,
        "study_time": 1
    }
]


# ---------- PRIORITY CALCULATION ----------

def calculate_priority(task):
    difficulty_score = task["difficulty"] * 2
    importance_score = task["importance"] * 3
    urgency_score = max(0, 7 - task["days_left"]) * 2

    return difficulty_score + importance_score + urgency_score


# ---------- PRIORITY LEVEL ----------

def get_priority_level(score):
    if score >= 25:
        return "HIGH"
    elif score >= 15:
        return "MEDIUM"
    else:
        return "LOW"


# ---------- CALCULATE SCORES ----------

for task in tasks:
    task["priority_score"] = calculate_priority(task)


# ---------- SORT TASKS ----------

tasks.sort(
    key=lambda task: task["priority_score"],
    reverse=True
)


# ---------- SHOW PRIORITY TASKS ----------

def show_priority_tasks():

    print("\n🔥 TODAY'S PRIORITY")
    print("-" * 50)

    for i, task in enumerate(tasks, start=1):

        level = get_priority_level(
            task["priority_score"]
        )

        print(
            f"{i}. {task['subject']} - "
            f"{task['topic']}"
        )

        print(
            f"   Priority Score: "
            f"{task['priority_score']}"
        )

        print(
            f"   Priority Level: "
            f"{level}"
        )

        print(
            f"   Deadline: "
            f"{task['days_left']} day(s)"
        )

        print(
            f"   Study Time: "
            f"{task['study_time']} hour(s)"
        )

        print()


# ---------- TOTAL STUDY TIME ----------

def calculate_total_time():

    total_time = 0

    for task in tasks:
        total_time += task["study_time"]

    return total_time


# ---------- CREATE STUDY PLAN ----------

def create_study_plan():

    try:
        available_hours = float(
            input(
                "\nHow many hours can you study today? "
            )
        )

    except ValueError:
        print("\n❌ Please enter a valid number.")
        return

    if available_hours <= 0:
        print("\n❌ Study time must be greater than 0.")
        return

    remaining_hours = available_hours

    print("\n📅 TODAY'S STUDY PLAN")
    print("-" * 50)

    for task in tasks:

        study_time = task["study_time"]

        if remaining_hours >= study_time:

            print(
                f"✅ {task['subject']} - "
                f"{task['topic']} "
                f"→ {study_time} hour(s)"
            )

            remaining_hours -= study_time

        else:

            print(
                f"⏳ {task['subject']} - "
                f"{task['topic']} "
                f"→ Continue later"
            )

    print(
        f"\nRemaining study time: "
        f"{remaining_hours:.1f} hour(s)"
    )


# ---------- MAIN MENU ----------

def main():

    while True:

        print("\n")
        print("=" * 50)
        print("          🎓 CAMPUSASSIST AI")
        print("=" * 50)

        print("\n1. View Priority Tasks")
        print("2. Create Today's Study Plan")
        print("3. View Total Study Time")
        print("4. Exit")

        choice = input(
            "\nEnter your choice: "
        )

        if choice == "1":

            show_priority_tasks()

        elif choice == "2":

            create_study_plan()

        elif choice == "3":

            total_time = calculate_total_time()

            print(
                f"\n⏱️ Total Study Time: "
                f"{total_time} hour(s)"
            )

        elif choice == "4":

            print(
                "\n🎓 Thank you for using "
                "CampusAssist AI!"
            )

            break

        else:

            print(
                "\n❌ Invalid choice. "
                "Please select 1, 2, 3, or 4."
            )


# ---------- START PROGRAM ----------

if __name__ == "__main__":
    main()