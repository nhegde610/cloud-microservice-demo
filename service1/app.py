from flask import Flask,request,render_template

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR']=False

@app.route("/")
def mainhtml():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=3000,debug=True)
