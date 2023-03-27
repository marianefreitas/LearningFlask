from flask import Flask, render_template, request, redirect
import pandas as pd
import xlwings as xw


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
       
        xl = pd.ExcelFile(file)
      
        df = pd.read_excel(file, 
                           sheet_name="Lista Presença_Alunos",
                           header=12,
                           usecols="B:AA")
        
        print(" df=> ",  df.tail() )
        return render_template("data.html", data=df.to_html())

if __name__ == "__main__":
    app.run(debug=True)