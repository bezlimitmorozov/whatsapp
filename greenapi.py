import requests

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


message = ''

accounts = {'26564': '53765baec53fc95ff1fda7c8bf295e459eef32b4f5be385b9e',
            '21269': '99c29f76d508405f16c0b1c83a251324835ab508c7546fc41e',
            '1101733372': 'adadbfec5bb649ba8abc754f926bc3fa6ebe202f63414fe887',
            '1101733373': 'e2648d3d898f45b9bd521cbe3f2859fc47a70385a21047e88d',
            '1101733374': '173b4386761f4e2fade2f14d3ffb9989a0907f5eb56644658a',
            '1101757556': '5ab883ce797b4add94839f46d416b9bdec679e3a68a449d09a',
            '1101757557': 'c207d7a95c3743f7a9c250e7001e3bdb0876b1d94e9e430592'
}
for i in accounts:
    response_url = "https://api.green-api.com/waInstance{0}/getStateInstance/{1}".format(i, accounts[i])
    response = requests.get(response_url)
    print(response.text)
    if 'authorized' not in response.text:
            message += f'\nВнимание!\nОтвет api аккаунта - [{i}](https://console.green-api.com/instanceList/{i}): "{response.text}".'

send_to_telegram(message, TOKEN, '-1001179024349')
print(message)
