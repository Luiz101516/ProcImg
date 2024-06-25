from flask import Flask, render_template, url_for, request

app = Flask(__name__)

@app.route("/templates/")
def main():
    return render_template("index.html")

@app.route("/templates/normalize-rgb")
def normalize_rgb():
    return render_template("normalize-rgb.html")

@app.route("/cmyk-to-rgb")
def cmyk_to_rgb():
    return render_template("cmyk-to-rgb.html")

@app.route("/hsv-to-rgb")
def hsv_to_rgb():
    return render_template("hsv-to-rgb.html")

@app.route("/rgb-to-cmyk")
def rgb_to_cmyk():
    return render_template("rgb-to-cmyk.html")

@app.route("/rgb-to-grey")
def rgb_to_grey():
    return render_template("rgb-to-grey.html")

@app.route("/rgb-to-hsv")
def rgb_to_hsv():
    return render_template("rgb-to-hsv.html")

def hex_to_rgb(hexa):
    hexa = hexa.lstrip('#')
    return tuple(int(hexa[i:i+2], 16)  for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

@app.route("/normalize", methods=["post"])
def normalize():
    color = request.form["color"]
    rgb = hex_to_rgb(color)
    return render_template("normalize-rgb.html", result=sum_normalized_rgb(rgb))

def sum_normalized_rgb(rgb):
    normalized_values = [component / 255.0 for component in rgb]
    return str(round(sum(normalized_values),2))

@app.route("/rgb-to-hsv", methods=["post"])
def convert_rgb_to_hsv():
    color = request.form["color"]
    rgb = hex_to_rgb(color)
    return render_template("rgb-to-hsv.html", result=rgb_to_hsv(rgb))

def rgb_to_hsv(rgb):
    r, g, b = rgb
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    cmax = max(r, g, b)
    cmin = min(r, g, b)
    delta = cmax - cmin

    if delta == 0:
        hue = 0
    elif cmax == r:
        hue = (60 * ((g - b) / delta) + 360) % 360
    elif cmax == g:
        hue = (60 * ((b - r) / delta) + 120) % 360
    else:
        hue = (60 * ((r - g) / delta) + 240) % 360

    saturation = 0 if cmax == 0 else delta / cmax
    value = cmax

    formatted_hue = f"{hue:.1f}°"
    formatted_saturation = f"{saturation * 100:.1f}%"
    formatted_value = f"{value * 100:.1f}%"

    return formatted_hue, formatted_saturation, formatted_value

@app.route("/rgb-to-cmyk", methods=["post"])
def convert_rgb_to_cmyk():
    color = request.form["color"]
    rgb = hex_to_rgb(color)
    return render_template("rgb-to-cmyk.html", result=rgb_to_cmyk(rgb))

def rgb_to_cmyk(rgb):
    r, g, b = [x / 255.0 for x in rgb]

    k = 1 - max(r, g, b)
    c = (1 - r - k) / (1 - k) if (1 - k) != 0 else 0
    m = (1 - g - k) / (1 - k) if (1 - k) != 0 else 0
    y = (1 - b - k) / (1 - k) if (1 - k) != 0 else 0

    formatted_c = f"{c * 100:.1f}%"
    formatted_m = f"{m * 100:.1f}%"
    formatted_y = f"{y * 100:.1f}%"
    formatted_k = f"{k * 100:.1f}%"

    return formatted_c, formatted_m, formatted_y, formatted_k

@app.route("/rgb-to-grey", methods=["post"])
def convert_rgb_to_grey():
    color = request.form["color"]
    rgb = hex_to_rgb(color)
    rgb_grey_scale = rgb_to_grey(rgb)
    r, g, b = rgb_grey_scale
    return render_template("rgb-to-grey.html", result=str(rgb_to_hex(rgb_grey_scale)), result_number=str(r))

def rgb_to_grey(rgb):
    r, g, b = rgb
    grey_value = int((r + g + b) / 3.0)
    return grey_value, grey_value, grey_value 
    
@app.route("/hsv-to-rgb", methods=["post"])
def convert_hsv_to_rgb():
    h = request.form["matriz"]
    s = request.form["saturacao"]
    v = request.form["valor"]
    rgb_value = hsv_to_rgb(float(h), float(s), float(v))
    return render_template("hsv-to-rgb.html", result=str(rgb_to_hex(rgb_value)), result_number=str(rgb_value))
    
def hsv_to_rgb(h, s, v):
    h /= 360.0
    s /= 100.0
    v /= 100.0

    if s == 0:
        return int(v * 255), int(v * 255), int(v * 255)

    i = int(h * 6.)
    f = (h * 6.) - i
    p = v * (1. - s)
    q = v * (1. - s * f)
    t = v * (1. - s * (1. - f))

    if i % 6 == 0:
        r, g, b = v, t, p
    elif i % 6 == 1:
        r, g, b = q, v, p
    elif i % 6 == 2:
        r, g, b = p, v, t
    elif i % 6 == 3:
        r, g, b = p, q, v
    elif i % 6 == 4:
        r, g, b = t, p, v
    else:
        r, g, b = v, p, q

    return int(r * 255), int(g * 255), int(b * 255)

@app.route("/cmyk-to-rgb", methods=["post"])
def convert_cmyk_to_rgb():
    c = request.form["cyan"]
    m = request.form["magenta"]
    y = request.form["yellow"]
    k = request.form["black"]
    
    rgb_value = cmyk_to_rgb(float(c), float(m), float(y), float(k))
    return render_template("cmyk-to-rgb.html", result=str(rgb_to_hex(rgb_value)), result_number=str(rgb_value))

def cmyk_to_rgb(c, m, y, k):
    c /= 100.0
    m /= 100.0
    y /= 100.0
    k /= 100.0
    
    r = 255 * (1 - c) * (1 - k)
    g = 255 * (1 - m) * (1 - k)
    b = 255 * (1 - y) * (1 - k)
    return round(r), round(g), round(b)
    
if __name__ == "__main__":
    app.run()
