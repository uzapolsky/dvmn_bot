FROM python:3

WORKDIR /dvmn_bot
COPY requirements.txt .env dvmn_bot.py ./
RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "dvmn_bot.py" ]