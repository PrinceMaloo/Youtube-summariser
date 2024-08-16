
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
import os
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup

load_dotenv()


prompt="""You are Yotube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text given here:  """

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))



def get_transcript(video_url):
    # Extract video ID from URL
    video_id = video_url.split("v=")[-1]

    # Construct URL for transcript page (example, may need adjustment)
    transcript_url = f"https://www.youtube.com/watch?v={video_id}"

    try:
        # Send a request to the transcript page
        response = requests.get(transcript_url)
        response.raise_for_status()

        # Parse the page content
        soup = BeautifulSoup(response.text, 'html.parser')
        transcript_data = soup.find_all("script", {"type": "application/json"})

        # Extract transcript text (example, may need adjustment based on actual page structure)
        transcript_text = transcript_data[0].get_text() if transcript_data else "Transcript not found"
        return transcript_text
    except Exception as e:
        return f"An error occurred: {e}"

def generate_gemini_content(transcript_text,prompt):

    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript_text)
    return response.text


st.title("YouTube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    video_id = youtube_link.split("=")[-1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Detailed Notes"):
    transcript_text=get_transcript(youtube_link)

    if transcript_text:
        summary=generate_gemini_content(transcript_text,prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)



