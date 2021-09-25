import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


def optimal_position(input_string):
    count = [0] * len(input_string)

    for i in range(len(input_string)):
        dummy_count = 0
        for j in range(len(input_string)):
            left = i - j
            right = i + j
            if left >= 0 and right < len(input_string):
                if input_string[left] == input_string[right]:
                    dummy_count += 1

            if dummy_count >= count[i]:
                count[i] = dummy_count

    return count.index(max(count))


def scoring(input_string, position):
    score = 0
    asteroid_type = [0] * 26
    asteroid_type[ord(input_string[position]) - 65] += 1
    for j in range(len(input_string)):
        left = position - j
        right = position + j
        if 0 <= left != right < len(input_string):
            if input_string[left] == input_string[right]:
                char = input_string[left]
                asteroid_type[ord(char)-65] += 2
                print(left, right, char)
    # print(asteroid_type)

    for asteroid in asteroid_type:
        if asteroid <= 6:
            score += asteroid * 1
        elif 6 <= asteroid < 10:
            score += asteroid * 1.5
        else:
            score += asteroid * 2

    return score


@app.route('/asteroid', methods=['POST'])
def evaluate_asteroid():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    input_data = data.get("input")
    output = []
    for each_input in input_data:
        each_output = dict()
        pos = optimal_position(each_input)
        each_output["input"] = each_input
        each_output["score"] = scoring(each_input, pos)
        each_output["origin"] = pos
        output.append(each_output)

    real_output = dict(output=output)
    return json.dumps(real_output)

    # inputValue = data.get("input")
    # result = inputValue * inputValue
    # logging.info("My result :{}".format(result))
    # return json.dumps(result)
