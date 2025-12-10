from flask import Flask, request, jsonify, render_template


app = Flask(__name__, static_url_path='', static_folder='static')




###################################################
@app.get("/login")
def login():
    return render_template('login.html')

@app.get("/home-page")
def home():
    return render_template('index.html')

@app.get("/indicadores")
def indicadores():
    return render_template('indicadores.html')

@app.get("/cadastro usuario")
def cadastro_usuario():
    return render_template('cad_usu.html')

@app.get("/cadastro especialista")
def cadastro_especialista():
    return render_template('tela_cad_especialista.html')

###################################################

if __name__ == "__main__":
    app.run(debug=True)
    
    