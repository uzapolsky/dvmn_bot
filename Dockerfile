FROM python:3

WORKDIR /dvmn_bot
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY dvmn_bot.py ./

ENTRYPOINT [ "python", "dvmn_bot.py" ]
