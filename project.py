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

.answer-title {
    font-size: 25px;
    font-weight: bold;
    margin-top: 20px;
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
    'Understand the same concept in three different ways'
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

    st.subheader("📌 Answer Modes")

    st.write("🟢 Beginner Explanation")
    st.write("🟡 Analogy Explanation")
    st.write("🔵 Technical Explanation")


# ============================================================
# AGE INPUT
# ============================================================

st.subheader("👤 User Information")

age = st.number_input(
    "Enter your age",
    min_value=16,
    max_value=75,
    value=20,
    step=1
)

st.caption(
    "Age range: 16–75 years"
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
# CREATE AI PROMPT
# ============================================================

def create_prompt(age, question):

    prompt = f"""
You are an educational AI assistant.

The user is {age} years old.

The user's question is:

{question}

Your task is to explain the SAME concept in exactly THREE
different ways.

The three explanations must discuss the SAME concept.

========================================
1. BEGINNER EXPLANATION
========================================

Explain the concept for a complete beginner.

Rules:
- Use very simple English.
- Use short and clear sentences.
- Avoid difficult technical words.
- Explain the basic meaning first.
- Make it easy for someone with no background knowledge.
- Give a simple example if useful.

========================================
2. ANALOGY EXPLANATION
========================================

Explain the SAME concept using a real-world analogy.

Rules:
- Use a familiar real-life situation.
- Make the analogy easy to understand.
- Clearly connect the analogy to the actual concept.
- Do not use an unrelated example.
- The analogy should help the user remember the concept.

========================================
3. TECHNICAL EXPLANATION
========================================

Explain the SAME concept at a technical level.

Rules:
- Use correct technical terminology.
- Explain how it works.
- Explain important components or mechanisms.
- Give a technical example when appropriate.
- Provide enough detail for a college student.

========================================

IMPORTANT:

Return the answer using EXACTLY these headings:

BEGINNER:
ANALOGY:
TECHNICAL:

Do NOT use JSON.

Do NOT put the answer inside a code block.

Do NOT add any explanation before BEGINNER.

Do NOT add any explanation after TECHNICAL.

The three sections must be clearly separated.
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
# SPLIT AI RESPONSE INTO THREE SECTIONS
# ============================================================

def split_answers(result):

    beginner = ""
    analogy = ""
    technical = ""

    # Find sections

    if "ANALOGY:" in result:

        parts = result.split(
            "ANALOGY:",
            1
        )

        beginner = parts[0]

        remaining = parts[1]

    else:

        beginner = result
        remaining = ""


    if "TECHNICAL:" in remaining:

        parts = remaining.split(
            "TECHNICAL:",
            1
        )

        analogy = parts[0]
        technical = parts[1]

    else:

        analogy = remaining
        technical = ""


    # Remove headings

    beginner = beginner.replace(
        "BEGINNER:",
        ""
    ).strip()

    analogy = analogy.strip()

    technical = technical.strip()


    return beginner, analogy, technical


# ============================================================
# GENERATE BUTTON
# ============================================================

if st.button(
    "✨ Generate 3 Explanations",
    use_container_width=True
):

    if question.strip() == "":

        st.warning(
            "⚠️ Please enter a question."
        )

    else:

        try:

            with st.spinner(
                "🤖 AI is preparing your three explanations..."
            ):

                result = generate_answer(
                    age,
                    question,
                    model
                )

            # Split response

            beginner, analogy, technical = split_answers(
                result
            )

            # Store answers

            st.session_state["beginner"] = beginner
            st.session_state["analogy"] = analogy
            st.session_state["technical"] = technical
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
# DISPLAY THREE ANSWERS
# ============================================================

if "beginner" in st.session_state:

    st.divider()

    st.subheader(
        "🤖 AI Explanations"
    )


    # ========================================================
    # BEGINNER
    # ========================================================

    st.markdown(
        "### 🟢 Beginner Explanation"
    )

    st.info(
        st.session_state["beginner"]
    )


    # ========================================================
    # ANALOGY
    # ========================================================

    st.markdown(
        "### 🟡 Analogy Explanation"
    )

    st.warning(
        st.session_state["analogy"]
    )


    # ========================================================
    # TECHNICAL
    # ========================================================

    st.markdown(
        "### 🔵 Technical Explanation"
    )

    st.success(
        st.session_state["technical"]
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
BEGINNER EXPLANATION
==================================================

{st.session_state["beginner"]}


==================================================
ANALOGY EXPLANATION
==================================================

{st.session_state["analogy"]}


==================================================
TECHNICAL EXPLANATION
==================================================

{st.session_state["technical"]}
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