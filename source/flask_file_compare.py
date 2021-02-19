from flask import Flask, request, Response
import file_compare as file
import json
import secrets
import os.path
import threading
import math
from linecache import getline
import logging
total_number_of_lines = 0
application = Flask(__name__)
per_page = 200
log_format = "%(levelname)s - %(asctime)s - %(message)s"
logging.basicConfig(filename='output/logs/log_file.log', level=logging.INFO, format=log_format)
logger = logging.getLogger()


@application.route('/paginate/')
def paginate():
    request_body = request.data.decode()
    if request_body == '':
        logging.warning("body is empty, please enter input in the body")
        return Response("please enter the input body, body is empty", status=500)
    try:
        body_input = json.loads(request_body)
    except ValueError:
        logging.warning('input body is not in proper json format, input must be in {"key":"value"} format')
        return Response("input not in proper format, input must be a json", status=500)

    if "token" not in body_input and "page_number" not in body_input:
        logging.warning('from input body both token and page_number are missing, input must contain '
                        'page_number and token as keys')
        return Response("please enter token and page_number", status=500)
    if "token" not in body_input:
        logging.warning("in input body key token is missing")
        return Response("Please enter token", status=500)
    if "page_number" not in body_input:
        logging.warning("in input body key page_number is missing")
        return Response("Please enter the page number", status=500)
    code = body_input["token"]
    num = body_input["page_number"]
    try:
        num = int(num)
    except ValueError:
        logging.warning("value of key page number must be an integer")
        return Response("page number must be an integer", status=500)
    if not os.path.exists('output/' + code + '.txt'):
        logging.warning("value enter in the key token is incorrect")
        return Response("please enter the valid token", status=500)
    with open("number_of_lines/number_of_lines.txt") as f:
        ans = ""
        for i in f:
            ans = ans + i
        dictionary = json.loads(ans)
    global total_number_of_lines
    total_number_of_lines = dictionary[code]
    if total_number_of_lines % per_page == 0:
        total_number_of_pages = int(total_number_of_lines / per_page) - 1
    else:
        total_number_of_pages = int(math.floor(total_number_of_lines / per_page))
    if num > total_number_of_pages:
        logging.warning("total number of pages is " + str(total_number_of_pages)+'page number entered by the user is '
                        'greater than the total page number')
        return Response("total number of pages is " + str(total_number_of_pages), status=500)
    start_page = num * per_page
    output = []
    for i in range(per_page):
        value = getline('output/' + code + '.txt', start_page + 1)
        start_page += 1
        if value == '':
            continue
        else:
            output.append(value)
    return {'output': output}


@application.route('/file_compare/', methods=['POST'])
def file_comp():
    code = secrets.token_hex(5)
    request_body = request.data.decode()
    if request_body == '':
        logging.warning("body is empty, please enter input in the body")
        return Response("please enter the input body, body is empty", status=500)
    try:
        body_data = json.loads(request_body)
    except ValueError:
        logging.warning('input body is not in proper json format, input must be in {"key":"value"} format')
        return Response("input not in proper format, input must be a json", status=500)
    if "file1_address" not in body_data and "file2_address" not in body_data:
        logging.warning('from input body both file1_address and file2_address are missing, input must contain '
                        'file1_address and file2_address as keys')
        return Response("please enter file1_address and file2_address", status=500)
    if "file1_address" not in body_data:
        logging.warning("in input body key file1_address is missing")
        return Response("file1 address is missing", status=500)
    if "file2_address" not in body_data:
        logging.warning("in input body key file2_address is missing")
        return Response("file2 address is missing", status=500)
    file1_address = body_data["file1_address"]
    file2_address = body_data["file2_address"]
    if os.path.exists(file1_address) is False and os.path.exists(file2_address) is False:
        logging.warning("file address entered in the value of both keys i.e. file1_address and file2_address is "
                        "not exist")
        return Response("Both files are not present", status=500)
    if os.path.exists(file1_address) is False or os.path.exists(file2_address) is False:
        if os.path.exists(file1_address):
            logging.warning("file address entered in the value of key file1_address is not exist")
            return Response("file2 is not present", status=500)
        if os.path.exists(file2_address):
            logging.warning("file address entered in the value of key file2_address is not exist")
            return Response("file1 is not present", status=500)
    if file.total_threads >= 2:
        logging.warning("2 processes are already in running state, please wait for sometime")
        return Response("2 requests are already processing", status=500)
    t1 = threading.Thread(target=file.main_code, args=[file1_address, file2_address, code])
    t1.start()
    msg = str({'token': code})
    logging.info(msg)
    return {"token": code}


if __name__ == "__main__":
    application.run(debug=True, host='0.0.0.0', port=5000)