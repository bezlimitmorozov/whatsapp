import requests
import datetime

TOKEN = '1388568494:AAFZCASLFx64WZnpQLyqmBjht66Y3LU9xEI' 

def send_to_telegram(text, token, chat):
    url = "https://api.telegram.org/bot" + token + "/sendMessage"  # 1388568494:AAFZCASLFx64WZnpQLyqmBjht66Y3LU9xEI 5156460237:AAEt1if6meaEGae-8lVWp20Egj4TnBdDdEs

    payload = {
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False,
        "disable_notification": False,
        "chat_id": chat
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)


now = str(datetime.date.today()).split('-')
url = f"https://bill.bezlimit.ru/log/other/check-whats-app-{''.join(now)}.log"

response = requests.post(url, headers={
    "Authorization": "Basic d2V0ZXI6VjdCbjYzeGN2MTJA",
    "Host": "bill.bezlimit.ru",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
            "image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Content-Type": "application/json-patch+json"})

out = response.content.decode()
print(out)
out = out.split('in ')[0]
print(out)

if "Выход." in out:
    message = f"[Скрипт по проверке аккаунтов Whatsapp]({url})\nЗавершился УСПЕШНО."
    send_to_telegram(message, TOKEN, '-1001179024349')

elif "Exception" in out:
    message = f"[Скрипт по проверке аккаунтов Whatsapp]({url})\nЗавершился С ОШИБКОЙ." \
              f"\nКод ошибки: ``` {out.split('Exception ')[1]} ```"
    send_to_telegram(message, TOKEN, '-1001179024349')
