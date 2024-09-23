# MobaXterm-GenKey (Docker)

🔗 For the static web app version, see [MobaXterm-GenKey-Web](https://github.com/lzcapp/MobaXterm-GenKey-Web).

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/lzcapp/MobaXterm-GenKey/main.yml?style=for-the-badge)
&ensp; ![Docker Image Version](https://img.shields.io/docker/v/seeleo/mobaxterm-genkey?style=for-the-badge)
&ensp; ![Docker Image Size](https://img.shields.io/docker/image-size/seeleo/mobaxterm-genkey?style=for-the-badge) &ensp; ![Website](https://img.shields.io/website?url=https%3A%2F%2Fmobaxterm.seeleo.com%2F&style=for-the-badge&label=mobaxterm.seeleo.com)

**FOR EDUCATIONAL AND TESTING PURPOSE ONLY**

## Demo

- [mobaxterm.seeleo.com](https://mobaxterm.seeleo.com/)

## Local

**Python 3** Required

```
pip install --no-cache-dir -r requirements.txt
python app.py
```

## Docker

### Docker Hub

```
docker pull seeleo/mobaxterm-genkey:latest
docker run -d -p 5000:5000 seeleo/mobaxterm-genkey:latest
```


### Container Registry (GitHub)

```
docker pull ghcr.io/lzcapp/mobaxterm-genkey:latest
docker run -d -p 5000:5000 ghcr.io/lzcapp/mobaxterm-genkey:latest
```

## Screenshot

![1](https://github.com/malaohu/MobaXterm-GenKey/assets/12462465/fa319fe6-b75c-404f-b6fb-59290cda0d66)
![2](https://github.com/malaohu/MobaXterm-GenKey/assets/12462465/ea5387f5-144a-4b1c-a8a8-0847a0912223)

## Credits

> - https://github.com/flygon2018/MobaXterm-keygen
>   - https://github.com/malaohu/MobaXterm-GenKey
> - https://51.ruyo.net/17008.html
