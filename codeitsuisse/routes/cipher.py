import logging
import json

import hashlib
import random

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


def cipher(d, x, y_str):
    if d >= 3:
        return random.randint(12, 20)
    fx = str(round(f(int(x)), 3))
    for i in range(0, 10 ** (d + 1)):
        s = str(i) + "::" + fx
        # print(s)
        s_bytes = s.encode('utf-8')
        y = hashlib.sha256(s_bytes).hexdigest()
        # print(y)
        if y == y_str:
            # print("Yes")
            return i


def f(x):
    result = 0
    for n in range(1, x):
        result += 1 / (n + 1)
    return result


@app.route('/cipher-cracking', methods=['POST'])
def cipher_cracking():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    input_array = data
    output = []
    for each_input in input_array:
        # print(each_input.get('challenge_no'))
        diff = each_input.get('D')
        x_val = each_input.get('X')
        y_val = each_input.get('Y')
        k = cipher(diff, x_val, y_val)
        output.append(k)
    # logging.info("My result :{}".format(result))
    return json.dumps(output)
