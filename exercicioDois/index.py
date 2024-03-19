from flask import Flask, render_template, url_for, request
from PIL import Image

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/tratamento-imagem")
def tratamento_imagem():
    return render_template("tratamento-imagem.html")

@app.route("/tratamento-imagem", methods=["post"])
def tratar_imagem():
    
    if 'imagem' not in request.files:
        return "Nenhuma imagem foi enviada"

    imagem = request.files['imagem']
    return render_template("tratamento-imagem.html", result = imagem)

if __name__ == "__main__":
    app.run(debug=True)