from flask import Flask, request, jsonify, render_template


app = Flask(__name__, static_url_path='', static_folder='static')




###################################################
@app.get("/login")
def login():
    return render_template('login.html')

@app.get("/home-page")
def home():
    return render_template('index.html')

@app.get("/Perfil")
def Perfil():
    return render_template('Perfil.html')

@app.get("/cad_usu")
def cad_usu():
    return render_template('cad_usu.html')

###################################################

if __name__ == "__main__":
    app.run(debug=True)
    
    