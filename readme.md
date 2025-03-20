# SQL vs NoSQL Comparison

| **Feature** | **SQL (Relational)** | **NoSQL** |
|------------|-----------------------|-----------|
| **Data Model** | Tables, Rows, and Columns | Key-Value, Document, Column, Graph |
| **Schema** | Fixed schema | Schema-less or dynamic |
| **ACID Compliance** | Strong consistency | Eventual consistency (in most cases) |
| **Scaling** | Vertical scaling (scale-up) | Horizontal scaling (scale-out) |
| **Joins** | Supports complex joins | No or limited support for joins |
| **Transactions** | Fully supported | Limited or no transaction support |



Error response from daemon: get redisinsight: no such volume
PS C:\Users\abhin> docker volume inspect redis_data
[]
Error response from daemon: get redis_data: no such volume
PS C:\Users\abhin> docker exec -it redis bash
root@cb985cc0f95a:/data# redis-cli
127.0.0.1:6379> exit
root@cb985cc0f95a:/data# ls
appendonlydir  commands  content  dump.rdb  logs  plugins  redisinsight.db  tutorials
root@cb985cc0f95a:/data#set user:1001 "Koenig"
root@cb985cc0f95a:/data# get user:1001
bash: get: command not found
root@cb985cc0f95a:/data# redis-cli     
127.0.0.1:6379>
root@cb985cc0f95a:/data# get user:1001
bash: get: command not found
root@cb985cc0f95a:/data#redis-cli
127.0.0.1:6379> get user:1001
"John Doe"
127.0.0.1:6379> set user:1001 "Koenig"
Invalid argument(s)
127.0.0.1:6379> set user:1001 "Koenig"
OK
127.0.0.1:6379>
127.0.0.1:6379> get user:1001
"Koenig"
127.0.0.1:6379> SETNX user:1005 "Koenig Cananda"
(integer) 1
127.0.0.1:6379> get user:1005
"Koenig Cananda"
127.0.0.1:6379> SETNX user:1005 "Koenig US""
Invalid argument(s)
127.0.0.1:6379> SETNX user:1005 "Koenig US"
(integer) 0
127.0.0.1:6379> get user:1005
"Koenig Cananda"
127.0.0.1:6379> MSET user:1006 "Koenig canada" user:1007 "koenig APAC" user:1008 "koenig India"
OK
127.0.0.1:6379> MGET user:1007 user:1008
1) "koenig APAC"
2) "koenig India"
127.0.0.1:6379> INCR user:number
(integer) 1
127.0.0.1:6379> set user:string "$user:number"
OK
127.0.0.1:6379> incrby user:number 5
(integer) 6
127.0.0.1:6379> set user:string $(redis-cli get user:number)
(error) ERR syntax error
127.0.0.1:6379> set user:string $(redis-cli get user:number)
(error) ERR syntax error
127.0.0.1:6379> multi
OK
127.0.0.1:6379(TX)> incr user:number
QUEUED
127.0.0.1:6379(TX)> set user:string "$(redis-cli get user:number)"
QUEUED
127.0.0.1:6379(TX)> incr user:id
QUEUED
127.0.0.1:6379(TX)> set user:$(redis-cli get user:id) "john doe"
QUEUED
127.0.0.1:6379(TX)> exit
root@cb985cc0f95a:/data# redis-cli
127.0.0.1:6379> incr user:id
(integer) 1
127.0.0.1:6379> set user:$(redis-cli get user:id) "john doe"
(error) ERR syntax error
127.0.0.1:6379> new_key = $(redis-cli INCR user:id)
(error) ERR unknown command 'new_key', with args beginning with: '=' '$(redis-cli' 'INCR' 'user:id)' 
127.0.0.1:6379> exit
root@cb985cc0f95a:/data# new_key = $(redis-cli INCR user:id)
bash: new_key: command not found
root@cb985cc0f95a:/data# new_key=$(redis-cli INCR user:id)
root@cb985cc0f95a:/data# redis-cli SET user:$new_key "John Doe"
OK
root@cb985cc0f95a:/data# new_key = $(redis-cli INCR user:id)
bash: new_key: command not found
root@cb985cc0f95a:/data# new_key=$(redis-cli INCR user:id)
root@cb985cc0f95a:/data# redis-cli SET user:$new_key "abhi""
>
>^C
root@cb985cc0f95a:/data# redis-cli SET user:$new_key "abhi" 
OK
root@cb985cc0f95a:/data# new_key=$(redis-cli INCRBY user:id 5)
root@cb985cc0f95a:/data# redis-cli SET user:$new_key "abhi"
OK
root@cb985cc0f95a:/data#
