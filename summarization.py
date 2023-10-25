import sys
import requests
import json


class SummarizationModule:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        url: str,
    ) -> None:
        self.url = url
        self.headers = {
            "Accept": "application/json;UTF-8",
            "Content-Type": "application/json;UTF-8",
            "X-NCP-APIGW-API-KEY-ID": client_id,
            "X-NCP-APIGW-API-KEY": client_secret,
        }

    def set_client_info(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret

    def summarize(self, text: str) -> str:
        data = {
            "document": {"content": f"{text}"},
            "option": {"language": "ko", "model": "general", "tone": 2, "summaryCount": 6},
        }
        # result = "ERROR"
        response = requests.post(self.url, headers=self.headers, data=json.dumps(data).encode("UTF-8"))
        rescode = response.status_code
        if rescode == 200:
            result = response.json()["summary"]
        else:
            print("Error : " + response.text)

        return result
