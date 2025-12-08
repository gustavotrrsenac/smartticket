import requests

# Base URL do seu backend
BASE_URL = "http://127.0.0.1:5000"

# Lista de rotas para testar
rotas = [
    {"nome": "Home", "url": "/", "metodo": "GET"},
    {"nome": "Listar Tickets", "url": "/api/tickets", "metodo": "GET"},
    {"nome": "Indicadores Totais", "url": "/api/totais", "metodo": "GET"},
    # Você pode adicionar mais rotas aqui
]

def testar_rotas():
    for rota in rotas:
        url_completa = BASE_URL + rota["url"]
        try:
            if rota["metodo"] == "GET":
                resposta = requests.get(url_completa)
            elif rota["metodo"] == "POST":
                # Exemplo: POST vazio, pode customizar payload
                resposta = requests.post(url_completa, json={})
            else:
                print(f"[AVISO] Método {rota['metodo']} não implementado para {rota['nome']}")
                continue

            print(f"\nRota: {rota['nome']} ({rota['url']})")
            print(f"Status Code: {resposta.status_code}")
            try:
                print("Resposta JSON:", resposta.json())
            except:
                print("Resposta Texto:", resposta.text)

        except Exception as e:
            print(f"[ERRO] Não foi possível acessar {rota['nome']}: {e}")

if __name__ == "__main__":
    testar_rotas()
