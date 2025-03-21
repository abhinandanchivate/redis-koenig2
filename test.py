import redis

# connect to redis server

client = redis.Redis(host='localhost',port=6379, db=0)

keys = client.keys("*")
# client.set('name','Jhon Doe')

# value = client.get('name')

# print(value.decode('utf-8'))

print([key.decode('utf-8') for key in keys])