from flask import Flask, jsonify, url_for, redirect, request
import file_compare_both_inputs_sorted as file
import json
application = Flask(__name__)
dictionary = {}
per_page = 2
@application.route('/paginate/', methods=["POST"])
def paginate():
    body_input = json.loads(request.data.decode())
    file1_address = body_input["file1_address"]
    file2_address = body_input["file2_address"]
    num = int(body_input["page_number"])
    #return jsonify(list3[per_page*(num-1):per_page*(num)])
    try:
        dictionary[file1_address+file2_address]
    except KeyError:
        return "The output for the files you are looking for is not available"
    return jsonify(dictionary[file1_address+file2_address][per_page*(num-1):per_page*(num)])
@application.route('/file_compare/', methods=['POST'])
def file_comp():
    body_data = json.loads(request.data.decode())
    file1_address = body_data["file1_address"]
    file2_address = body_data["file2_address"]
    list3 = file.main_code(file1_address, file2_address)
    dictionary[file1_address+file2_address] = list3
    return jsonify(dictionary[file1_address+file2_address])


if __name__ == "__main__":
    application.run(debug=True, host='0.0.0.0', port=5000)