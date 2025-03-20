# SQL vs NoSQL Comparison

| **Feature** | **SQL (Relational)** | **NoSQL** |
|------------|-----------------------|-----------|
| **Data Model** | Tables, Rows, and Columns | Key-Value, Document, Column, Graph |
| **Schema** | Fixed schema | Schema-less or dynamic |
| **ACID Compliance** | Strong consistency | Eventual consistency (in most cases) |
| **Scaling** | Vertical scaling (scale-up) | Horizontal scaling (scale-out) |
| **Joins** | Supports complex joins | No or limited support for joins |
| **Transactions** | Fully supported | Limited or no transaction support |


Here’s a well-organized `README.md` file summarizing the Redis commands and issues encountered with Docker:

---

# 🚀 Redis Docker Setup and Key Increment Example

This guide covers how to set up Redis with Docker, handle key increments, and resolve common issues.

---

## 🏆 **Setup Redis in Docker**

### 1. **Start Redis Container**
To start a Redis container:
```bash
docker run -d --name redis -p 6379:6379 redis
```

---

### 2. **Access Redis CLI**
To open the Redis CLI inside the container:
```bash
docker exec -it redis bash
redis-cli
```

---

## ✅ **Common Redis Commands**

### **Set and Get a Key**
```bash
SET user:1001 "John Doe"
GET user:1001
```

---

### **Increment a Key**
Increment a numeric key:
```bash
INCR user:number
```

---

### **Increment by a Specific Value**
Increment a key by 5:
```bash
INCRBY user:number 5
```

---

### **Set Key Value Using Incremented Value**
```bash
new_key=$(redis-cli INCR user:id)
redis-cli SET user:$new_key "John Doe"
```

---

### **Set Only If Key Does Not Exist (`SETNX`)**
```bash
SETNX user:1005 "Koenig Canada"
GET user:1005
```

Output:
```bash
"Koenig Canada"
```

If the key exists, `SETNX` returns `0`:
```bash
SETNX user:1005 "Koenig US"
(integer) 0
```

---

### **Set Multiple Keys at Once (`MSET`)**
```bash
MSET user:1006 "Koenig Canada" user:1007 "Koenig APAC" user:1008 "Koenig India"
```

Retrieve multiple keys:
```bash
MGET user:1007 user:1008
```

Output:
```bash
1) "Koenig APAC"
2) "Koenig India"
```

---

## 🔥 **Common Issues and Fixes**

### ❌ **Error: No Such Volume in Docker**
When inspecting a Docker volume:
```bash
docker volume inspect redis_data
[]
Error response from daemon: get redis_data: no such volume
```
**Solution:**  
Make sure the volume is created and properly mounted:
```bash
docker run -d --name redis -p 6379:6379 -v redis_data:/data redis
```

---

### ❌ **Bash Error: `command not found`**
Error:
```bash
root@cb985cc0f95a:/data# get user:1001
bash: get: command not found
```
**Solution:**  
Use `redis-cli` before running Redis commands:
```bash
redis-cli
GET user:1001
```

---

### ❌ **Syntax Error When Using Embedded Commands**
Error:
```bash
set user:string $(redis-cli get user:number)
(error) ERR syntax error
```
**Solution:**  
Capture the result into a variable using shell syntax:
```bash
new_key=$(redis-cli INCR user:id)
redis-cli SET user:$new_key "John Doe"
```

---

### ❌ **Unknown Command When Assigning Value**
Error:
```bash
new_key = $(redis-cli INCR user:id)
(error) ERR unknown command 'new_key'
```
**Solution:**  
Remove the `=` sign and use `$(...)` correctly:
```bash
new_key=$(redis-cli INCR user:id)
redis-cli SET user:$new_key "John Doe"
```

---

### ✅ **Working Example for Incrementing and Setting a Key**
```bash
new_key=$(redis-cli INCR user:id)
redis-cli SET user:$new_key "John Doe"
```

**Output:**
```bash
OK
```

---

## 🚀 **Best Practices**
✔️ Use `INCR` for numeric auto-increment values.  
✔️ Use `INCRBY` when you need to increment by a specific step.  
✔️ Use `SETNX` to prevent overwriting keys.  
✔️ Use `MSET` for batch updates.  

---

## 🎯 **Example of Increment by Step and Assigning Key**
```bash
new_key=$(redis-cli INCRBY user:id 5)
redis-cli SET user:$new_key "Abhi"
```

---

## ✅ **Final Output Example**
```bash
127.0.0.1:6379> INCR user:id
(integer) 1
127.0.0.1:6379> SET user:1 "John Doe"
OK
127.0.0.1:6379> GET user:1
"John Doe"
```

---

The `EVAL` command in Redis allows you to execute a Lua script directly on the Redis server. Let’s break down the command you provided:

```bash
redis-cli EVAL "local id = redis.call('INCR', KEYS[1]); redis.call('SET', 'user:' .. id, ARGV[1]); return id;" 1 user:id "Scripted User"
```

### 🧠 **Explanation**
1. **EVAL** – Executes a Lua script on the Redis server.
2. **"local id = redis.call('INCR', KEYS[1]); redis.call('SET', 'user:' .. id, ARGV[1]); return id;"** – This is the Lua script being executed.
   - `local id = redis.call('INCR', KEYS[1])`  
     - `redis.call` – Calls a Redis command within the Lua script.
     - `'INCR'` – Increments the value of the key `KEYS[1]` by 1 and returns the new value.
     - The result is stored in the local Lua variable `id`.

   - `redis.call('SET', 'user:' .. id, ARGV[1])`  
     - `redis.call` – Executes the `SET` command.
     - `'user:' .. id` – Concatenates `'user:'` with the incremented `id` value.
     - `ARGV[1]` – Takes the first argument passed after the `key` (in this case `"Scripted User"`) and assigns it to the key.

   - `return id` – Returns the newly incremented value (the new `id`).

3. **1** – This specifies the number of `KEYS` arguments that the script will receive (in this case, one key).
   - `KEYS[1] = user:id`

4. **user:id** – The key passed to the script (`KEYS[1]`).
   - This is the key that will be incremented.

5. **"Scripted User"** – The value passed as the first argument (`ARGV[1]`).
   - This will be stored in the key `user:<id>` after the `INCR` operation.

---

### ✅ **What Happens Step-by-Step**
1. The script increments the key `user:id` using `INCR`.  
   - If `user:id` = `0`, it will be incremented to `1`.  

2. The script then sets the value of the key `user:<id>` (in this case, `user:1`) to `"Scripted User"`.  

3. Finally, the script returns the new incremented value (in this case, `1`).  

---

### 🏆 **Example Output**
If `user:id` was initially `0`, after running the script:
```text
1
```
Redis will have the following key-value pairs:
```text
user:id -> 1
user:1  -> "Scripted User"
```

---

### 🚀 **Why Use Lua with `EVAL`?**
✅ Atomicity – The entire Lua script is executed atomically. This means that no other commands will interrupt the execution of the script.  
✅ Efficiency – Fewer network round-trips compared to executing multiple separate commands.  
✅ Flexibility – You can define complex logic inside the script.  

---

### ✅ **Use Cases**
- Generating unique IDs for users or objects.
- Setting related data atomically.
- Ensuring consistency and avoiding race conditions.
