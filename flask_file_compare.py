from flask import Flask, jsonify, url_for, redirect
import file_compare_both_inputs_sorted as file
application = Flask(__name__)
list3 = []
per_page = 2
@application.route('/paginate/<number>')
def paginate(number):
    num = int(number)
    return jsonify(list3[per_page*(num-1):per_page*(num)])
@application.route('/file_compare/<file1_address>/<file2_address>')
def file_comp(file1_address, file2_address):
    global list3
    list3 = file.main_code(file1_address, file2_address)
    return redirect(url_for('paginate',number = 1))


if __name__ == "__main__":
    application.run(debug=True, host='0.0.0.0', port=5000)