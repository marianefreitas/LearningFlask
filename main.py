from flask import Flask, render_template, request, redirect
import pandas as pd

app = Flask(__name__,)

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/upload", methods=['GET', 'POST'])
def upload():
        return render_template("upload.html")

@app.route("/data", methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        file = request.files['uploadFile']
        print(" file => ", file)
        data = pd.read_excel(file)
        print(" data => ", data)
        return render_template("data.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)