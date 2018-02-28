ZADD mysales 2200 Sunsui 1800 MicroSoft 2500 LG

ZADD mysales 1556 Samsung 2000 Nokis 1800 Micromax

ZREVRANGE mysales 0 10

zscan mysales 0 match Nokis*

SMEMBERS name_ABB LTD.

-----------------------------------------------------------------------------
hmset 500002 name ABB LTD. close 1515.15

hmset code:500002 name ABB LTD. close 1515.15