
#!flask/bin/python3.7

from flask import abort,request,jsonify,Flask
from baidu_index import BaiduIndex, ExtendedBaiduIndex
import datetime

app = Flask(__name__)

@app.route('/baidu_index/search', methods=['GET'])
def get_task():
    cookies = request.args.get('cookie')
    keywords = [request.args.get('keywords')]
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    if cookies is None :
        abort(422, {'message': 'Cookie is required.'})
    if keywords is None:
        abort(422, {'message': 'keywords is required.'})
    if start_date is None:
        abort(422, {'message': 'start_date is required.'})
    if end_date is None:
        abort(422, {'message': 'end_date is required.'})

    baidu_index = BaiduIndex(
        keywords=keywords,
        start_date=start_date,
        end_date=end_date,
        cookies=cookies
    )
    info = []
    for index in baidu_index.get_index():
        info.append(index)

    return jsonify({'data': info})

if __name__ == '__main__':
    app.run(debug=True)

