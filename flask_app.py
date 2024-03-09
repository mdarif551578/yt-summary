import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import extract
import markdown

GOOGLE_API_KEY = "AIzaSyBLcku_zuoY1m4eyizYwJmNqfoVWMoYVCE"
genai.configure(api_key=GOOGLE_API_KEY)

def get_video_id(video_url):
    id = extract.video_id(video_url)
    return id

def get_subtitle(video_url):
    subtitle = ""
    video_id = get_video_id(video_url)
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    for segment in transcript:
        subtitle += segment['text']
    return subtitle

def summarize(text):
    summarized_text = ""
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(f"Can you generate a long descriptive and informative summery for this youtube video subtitle text??? ```{text}```")
        summarized_text = response.text
    except:
        pass
    return markdown.markdown(summarized_text)

def get_summarized_context(video_url):
    context = {
        "is_succeed": False,
        "message": "Something went wrong. Please try again...",
    }
    try:
        subtitle = get_subtitle(video_url)
        if subtitle == "":
            context["message"] = "No Transcript found for this video!"
        else:
            context = {
                "is_succeed": True,
                "message": "",
                "title": "",
                "channel": "",
                "summary": summarize(subtitle),
            }
    except:
        context["message"] = "No Transcript found for this video!"
    return context

from flask import Flask, render_template, request

app = Flask(__name__, template_folder="templates", static_folder="static", static_url_path="/static")

@app.route("/")
def home():
    print(request)
    return render_template("index.html")

@app.route("/summary", methods=['POST'])
def get_summary():
    context = {
        "is_succeed": False,
        "message": "Something went wrong. Please try again...",
    }
    try:
        video_url = request.form['video_url']
        context = get_summarized_context(video_url)
    except:
        context["message"] = "Enter a video url. Empty field not allowed!"
    return render_template("summary.html", context=context)

# if __name__ == "__main__":
#     app.run(debug=True, port=5050) # host="0.0.0.0",
