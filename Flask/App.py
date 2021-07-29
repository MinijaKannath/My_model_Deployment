from flask import Flask,render_template,request
import numpy as np
import pickle

app = Flask(__name__)
port = 9000 
@app.route("/")
def index():
    return render_template("HTML.html")

# prediction function
def ValuePredictor(to_predict_list):
    import os
        
    print("current working directory: ", os.getcwd())

    file_handle = None
    to_predict = np.array(to_predict_list).reshape(1, 22)
    try :
        file_handle = open("Flask/finalized_model.sav", "rb")
    except:
        print("Could not open file")
    
    loaded_model = pickle.load(file_handle)
    result = loaded_model.predict(to_predict)
    return result[0]
  
@app.route('/result', methods = ['POST'])
def result():
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        to_predict_list = list(to_predict_list.values())
        to_predict_list = list(map(int, to_predict_list))
        result = ValuePredictor(to_predict_list)        
        if int(result)== 0:
            prediction ='Operating'
        elif int(result)==1:
            prediction ='Acquired' 
        elif int(result) == 2:
            prediction = "Closed" 
        else:
            prediction = "IPO(Initial Public Offering)"

        return render_template("result.html", prediction = prediction)
if __name__ =="__main__":
    app.run(port=port,debug=True)
    app.config["TRMPLATES_AUTO_RELOAD"] =True
