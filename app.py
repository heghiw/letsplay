import streamlit as st
import pandas as pd
from urllib.parse import urlencode

# Session state initialization
if "round" not in st.session_state:
    st.session_state.round = 1
if "prompt_submitted" not in st.session_state:
    st.session_state.prompt_submitted = False
if "session_id" not in st.session_state:
    st.session_state.session_id = "abc123"
if "player_name" not in st.session_state:
    st.session_state.player_name = ""
if "scores" not in st.session_state:
    st.session_state.scores = []

# --------- Sidebar ---------
with st.sidebar:
    st.title("🔧 Game Settings")
    st.session_state.player_name = st.text_input("👤 Player Name", st.session_state.player_name)
    st.write("🆔 Session ID:")
    st.code(st.session_state.session_id)
    share_url = f"?session={st.session_state.session_id}"
    st.markdown(f"🔗 Shareable link: `{share_url}`")

    with st.expander("📖 How to Play", expanded=False):
        st.markdown("""
        1. Enter a prompt to solve the challenge.
        2. The model will generate an output.
        3. You’ll receive a score based on precision and token usage.
        4. Highest score wins after 5 rounds!
        """)

# --------- Main Area ---------
st.title("🚀 Prompt Challenge Game")
st.markdown(f"### 🎮 Round {st.session_state.round} of 5")

# --- Challenge Display ---
challenge_text = f"Write a prompt to generate a poem about space exploration."
st.markdown("#### 🧩 Current Challenge")
st.info(challenge_text)

# --- Prompt Input ---
if not st.session_state.prompt_submitted:
    user_prompt = st.text_area("✍️ Enter your prompt here:", height=150)
    if st.button("✅ Submit Prompt"):
        # Simulated scoring and response (replace with your logic)
        model_output = f"Poem about space generated using: '{user_prompt}'"
        match_score = 85
        token_penalty = -10
        final_score = match_score + token_penalty

        st.session_state.prompt_submitted = True
        st.session_state.current_output = model_output
        st.session_state.current_score = {
            "round": st.session_state.round,
            "player": st.session_state.player_name,
            "prompt": user_prompt,
            "output": model_output,
            "match_score": match_score,
            "token_penalty": token_penalty,
            "final_score": final_score
        }
        st.session_state.scores.append(st.session_state.current_score)
else:
    score = st.session_state.current_score
    st.subheader("🤖 Model Output")
    st.code(score["output"])

    st.subheader("📊 Scoring Breakdown")
    col1, col2, col3 = st.columns(3)
    col1.metric("Match Score", f"{score['match_score']}%")
    col2.metric("Token Penalty", f"{score['token_penalty']}")
    col3.metric("Final Score", f"{score['final_score']}")

    # Dynamic feedback
    if score["final_score"] >= 80:
        st.success("🔥 Great prompt!")
    elif score["final_score"] >= 60:
        st.warning("👍 Decent! Try to optimize further.")
    else:
        st.error("😬 Needs improvement.")

    if st.button("➡️ Next Round"):
        st.session_state.round += 1
        st.session_state.prompt_submitted = False

# --- Final Scoreboard ---
if st.session_state.round > 5:
    st.balloons()
    st.title("🏁 Game Over")
    st.header("📈 Final Scoreboard")

    df = pd.DataFrame(st.session_state.scores)
    st.dataframe(df.style.highlight_max(axis=0, subset=["final_score"], color="lightgreen"))

    top_player = df.loc[df["final_score"].idxmax(), "player"]
    st.success(f"🏆 Top Player: **{top_player}**")

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Results as CSV", csv, "results.csv", "text/csv")

# --- Optional Enhancements ---
if st.session_state.prompt_submitted and st.session_state.round <= 5:
    # Countdown timer placeholder (implement with JavaScript for real-time)
    st.markdown("⏱️ _Time remaining: (feature not implemented)_")

    # Score color coding could be integrated via CSS or `st.markdown`
    st.progress(st.session_state.round / 5)

# --- Responsive Design & UX tweaks ---
st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    textarea {
        font-size: 16px !important;
    }
</style>
""", unsafe_allow_html=True)

