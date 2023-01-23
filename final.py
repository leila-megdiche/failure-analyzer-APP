from flask import Flask, render_template , Response, request
from simpful import *

app = Flask(__name__)

@app.route("/")
def home() :
    return render_template("fini.html")
@app.route("/fini.html")
def WebPage1() :
    return render_template("fini.html")
@app.route("/traitment",methods=["POST" ,"GET"])
def traitment() :
    donnees = request.form
    #print(donnees)
    t1= (donnees.get('noises'))
    t2= (donnees.get('Vibration'))
    t3= (donnees.get('Smells'))
    t4= (donnees.get('Leaks'))
    if t1=='' or t2=='' or t3=='' or t4=='':
        t1,t2,t3,t4=0,0,0,0
    else:
         t1= int(donnees.get('noises'))
         t2= int(donnees.get('Vibration'))
         t3= int(donnees.get('Smells'))
         t4= int(donnees.get('Leaks'))

   
   
     # Create a fuzzy system object
    FS = FuzzySystem()

     # Define fuzzy sets and linguistic variables
    S_1 = FuzzySet(function=Triangular_MF(a=0, b=2, c=4), term="Humming")
    S_2 = FuzzySet(function=Triangular_MF(a=3, b=5, c=7), term="Rattling")
    S_3 = FuzzySet(function=Triangular_MF(a=6, b=8, c=10), term="Grinding")
    FS.add_linguistic_variable("noises", LinguisticVariable([S_1, S_2, S_3], concept="types of noises", universe_of_discourse=[0,10]))

    F_1 = FuzzySet(function=Triangular_MF(a=0, b=2, c=4), term="Transient")
    F_2 = FuzzySet(function=Triangular_MF(a=3, b=5, c=7), term="Continuous")
    F_3 = FuzzySet(function=Triangular_MF(a=6, b=8, c=10), term="Forced")
    FS.add_linguistic_variable("Vibration", LinguisticVariable([F_1, F_2,F_3], concept="vibration degree", universe_of_discourse=[0,10]))

    L_1 = FuzzySet(function=Triangular_MF(a=0, b=2, c=4), term="Air")
    L_2 = FuzzySet(function=Triangular_MF(a=3, b=5, c=7), term="Oil")
    L_3 = FuzzySet(function=Triangular_MF(a=6, b=8, c=10), term="Gaz")
    FS.add_linguistic_variable("Leaks", LinguisticVariable([L_1, L_2, L_3], concept="type of leaks", universe_of_discourse=[0,10]))

    M_1 = FuzzySet(function=Triangular_MF(a=0, b=2, c=4), term="Acrid")
    M_2 = FuzzySet(function=Triangular_MF(a=3, b=5, c=7), term="Metallic")
    M_3 = FuzzySet(function=Triangular_MF(a=6, b=8, c=10), term="Burning")
    FS.add_linguistic_variable("Smells", LinguisticVariable([M_1, M_2, M_3], concept="type of smells", universe_of_discourse=[0,10]))

    # Define output fuzzy sets and linguistic variable
    T_1 = FuzzySet(function=Triangular_MF(a=0, b=2, c=4), term="Minor")
    T_2 = FuzzySet(function=Triangular_MF(a=3, b=5, c=7), term="Major")
    T_3 = FuzzySet(function=Triangular_MF(a=6, b=8, c=10), term="Catastrophic")
    FS.add_linguistic_variable("failure",LinguisticVariable([T_1, T_2, T_3],concept="degree of failure",universe_of_discourse=[0,25]))

    # Define fuzzy rules
    R1 = "IF (Leaks IS Gaz) AND (Smells IS Burning) AND ((Vibration IS Transient) OR (Vibration IS Continuous) OR (Vibration IS Forced)) AND ((noises IS Humming) OR (noises IS Rattling) OR (noises IS Grinding))  THEN (failure IS Catastrophic)"
    R2 = "IF (noises IS Rattling) AND (Leaks IS Oil) AND (Vibration IS Continuous) AND (Smells IS Metallic) THEN (failure IS Major)"
    R3 = "IF (noises IS Humming) AND (Leaks IS Air) AND (Vibration IS Transient) AND (Smells IS Acrid) THEN (failure IS Minor)"
    R4 = "IF (Vibration IS Continuous) AND (Smells IS Metallic) AND (noises IS Grinding) AND (Leaks IS Oil) THEN (failure IS Major)"
    R5 = "IF (noises IS Humming) AND (Leaks IS Oil) AND (Smells IS Acrid) AND (Vibration IS Continuous) THEN (failure IS Minor)"
    FS.add_rules([R1, R2, R3, R4, R5])

    # Set antecedents values
    FS.set_variable("noises",t1)
    FS.set_variable("Vibration",t2)
    FS.set_variable("Smells",t3)
    FS.set_variable("Leaks",t4)
   
    # Perform Mamdani inference and print output
    #print(FS.Mamdani_inference(["failure"]))
    result = FS.Mamdani_inference(["failure"])
    value = result.get("failure", 0)
    if value <= 3:
        return render_template("hmd1.html")
         
    if value > 3 and value <= 6 :
         return render_template("hmd2.html")
    if value > 6:
         return render_template("hmd3.html")

   

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
