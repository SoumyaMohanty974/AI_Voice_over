import streamlit as st
from moviepy.editor import VideoFileClip, AudioFileClip  # Add AudioFileClip here
import whisper
from gtts import gTTS
from pydub import AudioSegment
import os

# Function to extract audio from video
def extract_audio(video_path):
    video = VideoFileClip(video_path)
    audio_path = "extracted_audio.wav"
    video.audio.write_audiofile(audio_path)
    return audio_path

# Function to transcribe audio
def transcribe_audio(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path, word_timestamps=True)
    transcript_text = " ".join([seg["text"] for seg in result["segments"]])
    return transcript_text

# Function to generate AI voice
def generate_ai_voice(text):
    if isinstance(text, list):
        text = " ".join(text)
    tts = gTTS(text)
    audio_path = "ai_audio.mp3"
    tts.save(audio_path)
    return audio_path

# Function to replace audio in video
def replace_audio(video_path, new_audio_path, output_path):
    video = VideoFileClip(video_path)
    new_audio = AudioFileClip(new_audio_path)
    video = video.set_audio(new_audio)
    video.write_videofile(output_path, codec="libx264", audio_codec="aac")

# Streamlit app
st.title("AI Translation Voice Over")

uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov"])

if uploaded_file is not None:
    video_path = "uploaded_video.mp4"
    with open(video_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.video(video_path)

    # Extract and transcribe audio
    if st.button("Process Video"):
        with st.spinner("Extracting and transcribing audio..."):
            audio_path = extract_audio(video_path)
            transcript = transcribe_audio(audio_path)
            st.write("Transcribed Text:", transcript)

        # Generate AI voice
        with st.spinner("Generating AI voice..."):
            ai_audio_path = generate_ai_voice(transcript)

        # Replace audio in the video
        output_video_path = "output_video.mp4"
        with st.spinner("Replacing audio in video..."):
            replace_audio(video_path, ai_audio_path, output_video_path)

        st.success("Audio has been replaced successfully!")
        st.video(output_video_path)

        # Option to download the output video
        with open(output_video_path, "rb") as f:
            st.download_button("Download Modified Video", f, file_name="modified_video.mp4")
