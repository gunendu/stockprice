from flask import Flask,render_template,jsonify
import redis 

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
r = redis.StrictRedis(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'], db=0)

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
  app.run(debug = True)