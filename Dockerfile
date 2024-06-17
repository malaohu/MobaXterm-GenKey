FROM python:3.12-alpine

MAINTAINER malaohu <tua@live.cn>

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./app.py" ]
