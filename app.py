from flask import Flask,render_template
import redis
from flask import jsonify

app = Flask(__name__)
r = redis.StrictRedis(host='localhost', port=6379, db=0)

@app.route('/')
def fetchTopStocks():
  stocks = show_top10()
  return render_template('stocks.html', stocks=stocks)

@app.route('/search/<name>', methods=['GET'])
def get_stock_byname(name):
  print "name is",name
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
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug = True)