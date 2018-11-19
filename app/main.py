from flask import Flask, request, render_template
from PIL import Image,ImageOps
import numpy as np
import cv2
from io import BytesIO 
import base64
import sys


app = Flask(__name__)

def edge_detection(img):
    img_array = np.asarray(img)
    img_array = cv2.Canny(img_array,100,200)
    img_array = cv2.bitwise_not(img_array)
    img = Image.fromarray(img_array)
    
    return img

def rgb_to_gray(img):
    img_array = np.asarray(img)
    img_array = cv2.cvtColor(img_array,cv2.COLOR_BGR2GRAY)
    img = Image.fromarray(img_array)
    
    return img


@app.route("/")
def index():
    
    return render_template("index.html")


@app.route("/result", methods=["POST"])
def result():
    try:
        stream = request.files["img_file"].stream
        binary = stream.read()
        img = Image.open(BytesIO(binary))

        if request.form["processing"] == "edge":
            img = edge_detection(img)
        elif request.form["processing"] == "gray":
            img = rgb_to_gray(img)

        buf = BytesIO()
        img.save(buf,format="png")
        img_b64str = base64.b64encode(buf.getvalue()).decode("utf-8")
        img_b64data = "data:image/png;base64,{}".format(img_b64str) 

        message = '処理に成功しました'
        return render_template("result.html", message = message, img_b64data = img_b64data)
    except Exception as e:
        tb = sys.exc_info()[2]
        print("message:{0}".format(e.with_traceback(tb)))
        message = '処理に失敗しました'
        return render_template("result.html", message = message)

if __name__ == "__main__":
    app.run()

