#from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np
import pandas as pd

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename


import json
from flask import (Blueprint, request, render_template, redirect, session,
               make_response, jsonify)
from flask import Response
from pathlib import Path
Path("uploads").mkdir( exist_ok=True )
Path("TEMP").mkdir( exist_ok=True )

# Define a flask app
app = Flask(__name__)
app.secret_key = "Rendich-Cepal"
df_ods = pd.read_csv("lista_ods.csv")


################################################################
import uuid
################################################################
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util

def fn_test(model,
    sentences,
    sentence_numbers,
    max_result = -1,
    min_score = 0.4,
    sentences2 = df_ods):
  sentence_numbers = sentence_numbers
  sentences = sentences
  embeddings1 = model.encode(sentences, convert_to_tensor=True)
  embeddings2 = model.encode(sentences2, convert_to_tensor=True)

  result = []
  if  "assignmentID" in session:
        assignmentID = session['assignmentID']
  print("#" * 10)
  print("assignmentID [1]: " + assignmentID)
  print("#" * 10)

  #Compute cosine-similarits
  cosine_scores = util.cos_sim(embeddings1, embeddings2)
  print("*** sentences: ")
  print(sentences)
  print("=" * 10)

  #Output the pairs with their score
  for i in range(len(sentences)):
    row = []
    index = 1
    for j in range(len(sentences2)):
      row.append([sentence_numbers[i],sentences[i], sentences2[j], cosine_scores[i][j]])
    aux_row = pd.DataFrame(row).sort_values([1,3], ascending=False)
    if max_result > 0:
        aux_row = aux_row.head( max_result )
    aux_row["Rank"] = [(i+1) for i in range(len(aux_row))]
    result.append(aux_row)
  if len(result) == 0:
    return None
  aux = pd.concat(result)
  aux.columns = ["Numero","Entrada", "ODS", "score", "Rank"]
  aux["score"] = (aux["score"] * 100).astype(int)
  return aux 

def create_multi(matrix):
  #matrix["N_Entrada"] = matrix["Entrada"].str.split().str.get(0)
  matrix["N_ODS"] = matrix["ODS"].str.split().str.get(0)
  matrix["N_ODS1"] = matrix["ODS"].apply(lambda x : int(x.split(".")[0]))
  return pd.pivot_table(matrix, index = ["Numero","Entrada", "Rank", "ODS", "N_ODS1"])

def descarga(file1):
  df_entrada = pd.read_csv(file1, header=None)

  print("- df_entrada")
  print(df_entrada)
  model1 = SentenceTransformer('hiiamsid/sentence_similarity_spanish_es') # 11 s
  df_entrada.columns = ["Numeros","Entrada"]
  matrix = fn_test(model = model1,
    sentence_numbers = df_entrada.Numeros.values, 
          sentences = df_entrada.Entrada.values,
          sentences2 = df_ods["Meta ODS"]
          )
  matrix # 36 s
  salida = create_multi(matrix)
  return salida


def model_predict(filename):
    x = 1
    df_sentences = pd.read_csv(filename, header=None, names=["Requested"], delimiter=";")
    df_preds = descarga(filename)

    if "assignmentID" in session:
        assignmentID = session['assignmentID']

    basepath = os.path.dirname(__file__)
    file_path = os.path.join(
        basepath, 'TEMP', secure_filename(assignmentID) + ".csv" )
    print("#" * 10)
    print(file_path)
    print("#" * 10)
    df_preds = df_preds.reset_index()
    df_preds.to_csv(file_path)

    preds = [{ "sentence":row["Entrada"],  "n_sentence":row["Numero"],  "Rank": row["Rank"],  "ODS": row["ODS"],  "score": row["score"] }  for index, row in df_preds.iterrows()]
    return preds


@app.route('/', methods=['GET'])
def index():
    # Main page
    assignmentID = str(uuid.uuid1())
    session['assignmentID'] = assignmentID

    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if "assignmentID" in session:
        assignmentID = session['assignmentID']
    print("#" * 10)
    print("assignmentID [0]: " + assignmentID)
    print("#" * 10)

    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path)

        pred_class = preds

        documents_ = []
        documents_ = preds

        #return Response(json.dumps(documents_), mimetype='application/json')
        return json.dumps(str(documents_))

    return None


##################
@app.route('/download', methods=['POST'])
def download():
    players = request.form.getlist('check_list')

    if "assignmentID" in session:
        assignmentID = session['assignmentID']

    basepath = os.path.dirname(__file__)
    file_path = os.path.join(
        basepath, 'TEMP', secure_filename(assignmentID) + ".csv" )
    print("#" * 10)
    print(file_path)
    print("#" * 10)

    data_result = pd.read_csv(file_path, index_col=0)

    data = data_result.iloc[players]
    print("--" * 5)
    #print(data)
    # Save the file to ./uploads
    basepath = os.path.dirname(__file__)
    file_path = os.path.join(
        basepath, 'TEMP', secure_filename(assignmentID) + ".csv" )
    print("#" * 10)
    print(file_path)
    print("#" * 10)

    data = data.to_csv(index=False)
    print("=======" * 5)
    #print(data)
    if "assignmentID" in session:
        assignmentID = session['assignmentID']

    return Response(
        data,
        mimetype="text/csv",
        #headers={"Content-disposition": "attachment; filename=" + file_path })
        headers={"Content-disposition": "attachment; filename=" + "resultados.csv" })

##################

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(debug=False)
