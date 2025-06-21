import streamlit as st
import requests

st.set_page_config(page_title="MeetMind - Smart Transcripts", page_icon="🧠")
st.title("MeetMind ")
st.text("From conversation to clarity, tasks, and timely reminders.")

uploaded_file = st.file_uploader("Upload transcript (.txt) or audio (.mp3)", type=["txt", "mp3"])

if uploaded_file:
    file_name = uploaded_file.name

    is_text_file = file_name.endswith(".txt")

    if is_text_file:
        st.success("Detected .txt file. Ready to upload.")
        if st.button("Upload Transcript"):
            response = requests.post(
                "${text-endpoint}",
                files={"file": (file_name, uploaded_file.getvalue())}
            )
            st.success("Transcript uploaded successfully! Check Google Calendar for updates")
    else:
        st.success("Detected audio file. Please enter speaker info below.")

        num_speakers = st.number_input("Number of Speakers", min_value=1, max_value=10, step=1)

        speaker_data = []
        for i in range(num_speakers):
            st.markdown(f"**Speaker {i+1}**")
            name = st.text_input(f"Name for speaker {i+1}", key=f"name_{i}")
            email = st.text_input(f"Email for speaker {i+1}", key=f"email_{i}")
            if name and email:
                speaker_data.append({"name": name, "email": email})

        if len(speaker_data) == num_speakers:
            if st.button("Upload Audio + Speaker Info"):
                response = requests.post(
                    "{audio-endpoint}",
                    files = {
                        "file": (file_name, uploaded_file.getvalue(), "audio/mpeg")
                    },
                    data={"speakers": str(speaker_data)}  
                )
                st.success("Audio + speaker info uploaded successfully! Check Google Calendar for updates")
