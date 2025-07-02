import streamlit as st
import json
import uuid
from transformers import pipeline
import difflib

# load challenges
with open("challenges.json", "r") as f:
    CHALLENGES = json.load(f)

TOTAL_ROUNDS = 5
MAX_PLAYERS = 25

# setup model
generator = pipeline("text-generation", model="gpt2")

# initialize session
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())[:8]

if "player_name" not in st.session_state:
    st.session_state.player_name = ""

if "current_round" not in st.session_state:
    st.session_state.current_round = 0

if "results" not in st.session_state:
    st.session_state.results = []

# sidebar: join session
st.sidebar.title("Session")
st.sidebar.write(f"Session ID: `{st.session_state.session_id}`")

player_name = st.sidebar.text_input("Enter your player name", value=st.session_state.player_name)
if player_name:
    st.session_state.player_name = player_name

# check valid
if not st.session_state.player_name:
    st.warning("Enter a name to continue.")
    st.stop()

# main game logic
round_num = st.session_state.current_round

if round_num >= TOTAL_ROUNDS:
    st.header("Final Results")
    df = st.session_state.results
    total_score = sum(r["score"] for r in df)
    st.write(f"Total Score: **{total_score} / {TOTAL_ROUNDS * 100}**")
    st.dataframe(df)
    st.stop()

# load current challenge
challenge = CHALLENGES[round_num % len(CHALLENGES)]
st.title(f"Round {round_num + 1} of {TOTAL_ROUNDS}")
st.markdown(f"**Task:** {challenge['task']}")

prompt_input = st.text_area("Enter your prompt")

if st.button("Submit Prompt"):
    if not prompt_input.strip():
        st.warning("Prompt is empty.")
        st.stop()

    response = generator(prompt_input, max_new_tokens=15)[0]['generated_text']
    output = response[len(prompt_input):].strip()

    # scoring
    target = challenge["target"].strip().lower()
    result = output.strip().lower()
    match_ratio = difflib.SequenceMatcher(None, result, target).ratio()
    match_score = round(match_ratio * 100)

    token_penalty = min(len(prompt_input.split()) * 2, 30)
    final_score = max(match_score - token_penalty, 0)

    st.success(f"Model Output: {output}")
    st.info(f"Match Score: {match_score}/100")
    st.info(f"Token Penalty: -{token_penalty}")
    st.subheader(f"Final Score: {final_score}/100")

    # store result
    st.session_state.results.append({
        "round": round_num + 1,
        "player": st.session_state.player_name,
        "task": challenge["task"],
        "prompt": prompt_input,
        "output": output,
        "score": final_score
    })
    st.session_state.current_round += 1
    st.experimental_rerun()
