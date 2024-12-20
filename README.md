# rita_bot

rita_bot

# Создаем виртуальное окружение

python3 -m venv repon

# Активируем виртуальное окружение

source repon/bin/activate

# Устанавливаем зависимости

pip install --upgrade pip
pip install -r requirements.txt

pip3 install python-telegram-bot==20.0 apscheduler
brew install python-telegram-bot==20.0 apscheduler

pip3 freeze > requirements.txt

pip3 install -r requirements.txt

pip install python-telegram-bot --upgrade
pip list

 ###
Для того чтобы бот обрабатывал все сообщения в чатах, нужно отключить “Privacy Mode” в настройках бота. Вот как это сделать:
	1.	Перейдите в чат с @BotFather.
	2.	Введите команду /mybots и выберите вашего бота.
	3.	Нажмите “Bot Settings” → “Group Privacy”.
	4.	Выберите “Turn off”. Это отключит режим приватности, и ваш бот сможет видеть все сообщения в группах.

Как отключить постоянные запросы

Если вы не хотите, чтобы бот делал такие запросы, можно перейти на Webhook, где Telegram отправляет обновления вашему серверу только по мере их появления.

Преимущества Webhook:
	1.	Меньше запросов к API Telegram.
	2.	Экономия ресурсов, особенно на хостинге с ограничениями.

Как настроить Webhook:
	1.	Запустите сервер, доступный через интернет (например, с помощью ngrok или хостинга).
	2.	Настройте Webhook с помощью метода setWebhook, указав URL вашего сервера.

Пример команды для настройки Webhook:
curl -F "url=https://your-server.com/botTOKEN" https://api.telegram.org/botTOKEN/setWebhook

Настройка бота для Webhook:

Вместо run_polling используйте run_webhook. Пример:
application.run_webhook(
    listen="0.0.0.0",
    port=8443,
    url_path="bot",
    webhook_url="https://your-server.com/bot"
)

CHECK http://127.0.0.1:5555/
CHECK http://127.0.0.1:5555/webhook
CHECK https://rita-bot.onrender.com
CHECK https://rita-bot.onrender.com/webhook

CHECK https://dashboard.uptimerobot.com/