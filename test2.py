import redis

# connect to redis server

client = redis.Redis(host='localhost',port=6379, db=0)

cursor = 0

keys = []

while True:
    cursor,partial_keys = client.scan(cursor=cursor)
    keys.extend(partial_keys)
    if cursor== 0:
        break

print([key.decode('utf-8') for key in keys])

#redis-cli EVAL "local id = redis.call('INCR', KEYS[1]); redis.call('SET', 'user:' .. id, ARGV[1]); return id;" 1 user:id "Scripted User"
#lua scripting'
