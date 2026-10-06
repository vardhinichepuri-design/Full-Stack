import streamlit as st
import ollama


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Age Adaptive AI",
    page_icon="🧠",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #666666;
    margin-bottom: 25px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# TITLE
# ============================================================

st.markdown(
    '<div class="main-title">🧠 Age-Adaptive AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Understand the same concept according to your age'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Settings")

    model = st.selectbox(
        "Choose Ollama Model",
        [
            "llama3.2",
            "gemma3"
        ]
    )

    st.info(
        "This project uses Ollama to run the AI model locally."
    )

    st.divider()

    st.subheader("📌 Age-Based Modes")

    st.write("📖 5–11 → Story Mode")
    st.write("🎯 12–20 → Three Ways")
    st.write("💡 21–35 → Practical Mode")
    st.write("🌍 36–75 → Real-Time Mode")


# ============================================================
# USER INFORMATION
# ============================================================

st.subheader("👤 User Information")

age = st.number_input(
    "Enter your age",
    min_value=5,
    max_value=75,
    value=20,
    step=1
)

st.caption(
    "Age range: 5–75 years"
)


# ============================================================
# SHOW CURRENT AGE MODE
# ============================================================

if 5 <= age <= 11:

    st.info(
        "📖 Story Mode: The concept will be explained as a simple story."
    )

elif 12 <= age <= 20:

    st.info(
        "🎯 Three-Way Mode: You will get three different explanations."
    )

elif 21 <= age <= 35:

    st.info(
        "💡 Practical Mode: The explanation will focus more on practical uses."
    )

else:

    st.info(
        "🌍 Real-Time Mode: The explanation will focus on real-world "
        "and practical situations."
    )


# ============================================================
# QUESTION INPUT
# ============================================================

st.subheader("💬 Enter Your Question")

question = st.text_area(
    "What do you want to understand?",
    placeholder="Example: What is Artificial Intelligence?",
    height=130
)


# ============================================================
# CREATE AGE-BASED AI PROMPT
# ============================================================

def create_prompt(age, question):

    # --------------------------------------------------------
    # AGE 5–11
    # --------------------------------------------------------

    if 5 <= age <= 11:

        prompt = f"""
You are an educational AI assistant for a young child.

The user is {age} years old.

The user's question is:

{question}

Explain the concept as a FUN AND SIMPLE STORY.

Rules:

- Explain it like a story for a young child.
- Use very simple English.
- Use short sentences.
- Use familiar characters.
- You can use a child, teacher, animal, superhero,
  family member, or imaginary character.
- Make the story interesting and easy to follow.
- Connect the story directly to the actual concept.
- Use simple examples from school, home, toys, games,
  friends, or everyday life.
- Avoid difficult technical words.
- If a technical word is necessary, explain it simply.
- Make the concept easy to remember.

IMPORTANT:

Return ONLY the story.

Do not use JSON.
Do not use a code block.
Do not add a technical explanation before or after the story.
"""

    # --------------------------------------------------------
    # AGE 12–20
    # --------------------------------------------------------

    elif 12 <= age <= 20:

        prompt = f"""
You are an educational AI assistant.

The user is {age} years old.

The user's question is:

{question}

Explain the SAME concept in exactly THREE different ways.

==================================================
1. SIMPLE EXPLANATION
==================================================

Explain the concept in simple language suitable for
a school or college student.

Rules:

- Use clear English.
- Explain the basic meaning first.
- Avoid unnecessary difficult words.
- Give a simple example.

==================================================
2. ANALOGY EXPLANATION
==================================================

Explain the SAME concept using a familiar real-world analogy.

Rules:

- Use an easy real-life situation.
- Clearly connect the analogy to the actual concept.
- Make it easy to remember.

==================================================
3. STUDENT EXPLANATION
==================================================

Explain the SAME concept at a moderate technical level.

Rules:

- Use correct technical terms.
- Explain how it works.
- Give a relevant example.
- Keep it understandable for a student.
- Do not make it unnecessarily advanced.

IMPORTANT:

Return EXACTLY these headings:

SIMPLE:
ANALOGY:
STUDENT:

Do not use JSON.
Do not use a code block.
Do not add anything before SIMPLE.
Do not add anything after STUDENT.
"""

    # --------------------------------------------------------
    # AGE 21–35
    # --------------------------------------------------------

    elif 21 <= age <= 35:

        prompt = f"""
You are an educational AI assistant.

The user is {age} years old.

The user's question is:

{question}

Explain the concept mainly from a PRACTICAL perspective.

Rules:

- Start with a clear definition.
- Focus more on practical understanding than theory.
- Explain where the concept is used in real life.
- Give realistic practical examples.
- Explain how a person can encounter or use this concept.
- Include workplace, technology, business, or daily-life
  examples when relevant.
- Explain the practical importance.
- Mention advantages when relevant.
- Use moderate technical terminology where useful.
- Keep the explanation clear and useful.

IMPORTANT:

Use EXACTLY these headings:

WHAT IT IS:
PRACTICAL EXAMPLE:
REAL-WORLD USE:
WHY IT MATTERS:

Do not use JSON.
Do not use a code block.
"""

    # --------------------------------------------------------
    # AGE 36–75
    # --------------------------------------------------------

    else:

        prompt = f"""
You are an educational AI assistant.

The user is {age} years old.

The user's question is:

{question}

Explain the concept using REAL-TIME and PRACTICAL
real-world situations.

Rules:

- Start with a clear explanation of the concept.
- Focus strongly on real-world applications.
- Explain how this concept is used in everyday life.
- Explain how it is used in work or business when relevant.
- Give realistic practical examples.
- Explain situations where the user may actually encounter
  this concept.
- Explain benefits and importance.
- Avoid unnecessary academic theory.
- Use professional but easy-to-understand language.
- Use technical terminology only when it helps understanding.

IMPORTANT:

Use EXACTLY these headings:

CONCEPT:
REAL-TIME EXAMPLE:
PRACTICAL APPLICATION:
BENEFITS:
REAL-WORLD IMPORTANCE:

Do not use JSON.
Do not use a code block.
"""

    return prompt


# ============================================================
# GENERATE AI RESPONSE
# ============================================================

def generate_answer(age, question, model):

    prompt = create_prompt(
        age,
        question
    )

    response = ollama.chat(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


# ============================================================
# GENERATE BUTTON
# ============================================================

if st.button(
    "✨ Generate Explanation",
    use_container_width=True
):

    if question.strip() == "":

        st.warning(
            "⚠️ Please enter a question."
        )

    else:

        try:

            with st.spinner(
                "🤖 AI is preparing your age-based explanation..."
            ):

                result = generate_answer(
                    age,
                    question,
                    model
                )

            # Store response

            st.session_state["answer"] = result
            st.session_state["question"] = question
            st.session_state["age"] = age

        except Exception as e:

            st.error(
                "❌ Unable to connect to Ollama."
            )

            st.write(
                "Please make sure Ollama is running "
                "and the selected model is installed."
            )

            st.code(
                str(e)
            )


# ============================================================
# DISPLAY AI RESPONSE
# ============================================================

if "answer" in st.session_state:

    st.divider()

    st.subheader(
        "🤖 AI Explanation"
    )

    current_age = st.session_state["age"]
    answer = st.session_state["answer"]


    # ========================================================
    # AGE 5–11
    # ========================================================

    if 5 <= current_age <= 11:

        st.markdown(
            "### 📖 Story Explanation"
        )

        st.info(
            answer
        )


    # ========================================================
    # AGE 12–20
    # ========================================================

    elif 12 <= current_age <= 20:

        st.markdown(
            "### 🎯 Three Different Ways"
        )

        # Find SIMPLE section

        simple = ""
        analogy = ""
        student = ""

        if "ANALOGY:" in answer:

            parts = answer.split(
                "ANALOGY:",
                1
            )

            simple = parts[0]

            remaining = parts[1]

        else:

            simple = answer
            remaining = ""


        if "STUDENT:" in remaining:

            parts = remaining.split(
                "STUDENT:",
                1
            )

            analogy = parts[0]
            student = parts[1]

        else:

            analogy = remaining
            student = ""


        simple = simple.replace(
            "SIMPLE:",
            ""
        ).strip()

        analogy = analogy.strip()
        student = student.strip()


        st.markdown(
            "### 🟢 Simple Explanation"
        )

        st.info(
            simple
        )


        st.markdown(
            "### 🟡 Analogy Explanation"
        )

        st.warning(
            analogy
        )


        st.markdown(
            "### 🔵 Student Explanation"
        )

        st.success(
            student
        )


    # ========================================================
    # AGE 21–35
    # ========================================================

    elif 21 <= current_age <= 35:

        st.markdown(
            "### 💡 Practical Explanation"
        )

        st.info(
            answer
        )


    # ========================================================
    # AGE 36–75
    # ========================================================

    else:

        st.markdown(
            "### 🌍 Real-Time & Practical Explanation"
        )

        st.success(
            answer
        )


    # ========================================================
    # DOWNLOAD ANSWER
    # ========================================================

    st.divider()

    download_text = f"""
AGE-ADAPTIVE AI
================

Age: {st.session_state["age"]}

Question:
{st.session_state["question"]}


==================================================
AI EXPLANATION
==================================================

{st.session_state["answer"]}
"""


    st.download_button(
        label="📥 Download Answer",
        data=download_text,
        file_name="age_adaptive_ai_answer.txt",
        mime="text/plain",
        use_container_width=True
    )


# ============================================================
# EXAMPLE QUESTIONS
# ============================================================

st.divider()

with st.expander("💡 Example Questions"):

    st.write(
        "• What is Artificial Intelligence?"
    )

    st.write(
        "• What is Machine Learning?"
    )

    st.write(
        "• What is Cloud Computing?"
    )

    st.write(
        "• What is Blockchain?"
    )

    st.write(
        "• What is a Database?"
    )

    st.write(
        "• What is Cyber Security?"
    )

    st.write(
        "• What is the Internet?"
    )

    st.write(
        "• What is Quantum Computing?"
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🧠 Age-Adaptive AI | Python + Streamlit + Ollama"
)