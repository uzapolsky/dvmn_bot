# Проверка работ на Девмане

Проект предназначен для информирования о проверенных работах на сайте [dvmn.org](https://dvmn.org/) через телеграм-бота. Для использования логгирования через телеграм-бота необходимо указать токен бота.

### Как установить

Создайте файл `.env` и поместите туда ваш телеграмм токен, чат id и devman токен.

```env
DVMN_TOKEN=
BOT_TOKEN=
CHAT_ID=
```

Python3 должен быть уже установлен.
Затем используйте `pip` (или `pip3`, если есть конфликт с Python2) для установки зависимостей:

```env
pip install -r requirements.txt
```

Чтобы запустить бота, необходимо выполнить команду:

```env
python3 bot.py
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).