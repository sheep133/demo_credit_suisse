import logging
import json

import requests
from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


@app.route('/tic-tac-toe', methods=['GET', 'POST'])
def tic_tac_toe():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    battle_id = data.get("battleId")

    battle_event = requests.get('https://cis2021-arena.herokuapp.com/tic-tac-toe/start/%s' % battle_id)

    # result = inputValue * inputValue
    # logging.info("My result :{}".format(result))
    return json.dumps(data)