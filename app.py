import streamlit as st
import pandas as pd
import os
import json

from dotenv import load_dotenv
from google import genai

from coordinator_agent import coordinator
from performance_agent import analyze_student
from assignment_agent import check_assignments


# =========================================================
# PAGE
# =========================================================

st.set_page_config(
    page_title="Multi-Agent Student Assistant",
    page_icon="🎓",
    layout="wide"
)


# =========================================================
# AI
# =========================================================

load_dotenv(override=True)

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background: #f5f7fb;
}

.block-container {
    max-width: 1350px;
    padding-top: 30px;
}

section[data-testid="stSidebar"] {
    background: #101a45;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

.sidebar-title {
    font-size: 22px;
    font-weight: 800;
}

.sidebar-subtitle {
    font-size: 12px;
    opacity: 0.7;
}

.profile {
    background: rgba(255,255,255,0.10);
    padding: 18px;
    border-radius: 15px;
    text-align: center;
    margin-top: 25px;
    margin-bottom: 25px;
}

.title {
    font-size: 36px;
    font-weight: 800;
    color: #111827;
}

.subtitle {
    color: #64748b;
    font-size: 16px;
    margin-bottom: 25px;
}

.card {
    background: white;
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #e5e7eb;
    margin-bottom: 20px;
}

.card-title {
    font-size: 20px;
    font-weight: 700;
    color: #111827;
}

.card-text {
    color: #64748b;
    font-size: 14px;
}

.ai {
    background: #f0f5ff;
    border-left: 5px solid #2563eb;
    padding: 18px;
    border-radius: 10px;
    margin-top: 15px;
}

.stButton > button {
    background: linear-gradient(90deg, #2563eb, #4f46e5);
    color: white !important;
    border: none;
    border-radius: 10px;
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================

data = pd.read_csv("data/students.csv")


# =========================================================
# LOGIN
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


if not st.session_state.logged_in:

    st.markdown(
        "<div class='title' style='text-align:center;'>🎓 Multi-Agent Student Assistant</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='subtitle' style='text-align:center;'>Your Personalized AI Academic Assistant</div>",
        unsafe_allow_html=True
    )

    _, center, _ = st.columns([1, 1.2, 1])

    with center:

        st.markdown("""
        <div class="card">
            <div class="card-title">🔐 Student Login</div>
            <div class="card-text">
                Sign in to access your academic dashboard.
            </div>
        </div>
        """, unsafe_allow_html=True)

        student_id = st.text_input(
            "Student ID",
            placeholder="Example: ST001"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("🚀 Login", use_container_width=True):

            student = data[
                (data["Student_ID"].astype(str) == student_id) &
                (data["Password"].astype(str) == password)
            ]

            if not student.empty:

                st.session_state.logged_in = True
                st.session_state.student_id = student_id
                st.rerun()

            else:
                st.error("❌ Invalid Student ID or Password")

    st.stop()


# =========================================================
# STUDENT
# =========================================================

student_data = data[
    data["Student_ID"].astype(str)
    == str(st.session_state.student_id)
].iloc[0]

student_name = student_data["Name"]


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">🎓 Multi-Agent</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-subtitle">STUDENT ASSISTANT</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="profile">
            <h3>👤 {student_name}</h3>
            <p>Student ID: {st.session_state.student_id}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("📊 Dashboard")
    st.write("📈 Academic Performance")
    st.write("📅 Study Planner")
    st.write("🎯 Exam Practice")
    st.write("📚 Study Help")
    st.write("📝 Assignments")

    st.divider()

    if st.button("🚪 Logout", use_container_width=True):

        st.session_state.logged_in = False
        del st.session_state.student_id
        st.rerun()


# =========================================================
# DASHBOARD HEADER
# =========================================================

st.markdown(
    f"<div class='title'>Welcome back, {student_name}! 👋</div>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
        Here's your academic overview for today.
        Your AI assistant is ready to help you learn.
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# DASHBOARD METRICS
# =========================================================

subjects = {
    "Python": student_data["Python"],
    "DBMS": student_data["DBMS"],
    "AI": student_data["AI"],
    "Data Mining": student_data["Data_Mining"]
}

average = sum(subjects.values()) / len(subjects)

weak = [
    subject
    for subject, marks in subjects.items()
    if marks < 60
]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("📈 Average Marks", f"{average:.1f}%")

with col2:
    st.metric("📅 Attendance", f"{student_data['Attendance']}%")

with col3:
    st.metric("⚠️ Subjects to Improve", len(weak))


# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "📊 Performance",
        "📅 Study Planner",
        "📚 Study Help",
        "📝 Assignments",
        "🎯 Exam Practice"
    ]
)


# =========================================================
# TAB 1 - PERFORMANCE
# =========================================================

with tab1:

    st.markdown("""
    <div class="card">
        <div class="card-title">📊 Academic Performance</div>
        <div class="card-text">
            View your subject-wise marks and AI performance analysis.
        </div>
    </div>
    """, unsafe_allow_html=True)

    chart_data = pd.DataFrame(
        {
            "Subject": list(subjects.keys()),
            "Marks": list(subjects.values())
        }
    )

    st.bar_chart(
        chart_data.set_index("Subject")
    )

    if st.button(
        "🤖 Analyze My Performance",
        key="performance_button"
    ):

        try:

            weak_data, analysis = analyze_student(
                student_name
            )

            st.markdown(
                f"<div class='ai'>{analysis}</div>",
                unsafe_allow_html=True
            )

        except Exception as e:

            st.error(f"Unable to analyze: {e}")


# =========================================================
# TAB 2 - STUDY PLANNER
# =========================================================

with tab2:

    st.markdown("""
    <div class="card">
        <div class="card-title">📅 Study Planner</div>
        <div class="card-text">
            Create a personalized study plan using AI.
        </div>
    </div>
    """, unsafe_allow_html=True)

    days = st.selectbox(
        "Study Plan",
        ["1 Week", "2 Weeks", "1 Month"]
    )

    if st.button(
        "✨ Generate Study Plan",
        key="planner_button"
    ):

        try:

            result = coordinator(
                f"Create a {days} study plan for me.",
                student_name
            )

            st.markdown(
                f"<div class='ai'>{result}</div>",
                unsafe_allow_html=True
            )

        except Exception as e:

            st.error(f"Unable to create plan: {e}")


# =========================================================
# TAB 3 - STUDY HELP
# =========================================================

with tab3:

    st.markdown("""
    <div class="card">
        <div class="card-title">📚 AI Study Help</div>
        <div class="card-text">
            Ask about any subject or topic.
        </div>
    </div>
    """, unsafe_allow_html=True)

    topic = st.text_input(
        "Enter Subject or Topic",
        placeholder="Mathematics, Science, DBMS, Python, Physics..."
    )

    if st.button(
        "💡 Explain",
        key="study_help_button"
    ):

        if topic.strip():

            try:

                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=f"""
You are an academic tutor.

Explain this topic to a college student:

{topic}

Give:
1. Simple explanation
2. Important points
3. Example
4. Exam preparation points
"""
                )

                st.markdown(
                    f"<div class='ai'>{response.text}</div>",
                    unsafe_allow_html=True
                )

            except Exception as e:

                st.error(f"Unable to answer: {e}")

        else:

            st.warning("Please enter a subject or topic.")


# =========================================================
# TAB 4 - ASSIGNMENTS
# =========================================================

with tab4:

    st.markdown("""
    <div class="card">
        <div class="card-title">📝 Assignment Assistant</div>
        <div class="card-text">
            Check your assignment deadlines.
        </div>
    </div>
    """, unsafe_allow_html=True)

    assignments = [
        {
            "subject": "Python",
            "deadline": "2026-09-10"
        },
        {
            "subject": "DBMS",
            "deadline": "2026-09-15"
        },
        {
            "subject": "AI",
            "deadline": "2026-09-20"
        }
    ]

    st.dataframe(
        pd.DataFrame(assignments),
        use_container_width=True
    )

    if st.button(
        "🔎 Check Assignments",
        key="assignment_button"
    ):

        try:

            result = check_assignments(assignments)

            st.markdown(
                f"<div class='ai'>{result}</div>",
                unsafe_allow_html=True
            )

        except Exception as e:

            st.error(f"Unable to check assignments: {e}")


# =========================================================
# TAB 5 - EXAM PRACTICE
# =========================================================

with tab5:

    st.markdown("""
    <div class="card">
        <div class="card-title">🎯 Exam Practice</div>
        <div class="card-text">
            Generate practice questions for ANY subject.
        </div>
    </div>
    """, unsafe_allow_html=True)

    subject = st.text_input(
        "📚 Enter Subject",
        placeholder="DBMS, Python, Mathematics, Science, Physics...",
        key="exam_subject"
    )

    difficulty = st.selectbox(
        "🎚️ Difficulty",
        ["Easy", "Medium", "Hard"],
        key="exam_difficulty"
    )

    number = st.selectbox(
        "🔢 Number of Questions",
        [5, 10, 15],
        key="exam_number"
    )


    # GENERATE

    if st.button(
        "🚀 Generate Test",
        key="generate_exam"
    ):

        if subject.strip():

            prompt = f"""
Create exactly {number} multiple-choice questions
for a college student.

Subject: {subject}
Difficulty: {difficulty}

Return ONLY valid JSON.

Format:

[
{{
"question": "Question",
"options": {{
"A": "Option A",
"B": "Option B",
"C": "Option C",
"D": "Option D"
}},
"answer": "A",
"explanation": "Short explanation"
}}
]

Do not add markdown.
Do not add ```json.
Do not add any text outside JSON.
"""

            try:

                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt
                )

                text = response.text.strip()

                text = text.replace(
                    "```json", ""
                )

                text = text.replace(
                    "```", ""
                )

                questions = json.loads(
                    text.strip()
                )

                st.session_state.exam_questions = questions
                st.session_state.exam_subject = subject
                st.session_state.exam_submitted = False

                for i in range(20):

                    key = f"exam_answer_{i}"

                    if key in st.session_state:
                        del st.session_state[key]

                st.rerun()

            except Exception as e:

                st.error(
                    f"❌ Unable to generate test: {e}"
                )

        else:

            st.warning(
                "⚠️ Please enter a subject."
            )


    # QUESTIONS

    if "exam_questions" in st.session_state:

        questions = st.session_state.exam_questions

        st.divider()

        st.subheader(
            f"📝 {st.session_state.exam_subject} Practice Test"
        )

        st.info(
            "Select your answers and submit the test."
        )

        for i, q in enumerate(questions):

            st.markdown(
                f"### Question {i + 1}"
            )

            st.write(
                q["question"]
            )

            options = [
                f"A. {q['options']['A']}",
                f"B. {q['options']['B']}",
                f"C. {q['options']['C']}",
                f"D. {q['options']['D']}"
            ]

            st.radio(
                "Choose answer:",
                options,
                key=f"exam_answer_{i}",
                index=None
            )


        # SUBMIT

        if st.button(
            "✅ Submit Test",
            key="submit_exam"
        ):

            score = 0

            for i, q in enumerate(questions):

                selected = st.session_state.get(
                    f"exam_answer_{i}"
                )

                if selected:

                    letter = selected[0]

                    if letter == q["answer"]:
                        score += 1

            st.session_state.exam_score = score
            st.session_state.exam_submitted = True

            st.rerun()


    # RESULTS

    if st.session_state.get(
        "exam_submitted",
        False
    ):

        questions = st.session_state.exam_questions

        score = st.session_state.exam_score

        total = len(questions)

        percentage = (
            score / total
        ) * 100

        st.divider()

        st.header("🏆 Exam Results")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "🎯 Score",
                f"{score}/{total}"
            )

        with c2:
            st.metric(
                "📊 Percentage",
                f"{percentage:.1f}%"
            )

        with c3:

            if percentage >= 80:
                result = "Excellent 🌟"

            elif percentage >= 60:
                result = "Good 👍"

            else:
                result = "Needs Practice 📚"

            st.metric(
                "Performance",
                result
            )

        st.subheader(
            "📖 Answer Review"
        )

        for i, q in enumerate(questions):

            selected = st.session_state.get(
                f"exam_answer_{i}"
            )

            if selected:
                selected_letter = selected[0]
            else:
                selected_letter = "Not Answered"

            st.markdown(
                f"### Question {i + 1}"
            )

            st.write(
                q["question"]
            )

            if selected_letter == q["answer"]:

                st.success(
                    f"✅ Correct! Your answer: {selected_letter}"
                )

            else:

                st.error(
                    f"❌ Your answer: {selected_letter}"
                )

                st.info(
                    f"Correct Answer: {q['answer']}"
                )

            st.write(
                f"💡 Explanation: {q['explanation']}"
            )


# =========================================================
# GENERAL AI ASSISTANT
# =========================================================

st.divider()

st.subheader(
    "💬 Ask Your Student Assistant"
)

question = st.text_input(
    "Your question",
    placeholder="Ask anything about your studies..."
)

if st.button(
    "🤖 Ask Assistant",
    key="general_ai"
):

    if question.strip():

        try:

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=f"""
You are a helpful college Student Assistant.

Student: {student_name}

Answer this question clearly and simply:

{question}
"""
            )

            st.markdown(
                f"<div class='ai'>{response.text}</div>",
                unsafe_allow_html=True
            )

        except Exception as e:

            st.error(
                f"Unable to answer: {e}"
            )

    else:

        st.warning(
            "Please enter your question."
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div style="text-align:center;color:#64748b;margin-top:40px;">
        🎓 Multi-Agent Student Assistant • Powered by AI
    </div>
    """,
    unsafe_allow_html=True
)