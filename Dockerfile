FROM python:3.12-slim

MAINTAINER malaohu <tua@live.cn>

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./app.py" ]

HEALTHCHECK --interval=5s --timeout=3s  --retries=3 CMD curl --fail http://localhost:5000/ || exit 1
