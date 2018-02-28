import csv
import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)

def parse_csv():
  with open('EQ270218.csv', 'rb') as csvfile:
      data = csv.reader(csvfile, delimiter=',')
      next(data, None)
      for row in data:
        code = row[0].strip()
        name =  row[1].strip()
        opening_value = row[4]
        high = row[5]
        low = row[6]
        close = float(row[7])
        stockdata = {"code": code,"name": name,"open": opening_value, "high": high,"low": low,"close": close}
        r.hmset(row[0],stockdata)
        #Build a secondary index for querying by name
        r.sadd('name:'+name,code)
        #add in zadd for top 10 query 
        r.zadd('mytop10', close, code)


def show_top10():
  top_stocks = r.zrevrange('mytop10', 0, 10)
  for code in top_stocks:
    print code
    print r.hgetall(code)

def get_stock_byname(name):
  name = name.strip()
  code = r.smembers('name:'+name)
  e = next(iter(code))
  newRes = r.hgetall(e)
  print newRes

#show_top10()

#get_stock_byname('ABB LTD.')

#parse_csv()