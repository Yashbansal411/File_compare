from flask import Flask, request, Response
import file_compare as file
import json
import secrets
import os.path
import threading
import math
from linecache import getline
import logging
import traceback
import sys

total_number_of_lines = 0
application = Flask(__name__)
per_page = 200
log_format = "%(levelname)s - %(asctime)s - %(message)s"
if os.path.isdir("output/logs") is False:
    os.system("mkdir output/logs")
logging.basicConfig(filename='output/logs/log_file.log', level=logging.INFO, format=log_format)
logger = logging.getLogger()


def get_file_length(code):
    f = open('output/' + code + '.txt', 'r')
    total_lines = 0
    for i in f:
        total_lines += 1
    f.close()
    file.persist_file_length(total_lines, code)
    return total_lines


@application.route('/paginate/')
def paginate():
    request_body = request.data.decode()
    if request_body == '':
        try:
            json.loads(request_body)
        except ValueError:
            tb = traceback.format_exc()
            logging.warning(tb)
            return Response("please enter the input body, body is empty", status=500)
    try:
        body_input = json.loads(request_body)
    except ValueError:
        tb = traceback.format_exc()
        logging.warning(tb)
        return Response("input not in proper format, input must be a json", status=500)

    if "token" not in body_input and "page_number" not in body_input:
        try:
            body_input["token"]
        except KeyError:
            tb = traceback.format_exc()
            logging.warning(tb)
        try:
            body_input["page_number"]
        except KeyError:
            tb = traceback.format_exc()
            logging.warning(tb)
        return Response("please enter token and page_number", status=500)
    if "token" not in body_input:
        try:
            body_input["token"]
        except KeyError:
            tb = traceback.format_exc()
            logging.warning(tb)
        return Response("Please enter token", status=500)
    if "page_number" not in body_input:
        try:
            body_input["page_number"]
        except KeyError:
            tb = traceback.format_exc()
            logging.warning(tb)
        return Response("Please enter the page number", status=500)
    code = body_input["token"]
    num = body_input["page_number"]
    try:
        num = int(num)
    except ValueError:
        tb = traceback.format_exc()
        logging.warning(tb)
        return Response("page number must be an integer", status=500)
    if not os.path.exists('output/' + code + '.txt'):
        try:
            open('output/' + code + '.txt')
        except FileNotFoundError:
            tb = traceback.format_exc()
            logging.warning(tb)
        return Response("please enter the valid token", status=500)
    with open("output/number_of_lines/number_of_lines.txt") as f:
        ans = ""
        for i in f:
            ans = ans + i
        dictionary = json.loads(ans)
    global total_number_of_lines
    try:
        total_number_of_lines = dictionary[code]
    except KeyError:
        t2 = threading.Thread(target=get_file_length, args=[code])
        t2.start()
        tb = traceback.format_exc()
        logging.warning(tb)
        return Response("Total number of lines of token " + code + " is not present", status=500)
    if total_number_of_lines % per_page == 0:
        total_number_of_pages = int(total_number_of_lines / per_page) - 1
    else:
        total_number_of_pages = int(math.floor(total_number_of_lines / per_page))
    if num > total_number_of_pages:
        try:
            raise ValueError
        except:
            tb = traceback.format_exc()
            logging.warning(
                tb + " total number of pages is " + str(total_number_of_pages) + ' page number entered by the user is '
                                                                                 'greater than the total number of pages')
        return Response("total number of pages is " + str(total_number_of_pages), status=500)
    start_page = num * per_page
    output = []
    for i in range(per_page):
        value = getline('output/' + code + '.txt', start_page + 1)
        start_page += 1
        if value == '':
            continue
        else:
            value = value.replace('\n', '')
            value = value.replace("\\", '')
            output.append(value)
    return {'output': output}


@application.route('/file_compare/', methods=['POST'])
def file_comp():
    code = secrets.token_hex(5)
    request_body = request.data.decode()
    if request_body == '':
        try:
            json.loads(request_body)
        except ValueError:
            tb = traceback.format_exc()
            logging.warning(tb)
        return Response("please enter the input body, body is empty", status=500)
    try:
        body_data = json.loads(request_body)
    except ValueError:
        try:
            json.loads(request_body)
        except:
            tb = traceback.format_exc()
            logging.warning(tb)
        return Response("input not in proper format, input must be a json", status=500)
    if "file1_address" not in body_data and "file2_address" not in body_data:
        try:
            body_data["file1_address"]
        except KeyError:
            tb = traceback.format_exc()
            logging.warning(tb)
        try:
            body_data["file2_address"]
        except KeyError:
            tb = traceback.format_exc()
            logging.warning(tb)
        return Response("please enter file1_address and file2_address", status=500)
    if "file1_address" not in body_data:
        try:
            body_data["file1_address"]
        except KeyError:
            tb = traceback.format_exc()
            logging.warning(tb)
        return Response("file1 address is missing", status=500)
    if "file2_address" not in body_data:
        try:
            body_data["file2_address"]
        except KeyError:
            tb = traceback.format_exc()
            logging.warning(tb)
        return Response("file2 address is missing", status=500)
    file1_address = "input/" + body_data["file1_address"]
    file2_address = "input/" + body_data["file2_address"]
    if os.path.exists(file1_address) is False and os.path.exists(file2_address) is False:
        try:
            open(file1_address)
        except FileNotFoundError:
            tb = traceback.format_exc()
            logging.warning(tb)
        try:
            open(file2_address)
        except FileNotFoundError:
            tb = traceback.format_exc()
            logging.warning(tb)
        return Response("Both files are not present", status=500)
    if os.path.exists(file1_address) is False:
        try:
            open(file1_address)
        except FileNotFoundError:
            tb = traceback.format_exc()
            logging.warning(tb)
        return Response("file1 is not present", status=500)
    if os.path.exists(file2_address) is False:
        try:
            open(file2_address)
        except FileNotFoundError:
            tb = traceback.format_exc()
            logging.warning(tb)
        return Response("file2 is not present", status=500)
    if file.total_threads >= 2:
        try:
            raise ValueError
        except ValueError:
            tb = traceback.format_exc()
            logging.warning(tb + " 2 processes are already in running state, please wait for sometime")
        return Response("2 requests are already processing", status=500)
    t1 = threading.Thread(target=file.main_code, args=[file1_address, file2_address, code])
    t1.start()
    msg = str({'token': code})
    logging.info(msg)
    return {"token": code}


if __name__ == "__main__":
    application.run(debug=True, host='0.0.0.0', port=5000)
