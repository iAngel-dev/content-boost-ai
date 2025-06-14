from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        topic = request.form["topic"]
        prompt = f"Donne-moi une idée de vidéo virale TikTok sur le sujet suivant : {topic}. Inclue un titre, un script court, et une liste de hashtags."
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=200,
            temperature=0.7
        )
        result = response.choices[0].text.strip()
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
