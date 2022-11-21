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
urls = [
    f"https://bill.bezlimit.ru/log/other/switch-to-cloud-{''.join(now)}.log",
    f"https://bill.bezlimit.ru/log/other/switch-from-cloud-{''.join(now)}.log",
    f"https://bill.bezlimit.ru/log/other/cloud-import-{''.join(now)}.log"
]
message = ''
counter = 0
for url in urls:
    res = requests.post(url, headers={
        "Authorization": "Basic d2V0ZXI6VjdCbjYzeGN2MTJA",
        "Host": "bill.bezlimit.ru",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
                "image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Content-Type": "application/json-patch+json"})
    # print(res.text, '--------------------------------------------------------------------')
    if res.status_code == 200:
        if counter == 0:
            message = f'Отчет по проверке WA в Whatsapp Cloud - [{datetime.date.today()}]({url}).'
            if 'Exception' in res.text.split('.')[2]:
                message += f"Проверка номеров завершилась с ошибкой: {res.text.split('.')[2]}"
            else:
                numbers_amount = res.text.split('.')[1]
                message += numbers_amount
                registered_numbers = res.text.split('.')[2].count('WhatsApp зарегистрирован')
                message += f'\nНомера с Whatsapp: {registered_numbers}'
                error_numbers = res.text.split('.')[2].count('Получен неизвестный ответ')
                message += f'\nНомеров с ошибкой проверки: {error_numbers}'
                to_cloud_numbers = res.text.split('.')[2].count('перемещен в облако')
                message += f'\nНомеров перемещенных в Cloud: {to_cloud_numbers}'
                cancelled_numbers = res.text.split('.')[2].count('Запрещено проверять этот номер на наличие WhatsApp')
                message += f'\nНомера с запретом проверки: {cancelled_numbers}'
        elif counter == 1:
            message = f'Отчет по проверке WA в Cloud - [{datetime.date.today()}]({url}).'
            if 'Exception' in res.text.split('.')[2]:
                message += f"Проверка номеров завершилась с ошибкой: {res.text.split('.')[2]}"
            else:
                numbers_amount = res.text.split('.')[1]
                message += numbers_amount
                non_registered_numbers = res.text.split('.')[2].count('WhatsApp отсутствует')
                non_registered_numbers += res.text.split('.')[2].count('WhatsApp не зарегистрирован')
                message += f'\nНомеров без Whatsapp: {non_registered_numbers}'
                error_numbers = res.text.split('.')[2].count('Получен неизвестный ответ')
                message += f'\nНомеров с ошибкой проверки: {error_numbers}'
                to_cloud_numbers = res.text.split('.')[2].count('перемещен в облако')
                message += f'\nНомеров перемещенных в Whatsapp Cloud: {to_cloud_numbers}'
                cancelled_numbers = res.text.split('.')[2].count('Запрещено проверять этот номер на наличие WhatsApp')
                message += f'\nНомера с запретом проверки: {cancelled_numbers}'
        elif counter == 2:
            message = f'Отчет по распределению номеров Сloud - [{datetime.date.today()}]({url}).'
            if 'Exception' in res.text:
                message += f"Проверка номеров завершилась с ошибкой: {res.text}"
            else:
                whatsapp_cloud = res.text.count('(WhatsApp Cloud)')
                regular_cloud = res.text.count('(Cloud)')
                numbers_amount = int(whatsapp_cloud) + int(regular_cloud)
                message += f'\nНайдено {numbers_amount} номеров с просроченным сроком годности'
                message += f'\nНомеров перемещенных в Whatsapp Cloud: {whatsapp_cloud}'
                message += f'\nНомеров перемещенных в Cloud: {regular_cloud}'
        if 'Выход' not in res.text:
            message += '\nСкрипт не завершил работу польностью.'
    else:
        if counter == 0:
            message = f'Не удалось сформировать отчет по проверке WA в Whatsapp Cloud - [{datetime.date.today()}]({url}).' \
                      f'\nОтвет метода логирования при запросе: {res.status_code}'

        if counter == 1:
            message = f'Не удалось сформировать отчет по проверке WA в Cloud - [{datetime.date.today()}]({url}).' \
                      f'\nОтвет метода логирования при запросе: {res.status_code}'

        if counter == 2:
            message = f'Отчет по распределению номеров Сloud - [{datetime.date.today()}]({url}).' \
                      f'\nОтвет метода логирования при запросе: {res.status_code}'
    counter += 1
    send_to_telegram(message, TOKEN, '-1001179024349')
    print(message)
