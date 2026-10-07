import streamlit as st
import pandas as pd
import plotly.express as px
import os
import json
import time

from dotenv import load_dotenv
from google import genai
from database import get_student

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
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
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


# ================= LOGIN =================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "student_data" not in st.session_state:
    st.session_state.student_data = None


if not st.session_state.logged_in or st.session_state.student_data is None:

    st.markdown("""
        <div style="
            max-width: 650px;
            margin: 80px auto 20px auto;
            text-align: center;
        ">
            <h1 style="font-size: 42px; margin-bottom: 10px;">
                🎓 Student Assistant
            </h1>

        </div>
    """, unsafe_allow_html=True)

    # Login box
    col1, col2, col3 = st.columns([1, 3, 1])

    with col2:

        st.markdown("""
            <div style="
                text-align: center;
                margin-bottom: 15px;
            ">
                <h2>🔐 Student Login</h2>
                <p style="color: #777;">
                    Enter your Student ID and password to continue
                </p>
            </div>
        """, unsafe_allow_html=True)

        student_id = st.text_input(
            "Student ID",
            placeholder="Example: ST001"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password"
        )

        if st.button(
            "🚀 Login",
            use_container_width=True
        ):

            student = get_student(student_id, password)

            if student is not None:

                st.session_state.logged_in = True
                st.session_state.student_id = student_id
                st.session_state.student_data = student

                st.rerun()

            else:
                st.error("❌ Invalid Student ID or Password")

    st.stop()


# ================= STUDENT DATA =================

student_data = st.session_state.student_data
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


## =========================================================
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

    # BAR CHART ONLY FOR ACADEMIC PERFORMANCE
    chart_data = pd.DataFrame(
        {
            "Subject": list(subjects.keys()),
            "Marks": list(subjects.values())
        }
    )

    fig = px.bar(
        chart_data,
        x="Subject",
        y="Marks",
        text="Marks"
    )

    fig.update_layout(
        height=300,
        yaxis=dict(range=[0, 100]),
        hovermode=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
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
        <div class="card-title">📅 Today's Study Planner</div>
        <div class="card-text">
            Personalized study plan based on your marks.
        </div>
    </div>
    """, unsafe_allow_html=True)

    hours = st.selectbox(
        "⏰ Study Hours Today",
        [3, 4, 5, 6, 7, 8]
    )

    if st.button("✨ Generate Today's Plan",
                 key="planner_button"):

        plan = sorted(
            subjects.items(),
            key=lambda x: x[1]
        )

        st.session_state.today_plan = plan

    # Show saved plan
    if "today_plan" in st.session_state:

        plan = st.session_state.today_plan

        st.success("✅ Today's Study Plan")

        for i, (subject, marks) in enumerate(plan):

            if marks < 50:
                duration = "1.5 hours"
                activity = "Learn concepts + practice"
            elif marks < 70:
                duration = "1 hour"
                activity = "Study + solve questions"
            else:
                duration = "30 minutes"
                activity = "Revision + practice"

            completed = st.checkbox(
                f"📚 {subject} — {duration}",
                key=f"completed_{i}"
            )

            st.caption(
                f"🎯 {activity} | Marks: {marks}%"
            )

        completed_count = sum(
            st.session_state.get(
                f"completed_{i}", False
            )
            for i in range(len(plan))
        )

        st.success(
            f"📊 Today's Progress: "
            f"{completed_count}/{len(plan)} tasks completed"
        )

        progress = completed_count / len(plan)

        st.progress(progress)

        if completed_count == len(plan):
            st.balloons()
            st.success("🎉 Great job! You completed today's plan!")
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
                if "503" in str(e):
                    st.warning("The AI assistant is temporarily busy. "
            "Please try again in a moment.")

        else:

            st.error(f"Unable to answer:{e}")


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

# ==============================
# GENERAL AI ASSISTANT
# ==============================
st.divider()

st.subheader("💬 Ask Your Student Assistant")

question = st.text_input(
    "Your question or topic",
    placeholder="Ask anything about your studies..."
)
# ==============================
# TEXT EXPLANATION
# ==============================

if st.button("💬 Ask Assistant", key="general_ai"):

    if question.strip():

        with st.spinner("AI is preparing your answer..."):

            for attempt in range(3):

                try:
                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=f"""
You are a helpful college Student Assistant.

Student: {student_name}

Question: {question}

Explain clearly using simple language.
Give examples wherever helpful.
Make the answer suitable for college students.
"""
                    )

                    if response.text:
                        st.markdown("### 📚 Answer")
                        st.markdown(response.text)

                    else:
                        st.warning("No response received. Please try again.")

                    break

                except Exception as e:

                    error = str(e).upper()

                    if "429" in error or "RESOURCE_EXHAUSTED" in error:

                        st.warning(
                            "Today's AI request limit has been reached. "
                            "Please try again later."
                        )
                        break

                    elif "503" in error or "UNAVAILABLE" in error:

                        st.error("Gemini returned a 503 error.")
                        st.code(str(e))
                        break

                    else:
                        st.error(
                            "Unable to answer your question. "
                            "Please check the API configuration."
                        )
                        break
    else:
        st.warning("Please enter a question first.")


# ==============================
# AI IMAGE GENERATION
# ==============================

st.divider()

st.subheader("🎨 AI Learning Visual")

st.write(
    "Generate an educational image to understand your topic visually."
)

if st.button("🎨 Generate Image", key="generate_image"):

    if question.strip():

        with st.spinner("Creating your educational image..."):

            try:
                image_response = client.models.generate_content(
                    model="gemini-3.1-flash-image",
                    contents=f"""
Create a clear, colorful educational illustration
for a college student about:

{question}

Make the image visually attractive,
easy to understand, and suitable for learning.
Use a clean educational infographic style.
"""
                )

                image_found = False

                for part in image_response.parts:

                    if part.inline_data is not None:

                        generated_image = part.as_image()

                        st.markdown("### 🖼️ Generated Learning Image")

                        st.image(
                            generated_image,
                            caption=f"AI-generated visual: {question}",
                            use_container_width=True
                        )

                        image_found = True
                        break

                if not image_found:
                    st.warning(
                        "No image was returned. Please try again."
                    )

            except Exception as e:
                st.error(
                    "Image generation is temporarily unavailable. "
                    "Please try again later."
                )

    else:
        st.warning("Please enter a topic first.")

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
