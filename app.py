#/usr/bin/env python3

import os, sys, zipfile
from flask import Flask, request, send_file
import os.path

app = Flask(__name__)

VariantBase64Table = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
VariantBase64Dict = { i : VariantBase64Table[i] for i in range(len(VariantBase64Table)) }
VariantBase64ReverseDict = { VariantBase64Table[i] : i for i in range(len(VariantBase64Table)) }

def VariantBase64Encode(bs : bytes):
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

def VariantBase64Decode(s : str):
    result = b''
    blocks_count, left_bytes = divmod(len(s), 4)

    for i in range(blocks_count):
        block = VariantBase64ReverseDict[s[4 * i]]
        block += VariantBase64ReverseDict[s[4 * i + 1]] << 6
        block += VariantBase64ReverseDict[s[4 * i + 2]] << 12
        block += VariantBase64ReverseDict[s[4 * i + 3]] << 18
        result += block.to_bytes(3, 'little')

    if left_bytes == 0:
        return result
    elif left_bytes == 2:
        block = VariantBase64ReverseDict[s[4 * blocks_count]]
        block += VariantBase64ReverseDict[s[4 * blocks_count + 1]] << 6
        result += block.to_bytes(1, 'little')
        return result
    elif left_bytes == 3:
        block = VariantBase64ReverseDict[s[4 * blocks_count]]
        block += VariantBase64ReverseDict[s[4 * blocks_count + 1]] << 6
        block += VariantBase64ReverseDict[s[4 * blocks_count + 2]] << 12
        result += block.to_bytes(2, 'little')
        return result
    else:
        raise ValueError('Invalid encoding.')

def EncryptBytes(key : int, bs : bytes):
    result = bytearray()
    for i in range(len(bs)):
        result.append(bs[i] ^ ((key >> 8) & 0xff))
        key = result[-1] & key | 0x482D
    return bytes(result)

def DecryptBytes(key : int, bs : bytes):
    result = bytearray()
    for i in range(len(bs)):
        result.append(bs[i] ^ ((key >> 8) & 0xff))
        key = bs[i] & key | 0x482D
    return bytes(result)

class LicenseType:
    Professional = 1
    Educational = 3
    Persional = 4

def GenerateLicense(Type : LicenseType, Count : int, UserName : str, MajorVersion : int, MinorVersion):
    assert(Count >= 0)
    LicenseString = '%d#%s|%d%d#%d#%d3%d6%d#%d#%d#%d#' % (Type, 
                                                          UserName, MajorVersion, MinorVersion, 
                                                          Count, 
                                                          MajorVersion, MinorVersion, MinorVersion,
                                                          0,    # Unknown
                                                          0,    # No Games flag. 0 means "NoGames = false". But it does not work.
                                                          0)    # No Plugins flag. 0 means "NoPlugins = false". But it does not work.
    EncodedLicenseString = VariantBase64Encode(EncryptBytes(0x787, LicenseString.encode())).decode()
    FileName = EncodedLicenseString.replace('/','').replace('\\','')
    with zipfile.ZipFile(FileName, 'w') as f:
        f.writestr('Pro.key', data = EncodedLicenseString)
    return FileName


#@app.route('/gen')
def get_lc():
    name = request.args.get('name', '')
    version = request.args.get('ver', '')
    count = int(request.args.get('count', '1'))
    try:
        MajorVersion, MinorVersion = version.split('.')[0:2]
    except:
        return
    MajorVersion = int(MajorVersion)
    MinorVersion = int(MinorVersion)
    lc = GenerateLicense(LicenseType.Professional, count, name, MajorVersion, MinorVersion)
    return lc


#@app.route('/download/<lc>')
def download_lc(lc):
    if lc and len(lc) > 5 and os.path.exists('./' + lc):
        return send_file(lc,
            as_attachment=True,
            attachment_filename='Custom.mxtpro') 
    else:
        return "请检查用户名版本号是否正确！"


@app.route('/gen')
def get():
    lc = get_lc()
    return download_lc(lc)


@app.route('/')
def index():
    return send_file('index.html')




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

