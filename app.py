from flask import Flask,render_template,jsonify
import redis 

application = Flask(__name__)
application.config.from_pyfile('config.cfg')
r = redis.StrictRedis(host=application.config['REDIS_HOST'], port=application.config['REDIS_PORT'], db=0)

@application.route('/')
def fetchTopStocks():
  stocks = show_top10()
  return render_template('stocks.html', stocks=stocks)

@application.route('/search/<name>', methods=['GET'])
def get_stock_byname(name):
  name = name.strip()
  code = r.smembers('name:'+name)
  e = next(iter(code))
  stock = r.hgetall(e)
  stocks = []
  stocks.append(stock)
  return render_template('search.html' , filterStocks=stocks)

def show_top10():
  top_stocks = r.zrevrange('mytop10', 0, 10)
  stocks = []
  for code in top_stocks:
    stock = r.hgetall(code) 
    stocks.append(stock)
  return stocks

if __name__ == '__main__':
  application.run(host='0.0.0.0')