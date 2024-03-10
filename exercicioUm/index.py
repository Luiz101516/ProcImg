from flask import Flask, render_template, url_for, request

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/normalize-rgb")
def normalize_rgb():
    return render_template("normalize-rgb.html")

@app.route("/cmky-to-rgb")
def cmky_to_rgb():
    return render_template("cmky-to-rgb.html")

@app.route("/hsv-to-rgb")
def hsv_to_rgb():
    return render_template("hsv-to-rgb.html")

@app.route("/rgb-to-cmky")
def rgb_to_cmky():
    return render_template("rgb-to-cmky.html")

@app.route("/rgb-to-grey")
def rgb_to_grey():
    return render_template("rgb-to-grey.html")

@app.route("/rgb-to-hsv")
def rgb_to_hsv():
    return render_template("rgb-to-hsv.html")

@app.route("/normalize", methods=["post"])
def normalize():
    color = request.form["color"]
    rgb = hex_to_rgb(color)
    return render_template("normalize-rgb.html", result=sum_normalized_rgb(rgb))


def hex_to_rgb(hexa):
    hexa = hexa.lstrip('#')
    return tuple(int(hexa[i:i+2], 16)  for i in (0, 2, 4))

def sum_normalized_rgb(rgb):
    normalized_values = [component / 255.0 for component in rgb]
    return str(sum(normalized_values))

if __name__ == "__main__":
    app.run(debug=True)