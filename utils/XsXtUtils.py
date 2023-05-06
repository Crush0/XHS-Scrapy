import base64
import json
import math
import random
import urllib.parse

import execjs
import os
import sys

dir_name = os.path.split(os.path.abspath(sys.argv[0]))[0]
JS_FILE = os.path.join(dir_name, 'js', 'sign.js')
MCR_FILE = os.path.join(dir_name, 'js', 'mcr.js')
COMMON_JS = os.path.join(dir_name, 'js', 'commonId.js')
if not os.path.exists(JS_FILE):
    print(f'{JS_FILE} Err:文件不存在')
if not os.path.exists(COMMON_JS):
    print(f'{COMMON_JS} Err:文件不存在')
js_body = open(JS_FILE, 'r').read()
common_js_body = open(COMMON_JS, 'r').read()
mcr_js_body = open(MCR_FILE, 'r').read()
index = 1


def sign(url, data):
    c = execjs.get()
    ctx = c.compile(js_body)
    if data == {}:
        result = ctx.eval(f'sign("{url}")')
    else:
        result = ctx.eval(f'sign("{url}",{data})')
    return {'x-t': result['X-t'], 'x-s': result['X-s']}


def trace():
    re_ = 'abcdef0123456789'
    je = 16
    e = ''
    for t in range(0, 16):
        e += re_[math.floor(random.random() * je)]
    return {"x-b3-traceid": e}


def encode_utf8(string):
    utf8_bytes = string.encode('utf-8')
    encoded_bytes = []
    for byte in utf8_bytes:
        if byte < 0x80:
            encoded_bytes.append(byte)
        else:
            encoded_bytes.append(0xc0 | (byte >> 6))
            encoded_bytes.append(0x80 | (byte & 0x3f))
    return encoded_bytes


def mcr(e):
    ctx = execjs.compile(mcr_js_body)
    return ctx.eval(f'mcrFun("{e}")')


def XCommonId(cookie_a1='', xt='', xs=''):
    global index
    e = {
        "s0": 5,
        "s1": '',
        'x0': '1',
        "x1": "3.2.0",
        'x2': 'Windows',
        'x3': 'xhs-pc-web',
        'x4': '2.0.3',
        'x5': cookie_a1,
        'x6': int(xt),
        'x7': xs,
        'x8': 'I38rHdgsjopgIvesdVwgIC+oIELmBZ5e3VwXLgFTIxS3bqwErFeexd0ekncAzMFYnqthIhJeSnMDKutRI3KsYorWHPtGrbV0P9WfIi/eWc6eYqtyQApPI37ekmR1QL+5Ii6sdnosjoT5yqtXqqwYrBqoIx++GDi/sVtkIx0sxuwr4qtiIkrwIi/skcc3ICLfI3Oe0utl20DZsL5eDSJejVw0IieexVwL+PtorqthPleekmW4Ix+iIhrRzVwgKPtYI3QPorKe6qthIx/s6VtoIiMoIiEge96eSdckrfvsjutKrZgefcr9gfKeYcPsIxKefVtzIE6edutholFIQdLnIx5s3qtRnc7eVfG+IkcwIiHt40bMIvhqtS8gIiifpVwAICHVJo3eSpeekPtVIx3e0jH=',
    }
    r = f'{xt}{xs}{e["x8"]}'
    e.update({'x9': mcr(r)})
    e.update({'x10': index})
    index += 1
    ctx = execjs.compile(common_js_body)
    json_str = json.dumps(e).replace(' ', '')
    return {'x-s-common': ctx.eval(f'b64Encode({encode_utf8(json_str)})')}
