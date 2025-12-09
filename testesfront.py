from flask import Flask, request, jsonify, render_template


app = Flask(__name__, static_url_path='', static_folder='static')




###################################################
@app.get("/login")
def login():
    return render_template('login.html')

@app.get("/home-page")
def home():
    return render_template('index.html')

<<<<<<< HEAD
@app.get("/Perfil")
def Perfil():
    return render_template('Perfil.html')
=======
@app.get("/indicadores")
def indicadores():
    return render_template('indicadores.html')
>>>>>>> b9e2d4d25a84bdbdd04cdc030959b647d1e4c5fd

###################################################

if __name__ == "__main__":
    app.run(debug=True)
    
    