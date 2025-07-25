#!/usr/bin/env python3

import os
import sys
import zipfile
import io  # <--- 引入 io 模块，用于内存操作
from flask import Flask, request, send_file, make_response

app = Flask(__name__)

# --- 核心加解密和编码逻辑 (这部分无需改动) ---
VariantBase64Table = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
VariantBase64Dict = {i: VariantBase64Table[i] for i in range(len(VariantBase64Table))}
VariantBase64ReverseDict = {VariantBase64Table[i]: i for i in range(len(VariantBase64Table))}

def VariantBase64Encode(bs: bytes):
    result = b''
    blocks_count, left_bytes = divmod(len(bs), 3)
    for i in range(blocks_count):
        coding_int = int.from_bytes(bs[3 * i:3 * i + 3], 'little')
        block = VariantBase64Dict[coding_int & 0x3f]
        block += VariantBase64Dict[(coding_int >> 6) & 0x3f]
        block += VariantBase64Dict[(coding_int >> 12) & 0x3f]
        block += VariantBase64Dict[(coding_int >> 18) & 0x3f]
        result += block.encode()
    if left_bytes == 0:
        return result
    elif left_bytes == 1:
        coding_int = int.from_bytes(bs[3 * blocks_count:], 'little')
        block = VariantBase64Dict[coding_int & 0x3f]
        block += VariantBase64Dict[(coding_int >> 6) & 0x3f]
        result += block.encode()
        return result
    else:
        coding_int = int.from_bytes(bs[3 * blocks_count:], 'little')
        block = VariantBase64Dict[coding_int & 0x3f]
        block += VariantBase64Dict[(coding_int >> 6) & 0x3f]
        block += VariantBase64Dict[(coding_int >> 12) & 0x3f]
        result += block.encode()
        return result

def EncryptBytes(key: int, bs: bytes):
    result = bytearray()
    for i in range(len(bs)):
        result.append(bs[i] ^ ((key >> 8) & 0xff))
        key = result[-1] & key | 0x482D
    return bytes(result)

class LicenseType:
    Professional = 1
    Educational = 3
    Persional = 4

# --- 重构后的核心功能 ---
def GenerateLicenseInMemory(Type: LicenseType, Count: int, UserName: str, MajorVersion: int, MinorVersion: int):
    """
    重构后的函数：在内存中生成许可证 ZIP 文件，并返回一个 BytesIO 对象。
    不再向磁盘写入任何文件。
    """
    assert Count >= 0
    LicenseString = '%d#%s|%d%d#%d#%d3%d6%d#%d#%d#%d#' % (
        Type, UserName, MajorVersion, MinorVersion,
        Count,
        MajorVersion, MinorVersion, MinorVersion,
        0, 0, 0
    )
    EncodedLicenseString = VariantBase64Encode(EncryptBytes(0x787, LicenseString.encode())).decode()

    # 1. 创建一个内存中的二进制流对象
    memory_file = io.BytesIO()

    # 2. 像操作普通文件一样，在内存中创建 ZIP 归档
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('Pro.key', data=EncodedLicenseString)

    # 3. 将内存流的指针移到开头，以便 send_file 从头读取
    memory_file.seek(0)

    return memory_file


# --- 重构后的 Flask 路由 ---
@app.route('/')
def index():
    """提供一个简单的使用说明页面"""
    return send_file('index.html')


@app.route('/gen')
def generate_and_download_license():
    """
    一个统一的路由，处理参数、生成许可证并直接提供下载。
    """
    # 1. 获取和验证参数
    name = request.args.get('name')
    version = request.args.get('ver')
    
    if not name or not version:
        return make_response("错误：必须提供 'name' 和 'ver' 参数 (例如: /gen?name=MyName&ver=25.2)", 400)

    try:
        count = int(request.args.get('count', '1'))
        MajorVersion, MinorVersion = version.split('.')[0:2]
        MajorVersion = int(MajorVersion)
        MinorVersion = int(MinorVersion)
    except (ValueError, IndexError):
        return make_response("错误：版本号 'ver' 格式不正确，应为 '主版本号.次版本号' (例如: 25.2)", 400)

    # 2. 在内存中生成许可证文件
    license_file_stream = GenerateLicenseInMemory(
        LicenseType.Professional, count, name, MajorVersion, MinorVersion
    )

    # 3. 使用 send_file 直接发送内存中的文件流
    return send_file(
        license_file_stream,
        mimetype='application/zip',
        as_attachment=True,
        download_name='Custom.mxtpro'  # <--- 使用了正确的参数名
    )


if __name__ == '__main__':
    # 建议开启 debug=True 进行开发调试，部署时设为 False
    app.run(host='0.0.0.0', port=5000, debug=True)

