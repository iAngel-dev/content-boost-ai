from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Rate limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["10 per minute"]
)

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    error = None
    if request.method == "POST":
        topic = request.form["topic"]
        # Input validation: ensure topic is not empty and is a string
        if not topic or not isinstance(topic, str) or len(topic.strip()) == 0:
            error = "Veuillez entrer un sujet valide."
            return render_template("index.html", result=result, error=error)
        if len(topic) > 100:
            error = "Le sujet est trop long. Veuillez le limiter à 100 caractères."
            return render_template("index.html", result=result, error=error)
        prompt = f"Donne-moi une idée de vidéo virale TikTok sur le sujet suivant : {topic}. Inclue un titre, un script court, et une liste de hashtags."
        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                max_tokens=200,
                temperature=0.7
            )
            result = response.choices[0].text.strip()
            # Optional: Format the response for better readability
            if result:
                parts = result.split('\n')
                title = ''
                script = ''
                hashtags = ''
                for part in parts:
                    if part.lower().startswith('titre') or part.lower().startswith('title'):
                        title = part
                    elif part.lower().startswith('script'):
                        script = part
                    elif part.lower().startswith('hashtag'):
                        hashtags = part
                if title or script or hashtags:
                    result = f"<b>{title}</b><br>{script}<br>{hashtags}"
        except Exception as e:
            error = f"Une erreur est survenue lors de la génération : {str(e)}"
    return render_template("index.html", result=result, error=error)

if __name__ == "__main__":
    app.run(debug=True)
