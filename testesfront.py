from flask import Flask, request, jsonify, render_template


app = Flask(__name__, static_url_path='', static_folder='static')

###################################################
@app.get("/login")
def login():
    return render_template('login.html')

@app.get("/home-page")
def home():
    return render_template('index.html')

@app.get("/perfil")
def Perfil():
    return render_template('Perfil.html')

@app.get("/cad_usu")
def cad_usu():
    return render_template('cad_usu.html')

@app.get("/painel_adm")
def adm():
    return render_template('painel_adm.html')

@app.get("/cadastro usuario")
def cadastro_usuario():
    return render_template('cad_usu.html')

@app.get("/cadastro especialista")
def cadastro_especialista():
    return render_template('tela_cad_especialista.html')

@app.get("/indicadores")
def indicadores():
    return render_template('indicadores.html')

@app.get("/tickets-gerais")
def tela_de_tickets():
    return render_template('tickets_gerais.html')

@app.get("/meus_chamados")
def meus_chamados():
    return render_template('tickets_pessoais.html')

@app.get("/chat")
def chat_user():
    return render_template('chat_user.html')

@app.get("/adm")
def painel_adm():
    return render_template('vali_esp_adm.html')

@app.get("/tickets")
def tickets():
    return render_template('tickets_gerais.html')

@app.get("/details") 
def detalhes_do_perfil():
    return render_template('ticket-details.html')

###################################################

if __name__ == "__main__":
    app.run(debug=True)
    
    