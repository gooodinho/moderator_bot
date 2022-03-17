FROM python:3.8

WORKDIR /axelar-mod-bot
COPY requirements.txt /axelar-mod-bot
RUN pip install -r requirements.txt
COPY . /axelar-mod-bot