"""
CampusConnect Lite - AI Study & Resource Hub for Students
No database used - all data comes from simple CSV files.

Tabs:
1. Resources          - search/filter notes, past papers, slides, assignments
2. Study Groups       - search/filter study groups by subject, day, time, mode
3. AI Study Assistant - ask a Generative AI (Gemini) for study help
4. About              - project info and team

Team: Ismail, Kashif, Hafsa, Ifra
"""

import os
import pandas as pd
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# ---------------------------------------------------------
# SETUP
# ---------------------------------------------------------
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY", None)

st.set_page_config(page_title="CampusConnect Lite", page_icon="🎓", layout="centered")

AI_READY = bool(API_KEY)
if AI_READY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-3.6-flash")

SYSTEM_PROMPT = (
    "You are a friendly university study assistant. Explain academic topics "
    "in simple, beginner-friendly language. Give practical study advice and "
    "create clear study plans when requested. Keep answers well-organized "
    "and encouraging in tone."
)


def ask_ai(user_question: str) -> str:
    if not AI_READY:
        return ("⚠️ The AI Study Assistant is temporarily unavailable because "
                "no API key is configured. Please try the Resources or Study "
                "Groups tabs in the meantime.")
    try:
        full_prompt = f"{SYSTEM_PROMPT}\n\nStudent's question: {user_question}"
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return (f"⚠️ The AI is temporarily unavailable ({e}). "
                "Please try again in a moment.")


# ---------------------------------------------------------
# LOAD DATA (CSV files - no database)
# ---------------------------------------------------------
@st.cache_data
def load_resources():
    return pd.read_csv("resources.csv")


@st.cache_data
def load_study_groups():
    return pd.read_csv("study_groups.csv")


resources_df = load_resources()
groups_df = load_study_groups()

# ---------------------------------------------------------
# UI
# ---------------------------------------------------------
st.title("🎓 CampusConnect Lite")
st.caption("Find notes, past papers, study groups, and get instant AI study help — all in one place.")

tab1, tab2, tab3, tab4 = st.tabs(
    ["📚 Resources", "👥 Study Groups", "🤖 AI Study Assistant", "ℹ️ About"]
)

# ----- TAB 1: RESOURCES -----
with tab1:
    st.subheader("Find notes, past papers, slides & assignments")

    col1, col2, col3 = st.columns(3)
    with col1:
        subject_filter = st.selectbox(
            "Subject", ["All"] + sorted(resources_df["Subject"].unique().tolist())
        )
    with col2:
        type_filter = st.selectbox(
            "Resource Type", ["All"] + sorted(resources_df["Type"].unique().tolist())
        )
    with col3:
        semester_filter = st.selectbox(
            "Semester", ["All"] + sorted(resources_df["Semester"].unique().astype(str).tolist())
        )

    search_text = st.text_input("🔍 Search by keyword", placeholder="e.g. calculus, grammar, mechanics")

    filtered = resources_df.copy()
    if subject_filter != "All":
        filtered = filtered[filtered["Subject"] == subject_filter]
    if type_filter != "All":
        filtered = filtered[filtered["Type"] == type_filter]
    if semester_filter != "All":
        filtered = filtered[filtered["Semester"].astype(str) == semester_filter]
    if search_text:
        filtered = filtered[filtered["Title"].str.contains(search_text, case=False) |
                             filtered["Description"].str.contains(search_text, case=False)]

    st.markdown(f"**{len(filtered)} resource(s) found**")
    if len(filtered) == 0:
        st.info("No resources match your search. Try a different subject or keyword.")
    else:
        for _, row in filtered.iterrows():
            with st.container(border=True):
                st.markdown(f"**{row['Title']}**")
                st.caption(f"{row['Subject']} · {row['Department']} · Semester {row['Semester']} · {row['Type']}")
                st.write(row["Description"])
                st.markdown(f"[Open Resource]({row['Link']})")

# ----- TAB 2: STUDY GROUPS -----
with tab2:
    st.subheader("Find a study group")

    col1, col2, col3 = st.columns(3)
    with col1:
        g_subject = st.selectbox(
            "Subject", ["All"] + sorted(groups_df["Subject"].unique().tolist()), key="g_subject"
        )
    with col2:
        g_day = st.selectbox(
            "Day", ["All"] + sorted(groups_df["Day"].unique().tolist()), key="g_day"
        )
    with col3:
        g_mode = st.selectbox(
            "Mode", ["All", "Online", "Offline"], key="g_mode"
        )

    g_filtered = groups_df.copy()
    if g_subject != "All":
        g_filtered = g_filtered[g_filtered["Subject"] == g_subject]
    if g_day != "All":
        g_filtered = g_filtered[g_filtered["Day"] == g_day]
    if g_mode != "All":
        g_filtered = g_filtered[g_filtered["Mode"] == g_mode]

    st.markdown(f"**{len(g_filtered)} study group(s) found**")
    if len(g_filtered) == 0:
        st.info("No study groups match your search yet. Try a different subject or day.")
    else:
        for _, row in g_filtered.iterrows():
            with st.container(border=True):
                st.markdown(f"**{row['Subject']} Study Group** ({row['Department']})")
                st.caption(f"{row['Day']} at {row['Time']} · {row['Mode']} · {row['Members']} members")
                st.write(f"How to join: {row['ContactInfo']}")

    st.divider()
    st.caption("Want to start your own group? (Coming soon in a future version — for now, "
               "share your group details with your class coordinator to be added here.)")

# ----- TAB 3: AI STUDY ASSISTANT -----
with tab3:
    st.subheader("Ask your AI study assistant anything")
    st.caption("Try things like: explain a topic simply, build a study plan, get revision points, or practice questions.")

    preset = st.selectbox(
        "Quick prompts (optional)",
        [
            "Write your own question below",
            "Explain this topic in simple words: [your topic]",
            "Create a 7-day study plan for my exam on: [your subject]",
            "Give me important revision points for: [your topic]",
            "Create 10 practice questions on: [your topic]",
            "Explain this concept for a complete beginner: [your topic]",
        ],
    )

    default_text = "" if preset == "Write your own question below" else preset
    question = st.text_area("Your question", value=default_text, height=100)

    if st.button("Ask AI Assistant"):
        if question.strip():
            with st.spinner("Thinking..."):
                answer = ask_ai(question)
            st.markdown(answer)
        else:
            st.warning("Please type or select a question first.")

# ----- TAB 4: ABOUT -----
with tab4:
    st.subheader("About CampusConnect Lite")
    st.write(
        "CampusConnect Lite is a simple, beginner-friendly hub that helps students "
        "find academic resources, connect with study groups, and get instant AI-powered "
        "study help — all without needing complex logins or databases."
    )

    st.markdown("#### Our Team")
    st.write("**Ismail** — MBA — Team Leader")
    st.write("**Kashif** — BS Information Technology — Technical Lead")
    st.write("**Hafsa** — Professor of Engineering — Academic/Domain Lead")
    st.write("**Ifra** — BS English — Content, Communication & UX Lead")

    st.markdown("#### Built With")
    st.write("Python · Streamlit · Pandas · CSV data · Google Gemini API")

st.divider()
st.caption("Built by Team CampusConnect Lite — Ismail, Kashif, Hafsa & Ifra 🚀")
