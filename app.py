
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()


prompt="""You are Yotube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text given here:  """

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

def get_transcript(video_url):
    vid_id = video_url.split("=")[-1]  # Extract the video ID from the URL
    transcript_text = []

    try:
        transcript_data = YouTubeTranscriptApi.get_transcript(vid_id)
        transcript_text += transcript_data
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""  # Return empty string in case of error
    
    text = ""
    for i in transcript_text:
        text += " " + i['text']
    
    return text

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



