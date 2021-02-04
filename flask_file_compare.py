from flask import Flask, request, Response
import file_compare as file
import json
import secrets
import os.path
import threading
import math
import logging
from linecache import getline
total_number_of_lines = 0
application = Flask(__name__)
per_page = 200

log_format = "%(levelname)s - %(asctime)s - %(message)s"
logging.basicConfig(filename='./log_file.log', level=logging.INFO, format=log_format)
logger = logging.getLogger()


@application.route('/paginate/')
def paginate():
    body_input = json.loads(request.data.decode())
    if body_input == {}:
        logging.warning("Please enter token and page number")
        return Response("Please enter token and page number", status=500)
    if "token" not in body_input:
        logging.warning("Please enter token")
        return Response("Please enter token", status=500)
    if "page_number" not in body_input:
        logging.warning("Please enter the page number")
        return Response("Please enter the page number", status=500)
    code = body_input["token"]
    num = body_input["page_number"]
    try:
        num = int(num)
    except ValueError:
        logging.warning("page number must be an integer")
        return Response("page number must be an integer", status=500)
    if not os.path.exists('output_files/' + code + '.txt'):
        logging.warning("please enter the valid token")
        return Response("please enter the valid token", status=500)
    with open("number_of_lines.txt") as f:
        ans = ""
        for i in f:
            ans = ans + i
        dictionary = json.loads(ans)
    global total_number_of_lines    
    total_number_of_lines = dictionary[code]
    if total_number_of_lines % per_page == 0:
        total_number_of_pages = int(total_number_of_lines/per_page) - 1
    else:
        total_number_of_pages = int(math.floor(total_number_of_lines/per_page))
    if num > total_number_of_pages:
        logging.warning("total number of pages are "+str(total_number_of_pages))
        return Response("total number of pages are "+str(total_number_of_pages), status=500)
    if num < 0:
        logging.warning("page number must be non-negative")
        return Response("page number must be non-negative", status=500)
    start_page = num * per_page
    output = []
    for i in range(per_page):
        output.append(getline('output_files/' + code + '.txt', start_page + 1))
        start_page += 1
    result = []
    for _ in output:
        if '<mismatch>' in _:
            sp = _.split('<')
            _ = sp[0]
            _ = json.loads(_)
            _ = (str(_) + '<mismatch>').replace(' ', '')
        elif '{' in _:
            _ = str(json.loads(_)).replace(" ", "")
        if _ == '':
            continue
        result.append(_)
    return {'output': result}


@application.route('/file_compare/', methods=['POST'])
def file_comp():
    code = secrets.token_hex(5)
    body_data = json.loads(request.data.decode())
    if body_data == {}:
        logging.warning("both file addresses are missing")
        return Response("both file addresses are missing", status=500)
    if "file1_address" not in body_data:
        logging.warning("file1 address is missing")
        return Response("file1 address is missing", status=500)
    if "file2_address" not in body_data:
        logging.warning("file2 address is missing")
        return Response("file2 address is missing", status=500)
    file1_address = body_data["file1_address"]
    file2_address = body_data["file2_address"]
    if os.path.exists(file1_address) is False and os.path.exists(file2_address) is False:
        logging.warning("Both files are not present")
        return Response("Both files are not present", status=500)
    if os.path.exists(file1_address) is False or os.path.exists(file2_address) is False:
        if os.path.exists(file1_address):
            logging.warning("file2 is not present")
            return Response("file2 is not present", status=500)
        if os.path.exists(file2_address):
            logging.warning("file1 is not present")
            return Response("file1 is not present", status=500)
    if file.total_threads >= 2:
        logging.warning("2 requests are already processing")
        return Response("2 requests are already processing", status=500)
    t1 = threading.Thread(target=file.main_code, args=[file1_address, file2_address, code])
    t1.start()
    msg = str({'token': code})
    logging.info(msg)
    return {"token": code}


if __name__ == "__main__":
    application.run(debug=True, host='0.0.0.0', port=5000)

