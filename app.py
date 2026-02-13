# valentine.py
# Run with: streamlit run valentine.py

import base64
from pathlib import Path
import streamlit as st

# ============================================================
# 🔧 CUSTOMIZE HERE (PUT MEDIA FILES NEXT TO valentine.py)
# ============================================================
CONFIG = {
    "bf_name": "Shinchan",
    "from_name": "Doraemon 😌",
    "secret_code": "Karu",  # secret word to unlock

    "media": {
        "intro": "angry.gif",
        "intro_reaction_default": "angry2.gif",
        "intro_reaction_extra": "angry2.gif",

        "q1": "q1.jpeg",
        "q2": "q2.gif",
        "q3": "q3.gif",
        "q4": "q3.gif",
        "q5": "q5.jpeg",
        "q6": "q6.jpeg",
        "q7": "q7.gif",
        "q8": "q8.jpeg",

        "code": "lock.gif",
        "valentine": "final.jpeg",
    },

    "questions": [
        {
            "id": "q1",
            "mode": "quiz",
            "type": "text",
            "title": "Question 1",
            "question": "Some annoying and teasing incident on 13th Feb 2025 when you came for dinner for the first time at our home?",
            "accepted": ["Jaiko Gouda", "Holding hands for the first time"],
            "hint": "Hint: My name you saved in your phone😏",
        },
        {
            "id": "q2",
            "mode": "quiz",
            "type": "mcq",
            "title": "Question 2",
            "question": "On which date did we kiss for the first time?",
            "options": ["16 February", "14 February", "18 February", "20 February"],
            "correct_index": 0,
        },
        {
            "id": "q3",
            "mode": "quiz",
            "type": "text",
            "title": "Question 3",
            "question": "Which dish I served you with my hands for the first time?🍕",
            "accepted": ["Beetroot Cheela", "Beetroot besan Cheela"],
            "hint": "Hint: Some Cheela",
        },
        {
            "id": "q4",
            "mode": "note",
            "type": "text_any",
            "title": "Question 4",
            "question": "What do you think is our most special memory together? 💭",
            "cute_reply": "Aww 🥹 that’s such a beautiful memory… my heart is smiling 💖",
        },
        {
            "id": "q5",
            "mode": "quiz",
            "type": "mcq",
            "title": "Question 5",
            "question": "Among us, who gets more angry? 😤",
            "options": ["Kaushal", "Ruchika"],
            "correct_index": 0,
        },
        {
            "id": "q6",
            "mode": "quiz",
            "type": "mcq",
            "title": "Question 6",
            "question": "Who can’t stay without talking to each other? 🤭",
            "options": ["Me", "You", "Both"],
            "correct_index": 2,
        },
        {
            "id": "q7",
            "mode": "note",
            "type": "text_any",
            "title": "Question 7",
            "question": "Which city/country are you most excited to visit with me? ✈️",
            "cute_reply": "Okayyy travel partner unlocked 😌✈️ I’m already excited with you 💞",
        },
        {
            "id": "q8",
            "mode": "note",
            "type": "text_any",
            "title": "Question 8",
            "question": "What do you think about this picture?💞",
            "cute_reply": "STOPP 🫠💗 you’re making me blush… I love this moment with you 😭💘",
        },
    ],
}

INTRO_OPTIONS = [
    "We are not Kids anymore😅",
    "We are Hindus. We don't celebrate valentine day",
    "I’m guilty, I should have🙏",
    "I was about to ask you but you asked me first🙏",
]

# ============================================================
# Helpers
# ============================================================
def norm(s):
    return " ".join(str(s).strip().lower().split())

def accepted_match(ans, accepted):
    return norm(ans) in [norm(x) for x in accepted]

def init_state():
    if "step" not in st.session_state:
        st.session_state.step = "intro"
    if "answers" not in st.session_state:
        st.session_state.answers = {}
    if "intro_choice" not in st.session_state:
        st.session_state.intro_choice = None

    if "attempts" not in st.session_state:
        st.session_state.attempts = {}
    if "show_hint" not in st.session_state:
        st.session_state.show_hint = {}

    if "noted" not in st.session_state:
        st.session_state.noted = {}

    if "code_attempts" not in st.session_state:
        st.session_state.code_attempts = 0

def goto(step):
    st.session_state.step = step
    st.rerun()

def restart():
    st.session_state.clear()
    init_state()
    st.rerun()

def question_steps():
    return [f"q::{q['id']}" for q in CONFIG["questions"]]

def mime_for(path: Path) -> str:
    ext = path.suffix.lower()
    if ext == ".gif":
        return "image/gif"
    if ext in [".jpg", ".jpeg"]:
        return "image/jpeg"
    if ext == ".png":
        return "image/png"
    if ext == ".webp":
        return "image/webp"
    return "application/octet-stream"

def render_media(path_str: str, height_px: int = 420):
    """Bigger + clearer media with object-fit: contain."""
    if not path_str:
        st.empty()
        return
    p = Path(path_str)
    if not p.exists():
        st.info(f"Media not found: {path_str}\n\n(Place it next to valentine.py)")
        return

    b64 = base64.b64encode(p.read_bytes()).decode("utf-8")
    mime = mime_for(p)

    st.markdown(
        f"""
        <div style="
            width:100%;
            height:{height_px}px;
            border-radius:18px;
            overflow:hidden;
            background:#0b0b0b;
            box-shadow: 0 10px 25px rgba(0,0,0,0.18);
            display:flex;
            align-items:center;
            justify-content:center;
        ">
          <img
            src="data:{mime};base64,{b64}"
            style="
              width:100%;
              height:100%;
              object-fit:contain;
              display:block;
            "
          />
        </div>
        """,
        unsafe_allow_html=True,
    )

def layout_with_media(media_key: str, height_px: int = 420):
    # Wider media column for better clarity
    left, right = st.columns([1.25, 1.0], gap="large")
    with left:
        render_media(CONFIG["media"].get(media_key, ""), height_px=height_px)
    return left, right

def ensure_attempt_state(qid: str):
    if qid not in st.session_state.attempts:
        st.session_state.attempts[qid] = 0
    if qid not in st.session_state.show_hint:
        st.session_state.show_hint[qid] = False

def is_correct(q, ans) -> bool:
    if q.get("mode", "quiz") == "note":
        return True
    if q["type"] == "mcq":
        correct = q["options"][q["correct_index"]]
        return ans == correct
    return accepted_match(ans, q.get("accepted", []))

def big_reaction_symbol(symbol: str, label: str):
    st.markdown(
        f"""
        <div style="text-align:center; padding:10px 0 0 0;">
          <div style="font-size:78px; line-height:1;">{symbol}</div>
          <div style="font-size:22px; font-weight:800;">{label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# App setup
# ============================================================
init_state()
st.set_page_config(page_title="Valentine 💘", page_icon="💘", layout="centered")

st.markdown(
    """
    <style>
      .block-container {max-width: 980px; padding-top: 1.05rem;}
    </style>
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    st.subheader("💘 Valentine Game")
    if st.button("Restart 🔁"):
        restart()

st.title("💌 Mini Love Quest")

# ============================================================
# INTRO
# ============================================================
if st.session_state.step == "intro":
    _, right = layout_with_media("intro", height_px=420)

    with right:
        st.markdown("### 😤")
        st.write(f"Hi **{CONFIG['bf_name']}**.")
        st.write("So… it’s February.")
        st.write("And SOMEONE still hasn’t asked me to be their Valentine.")

        choice = st.radio("Explain yourself:", INTRO_OPTIONS, index=None, key="intro_choice_radio")

        if st.button("Continue ➜", disabled=choice is None, use_container_width=True):
            st.session_state.intro_choice = choice
            goto("intro_reaction")

# ============================================================
# INTRO REACTION
# ============================================================
elif st.session_state.step == "intro_reaction":
    choice = st.session_state.intro_choice or ""
    media_key = "intro_reaction_extra" if (choice == INTRO_OPTIONS[1]) else "intro_reaction_default"
    _, right = layout_with_media(media_key, height_px=420)

    with right:
        if choice == INTRO_OPTIONS[1]:
            st.markdown("### 😡 EXCUSE ME???")
            st.write("Nice try 😤")
            st.write("So you can celebrate *everything else* but not this? Hmm??")
            st.write("Okay. Now you have to pass the test with **FULL MARKS**. 😤")
        elif choice == INTRO_OPTIONS[0]:
            st.markdown("### 😏")
            st.write("Ohhh okay… big grown-up talk now?")
            st.write("So grown-up that you forgot to ask me? 🙂")
        else:
            st.markdown("### 😌")
            st.write("At least you admitted it 😌")
            st.write("Punishment reduced by 2% 😂")

        st.write("")
        st.write("Anyway… since you didn’t ask…")
        st.write("I made a small test.")
        st.write("Answer correctly to move ahead 😌")

        if st.button("Start the quiz 💘", use_container_width=True):
            goto(question_steps()[0])

# ============================================================
# QUESTIONS
# ============================================================
elif st.session_state.step.startswith("q::"):
    qid = st.session_state.step.split("q::")[1]
    q = next(x for x in CONFIG["questions"] if x["id"] == qid)
    ensure_attempt_state(qid)

    _, right = layout_with_media(qid, height_px=460)  # even bigger for questions

    with right:
        mode = q.get("mode", "quiz")

        st.markdown(f"### 🧠 {q['title']}")
        st.write(q["question"])

        if q["type"] == "mcq":
            ans = st.radio(
                "Choose one:",
                q["options"],
                index=(
                    q["options"].index(st.session_state.answers[qid])
                    if qid in st.session_state.answers and st.session_state.answers[qid] in q["options"]
                    else None
                ),
                key=f"radio_{qid}",
            )
        else:
            widget_key = f"text_{qid}"
            if widget_key not in st.session_state:
                st.session_state[widget_key] = st.session_state.answers.get(qid, "")
            ans = st.text_input("Your answer:", key=widget_key)

        st.session_state.answers[qid] = ans
        answered = ans is not None and str(ans).strip() != ""

        if answered:
            if mode == "note":
                reply = q.get("cute_reply", "Awww 🥹💖")
                big_reaction_symbol("🥹", "Awwww")
                st.success(reply)
                st.session_state.noted[qid] = str(ans).strip()
            else:
                ok_live = is_correct(q, ans)
                big_reaction_symbol("💖" if ok_live else "😡", "Correct!" if ok_live else "Wrong!")

        # hint for text quiz
        if mode == "quiz" and q["type"] != "mcq" and st.session_state.show_hint.get(qid, False) and q.get("hint"):
            st.info(q["hint"])

        steps = question_steps()
        i = steps.index(st.session_state.step)
        prev_step = "intro_reaction" if i == 0 else steps[i - 1]
        next_step = "code" if i == len(steps) - 1 else steps[i + 1]

        st.write("")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Back ⟵", use_container_width=True):
                goto(prev_step)

        with c2:
            if st.button("Next ➜", disabled=not answered, use_container_width=True):
                if mode == "note":
                    goto(next_step)

                if is_correct(q, st.session_state.answers.get(qid, "")):
                    goto(next_step)

                st.session_state.attempts[qid] += 1
                if q["type"] != "mcq" and st.session_state.attempts[qid] >= 2:
                    st.session_state.show_hint[qid] = True

                st.error("Nope 😡 Not correct. Try again.")
                st.rerun()

# ============================================================
# SECRET CODE (with hint after 2 attempts)
# ============================================================
elif st.session_state.step == "code":
    _, right = layout_with_media("code", height_px=460)

    with right:
        st.markdown("### 🔐 Final challenge")
        st.write("Type the secret code word.")

        code_key = "secret_code_input"
        if code_key not in st.session_state:
            st.session_state[code_key] = ""

        code = st.text_input("Secret word:", type="password", key=code_key)

        if st.session_state.code_attempts >= 2:
            st.info("Hint 💡: It’s literally our names together 👀 (Kaushal + Ruchika)")

        if st.button("Unlock 🔓", use_container_width=True):
            st.session_state.code_attempts += 1

            if norm(code) == norm(CONFIG["secret_code"]):
                st.success("Hehehe 💖 You know us too well.")
                goto("valentine")  # ✅ DIRECTLY to final page (no summary)

            elif st.session_state.code_attempts == 1:
                st.error("Wrong 😤 Try again.")
                st.write("Think romantic 😌")

            elif st.session_state.code_attempts == 2:
                st.error("Still wrong 😤")
                st.write("Okay fine… I’ll give you a hint above 👆")

            elif st.session_state.code_attempts >= 3:
                st.write("Okay okay… unlocked because you’re cute 🙄💖")
                goto("valentine")  # ✅ DIRECTLY to final page

# ============================================================
# FINAL
# ============================================================
elif st.session_state.step == "valentine":
    _, right = layout_with_media("valentine", height_px=460)

    with right:
        st.markdown("### 💘")
        answer = st.radio(
            "Will you be my Valentine?",
            ["YES ❤️", "YESSS 💞", "Of course 🥹", "I already am 😌"],
            index=None,
            key="valentine_answer",
        )

        if st.button("Submit 💌", disabled=answer is None, use_container_width=True):
            st.balloons()
            st.markdown("## Happy Valentine’s 🥰")
            st.caption(f"— {CONFIG['from_name']}")
            st.write(f"You chose: **{answer}**")

else:
    restart()
