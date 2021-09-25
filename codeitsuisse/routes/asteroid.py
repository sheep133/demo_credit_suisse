import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


def scoring(input_string):
    s = input_string
    score_list = [0.0] * len(s)

    for origin in range(int(len(s)/2-len(s)/5), int(len(s)/2+len(s)/5)):
        score = 0
        left_queue = []
        right_queue = []
        for pointer in range(1, len(s)):

            # if left_flag:
            #     left_pointer = new_left_pointer
            #     left_flag = False
            # else:
            #     left_pointer = origin - pointer
            # if right_flag:
            #     right_pointer = new_right_pointer
            #     right_flag = False
            # else:
            #     right_pointer = origin + pointer
            #
            # if left_pointer >= 0 and right_pointer < len(s):
            #     if s[left_pointer] == s[right_pointer]:
            #         current_char = s[left_pointer]
            #         left_queue.append(s[left_pointer])
            #         right_queue.append(s[right_pointer])
            #         # print(left_pointer, right_pointer)
            #     elif s[left_pointer] != current_char:
            #         while right_pointer < len(s) and s[right_pointer] == current_char:
            #             right_queue.append(s[right_pointer])
            #             right_pointer += 1
            #             right_flag = True
            #     elif s[right_pointer] != current_char:
            #         while left_pointer >= 0 and s[left_pointer] == current_char:
            #             left_queue.append(s[left_pointer])
            #             left_pointer -= 1
            #             left_flag = True

        # print(left_queue)
        # print(right_queue)

            left_pointer = origin - pointer
            right_pointer = origin + pointer

            if left_pointer >= 0:
                left_queue.append(s[left_pointer])
            if right_pointer < len(s):
                right_queue.append(s[right_pointer])

        # print(left_queue, right_queue)

        current_char = s[origin]

        while len(left_queue) != 0 or len(right_queue) != 0:
            left_count = 0
            right_count = 0
            while len(left_queue) != 0 and left_queue[0] == current_char:
                left_queue.pop(0)
                left_count += 1
            while len(right_queue) != 0 and right_queue[0] == current_char:
                right_queue.pop(0)
                right_count += 1
            # print(left_queue, right_queue, left_count, right_count)
            dummy = left_count + right_count
            if dummy <= 6:
                score += dummy * 1
            elif 7 <= dummy < 10:
                score += dummy * 1.5
            else:
                score += dummy * 2

            if left_queue and right_queue and left_queue[0] == right_queue[0]:
                current_char = left_queue[0]
            else:
                break

        score_list[origin] = score

    return max(score_list)+1, score_list.index(max(score_list)) + 1


@app.route('/asteroid', methods=['POST'])
def evaluate_asteroid():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    input_data = data.get("test_cases")
    output = []
    for each_input in input_data:
        each_output = dict()
        score, origin = scoring(each_input)
        each_output["input"] = each_input
        each_output["score"] = score
        each_output["origin"] = origin
        output.append(each_output)

    real_output = {'test_cases': output}
    return json.dumps(output)

    # inputValue = data.get("input")
    # result = inputValue * inputValue
    # logging.info("My result :{}".format(result))
    # return json.dumps(result)
