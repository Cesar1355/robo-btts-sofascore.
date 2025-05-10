import requests
import os
from bs4 import BeautifulSoup
import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def enviar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": mensagem,
        "parse_mode": "HTML"
    }
    requests.post(url, data=payload)

def obter_jogos():
    url = "https://www.sofascore.com/football//20240510"  # Data atual ou ajustável
    headers = {"User-Agent": "Mozilla/5.0"}
    resposta = requests.get(url, headers=headers)
    soup = BeautifulSoup(resposta.text, "html.parser")

    jogos = []
    for partida in soup.select(".eventRow"):
        try:
            times = partida.select_one(".cell__content").text.strip().split(" - ")
            if len(times) == 2:
                jogos.append(f"{times[0]} vs {times[1]}")
        except:
            continue

    return jogos

def main():
    jogos = obter_jogos()
    if jogos:
        mensagem = "<b>Sinais BTTS para hoje:</b>\n\n"
        for jogo in jogos[:5]:  # Limite de jogos (exemplo: 5)
            mensagem += f"• {jogo}\n"
        enviar_telegram(mensagem)
    else:
        enviar_telegram("Nenhum sinal encontrado hoje.")

if __name__ == "__main__":
    main()
