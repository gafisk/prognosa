import re
from flask import Flask, render_template, request
import joblib
import numpy as np
import pandas as pd
import sklearn

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/prediksi')
def prediksi():
    return render_template("prediksi.html")


if __name__ == "__main__":
    app.run(debug=True)