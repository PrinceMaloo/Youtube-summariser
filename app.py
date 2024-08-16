import requests
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.request import Request
import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

# Define prompt
prompt = """You are a YouTube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text given here:  """

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define proxies
proxies = {
    'http': 'socks5://myproxy:9191',
    'https': 'socks5://myproxy:9191'
}

class ProxyRequest(Request):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = requests.Session()
        self.session.proxies.update(proxies)

def get_transcript(video_url):
    try:
        video_id = video_url.split("=")[-1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id, request_class=ProxyRequest)
        text = " ".join([item['text'] for item in transcript_text])
        return text
    except Exception as e:
        st.error(f"Error retrieving transcript: {e}")
        return None

def generate_gemini_content(transcript_text, prompt):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt + transcript_text)
        return response.text
    except Exception as e:
        st.error(f"Error generating content: {e}")
        return None

# Streamlit app
st.title("YouTube Transcript to Detailed Notes Converter")

youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    video_id = youtube_link.split("=")[-1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Detailed Notes"):
    if youtube_link:
        transcript_text = get_transcript(youtube_link)
        if transcript_text:
            summary = generate_gemini_content(transcript_text, prompt)
            if summary:
                st.markdown("## Detailed Notes:")
                st.write(summary)
