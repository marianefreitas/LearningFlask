from flask import Flask, render_template, request, redirect
import pandas as pd
import sqlite3
import calendar
import time
from datetime import datetime

con = sqlite3.connect('dataframe.db', check_same_thread=False)

create_sql = "CREATE TABLE IF NOT EXISTS frequencia (nome_aluno TEXT, serie TEXT, status TEXT, data TEXT, data_alteracao INTEGER, frequencia TEXT ) "

cur = con.cursor()

cur.execute(create_sql)

# for row in df.itertuples():
#     insert_sql = "INSERT INTO frequencia () VALUES"

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


        
                       
        xl = pd.ExcelFile(file)
        #print(xl.sheet_names)

# O atributo nrows precisa ser dinamico
# Formatar as datas e tirar o horário
# remover coluna de indices?
# usecols dinamico?

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

        
        #print(" 4 ==> ", df.columns[4])
        #print(" 10 ==> ", df.columns[10])
        #print(df.shape)
        currentData = time.gmtime()
        dataTS= calendar.timegm(currentData)
        tsConvertido = datetime.fromtimestamp(dataTS)
        print(tsConvertido.strftime("%d-%m-%Y, %H:%M:%S"))
        coluna = 3

        #como fazer o range das colunas dinamico?
        for i in range (20):
            coluna +=1
            numerolinha= 0
            for row in df.itertuples():
                numerolinha += 1
                insert_sql = f"INSERT INTO frequencia (nome_aluno, serie, status, data, data_alteracao, frequencia  ) VALUES ('{row[2]}', '{row[3]}', '{row[4]}', '{df.columns[coluna]}', {dataTS}, '{row[coluna+1]}' );"
                #print(insert_sql)
                cur.execute(insert_sql)
            #print(" ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++" ,coluna, numerolinha)
            # coluna = coluna + 1
            #print(" 10 ==> ", df.columns[10])

        # for i in df.columns:
        #     print(df[i])
    con.commit()    
    return render_template("data.html", data=df.to_html())

if __name__ == "__main__":
    app.run(debug=True)