import streamlit as st
import pandas as pd
import json

# --- Load challenges ---
@st.cache_data
def load_challenges():
    with open("challenge.json", "r") as f:
        return json.load(f)

challenges = load_challenges()

# --- Session state ---
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

# --- Sidebar ---
with st.sidebar:
    st.title("🎮 Game Setup")
    st.session_state.player_name = st.text_input("👤 Player Name", st.session_state.player_name)
    st.write("🆔 Session ID:")
    st.code(st.session_state.session_id)
    share_url = f"?session={st.session_state.session_id}"
    st.markdown(f"🔗 Shareable link: `{share_url}`")

    with st.expander("📖 How to Play", expanded=False):
        st.markdown("""
        1. Enter a prompt to solve the challenge.
        2. The model will generate an output.
        3. You’ll be scored based on how closely the output matches the target.
        4. Highest score wins after 5 rounds!
        """)

# --- Main Area ---
st.title("🚀 Prompt Challenge Game")

current_round = st.session_state.round
max_rounds = len(challenges)

if current_round <= max_rounds:
    challenge = challenges[current_round - 1]
    challenge_text = challenge["task"]
    target_output = challenge["target"]

    st.markdown(f"### 🧩 Round {current_round} of {max_rounds}")
    st.markdown("#### 🔍 Challenge")
    st.info(challenge_text)

    # --- Prompt input ---
    if not st.session_state.prompt_submitted:
        user_prompt = st.text_area("✍️ Your Prompt:", height=150)

        if st.button("✅ Submit Prompt"):
            # --- Simulate model output (replace with real model call) ---
            model_output = target_output  # simulated as if model works perfectly

            # --- Simple scoring logic ---
            match_score = 100 if model_output.strip() == target_output.strip() else 0
            token_penalty = -len(model_output.strip().split())
            final_score = max(0, match_score + token_penalty)

            # --- Store score ---
            st.session_state.current_score = {
                "round": current_round,
                "player": st.session_state.player_name,
                "prompt": user_prompt,
                "output": model_output,
                "target": target_output,
                "match_score": match_score,
                "token_penalty": token_penalty,
                "final_score": final_score
            }

            st.session_state.scores.append(st.session_state.current_score)
            st.session_state.prompt_submitted = True

    else:
        score = st.session_state.current_score
        st.subheader("🤖 Model Output")
        st.code(score["output"])

        st.subheader("🎯 Target Output")
        st.code(score["target"])

        st.subheader("📊 Scoring Breakdown")
        col1, col2, col3 = st.columns(3)
        col1.metric("Match Score", f"{score['match_score']}%")
        col2.metric("Token Penalty", f"{score['token_penalty']}")
        col3.metric("Final Score", f"{score['final_score']}")

        # Dynamic feedback
        if score["final_score"] >= 90:
            st.success("🔥 Excellent match!")
        elif score["final_score"] >= 60:
            st.warning("👍 Not bad! Try to reduce tokens.")
        else:
            st.error("😬 Needs improvement.")

        if st.button("➡️ Next Round"):
            st.session_state.round += 1
            st.session_state.prompt_submitted = False

else:
    # --- Final scoreboard ---
    st.balloons()
    st.title("🏁 Game Over")
    st.header("📈 Final Scoreboard")

    df = pd.DataFrame(st.session_state.scores)
    st.dataframe(df.style.highlight_max(axis=0, subset=["final_score"], color="lightgreen"))

    top_player = df.loc[df["final_score"].idxmax(), "player"]
    st.success(f"🏆 Top Player: **{top_player}**")

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Results as CSV", csv, "results.csv", "text/csv")

# --- Progress bar ---
if st.session_state.round <= max_rounds:
    st.progress((st.session_state.round - 1) / max_rounds)

# --- Style tweaks ---
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

