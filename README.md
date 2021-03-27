# MobaXterm-GenKey
你懂的！！

## 本地启动
需要安装Python3!!!
```
pip install --no-cache-dir -r requirements.txt
python app.py
```

## Docker
```
docker pull malaohu/mobaxterm-genkey
docker run -d -p 5000:5000 malaohu/mobaxterm-genkey
```


## 使用方法
### 生成LC

name -- 自定义用户名
ver  -- 软件版本

访问：IP:5000/gen/?name=malaohu&ver=21.0
接口返回一串字符串

### 下载文件
访问：IP:5000/download/xxxxxxx
xxxxxxx 为上面生成的字符串

### 生成&下载
IP:5000/?name=malaohu&ver=21.0

### 激活方式
直接放到软件目录即可！



核心内容来自：https://github.com/flygon2018/MobaXterm-keygen
