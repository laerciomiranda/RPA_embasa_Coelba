import requests
import json

class BianatechService:
    def __init__(self):
        self.url = "https://services.bianatech.com.br/6b865816-ea52-4248-9274-ee7981952c34"
        self.headers = {
            "Content-Type": "application/json"
        }

    def consultar(self, documento: str = "", campos: str = ""):
        try:
            payload = {
            "token": "cf903bb2-cf25-4e1a-bce1-8f035296743c",
            "documento": documento,
            "campos": campos
            }
            
            response = requests.get(
                self.url,
                headers=self.headers,
                data=json.dumps(payload),
                verify=False
            )

            # Verifica se a requisição foi bem sucedida
            if response.status_code == 200:
                try:
                    return response.json()
                except json.JSONDecodeError:
                    return {"erro": "Resposta não está em formato JSON", "resposta": response.text}
            else:
                return {
                    "erro": f"Falha na requisição (status {response.status_code})",
                    "detalhes": response.text
                }

        except requests.RequestException as e:
            return {"erro": f"Erro ao conectar à API: {str(e)}"}
