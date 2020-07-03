
#!flask/bin/python3.7

from flask import abort,request,jsonify,Flask
from baidu_index import BaiduIndex, ExtendedBaiduIndex, ResponseError
import datetime
from flask import current_app

app = Flask(__name__)

def response(code, message, error_code=0):
    response = {
                'status_code': code,
                'message': message,
                'error_code':error_code
            }
    return jsonify(response), code

def return_500_if_errors(f):
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ResponseError as e:
            return response(400, e.args[0]['message'], e.args[0]['status'])
        else:
            return response(500, 'Internal Server Error', 500)
    return wrapper

@app.route('/baidu_index/search', methods=['GET'])

@return_500_if_errors

def get_task():
    cookies = request.args.get('cookie')
    keywords = request.args.get('keywords')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    if cookies is None :
        return response(422, 'cookie is required.')
    if keywords is None:
        return response(422, 'keywords is required.')
    if start_date is None:
        return response(422, 'start_date is required.')
    if end_date is None:
         return response(422, 'end_date is required.')

    baidu_index = BaiduIndex(
        keywords=keywords.split(','),
        start_date=start_date,
        end_date=end_date,
        cookies=cookies
    )
    info = []
    for index in baidu_index.get_index():
        info.append(index)

    return jsonify({'data': info})

if __name__ == '__main__':
    app.run(debug=True, port=8899)

