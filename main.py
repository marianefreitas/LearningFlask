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
       
        xl = pd.ExcelFile(file)
        print(xl.sheet_names)

# O atributo nrows precisa ser dinamico
# Formatar as datas e tirar o horário
# remover coluna de indices?

        def convert_to_int(row):
          return int(row)
        
        def convert_transferido(row):
            if row.lower() == 'x':
                return True
            else:
                return row

        df = pd.read_excel(file, 
                           sheet_name=xl.sheet_names[5],
                           header=12,
                           usecols="A:AA",
                           nrows=31,
                           converters={'Nº Aluno':convert_to_int,"Unnamed: 3": convert_transferido},
                           index_col=False)
        
        df = df.rename(columns={"Unnamed: 3": " Transferido"})

        df.fillna(False, inplace=True)

        return render_template("data.html", data=df.to_html())

if __name__ == "__main__":
    app.run(debug=True)