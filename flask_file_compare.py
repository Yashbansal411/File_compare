from flask import Flask, jsonify, request
import file_compare_both_inputs_sorted as file
import json, secrets, os.path, time
from linecache import getline
application = Flask(__name__)
per_page = 2
@application.route('/paginate/', methods=["POST"])
def paginate():
    body_input = json.loads(request.data.decode())
    try:
        code = body_input["code"]
        num = body_input["page_number"]
    except KeyError:
        return "Please insert the code and page_number"
    try:
        num = int(num)
    except ValueError:
        return "page number must be an integer"
    start_page = num*per_page
    output = []
    if not os.path.exists('output_files/'+code+'.txt'): # to check file exists or not
        return "please enter the valid code"

    for i in range(per_page):
        output.append(getline('output_files/'+code+'.txt', start_page+1))
        start_page += 1
    return jsonify(output)


@application.route('/file_compare/', methods=['POST'])
def file_comp():
    start_time = time.time()
    code = secrets.token_hex(5)
    body_data = json.loads(request.data.decode())
    try:
        file1_address = body_data["file1_address"]
        file2_address = body_data["file2_address"]
    except KeyError:
        return "file address is missing"
    try:
        list3 = file.main_code(file1_address, file2_address)
    except (FileNotFoundError, IOError):
        return "file address is incorrect"
    file.listtofile(list3,code)
    time_of_execution = time.time()-start_time
    return jsonify([code, time_of_execution])


if __name__ == "__main__":
    application.run(debug=True, host='0.0.0.0', port=5000)