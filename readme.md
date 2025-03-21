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


Here are detailed examples for various **Redis String Commands** with explanations:

---

## 1. **APPEND** – Append a value to a key's existing value
### Syntax:
```bash
APPEND key value
```
### Example:
```bash
redis-cli SET message "Hello"
redis-cli APPEND message " World"
redis-cli GET message
```
### ✅ Output:
```text
"Hello World"
```
- If the key does not exist, `APPEND` creates the key and sets the value.

---

## 2. **GETRANGE** – Get a substring of the string value stored at a key
### Syntax:
```bash
GETRANGE key start end
```
### Example:
```bash
redis-cli SET message "Hello World"
redis-cli GETRANGE message 0 4
```
### ✅ Output:
```text
"Hello"
```
- `start` and `end` are zero-based indices.

---

## 3. **GETSET** – Set a new value and return the old value
### Syntax:
```bash
GETSET key value
```
### Example:
```bash
redis-cli SET message "Hello"
redis-cli GETSET message "Hi"
redis-cli GET message
```
### ✅ Output:
```text
"Hello"   -- Output of GETSET
"Hi"      -- Output of GET
```
- Returns the old value and sets a new value.

---

## 4. **GETBIT** – Get the bit at a specific offset
### Syntax:
```bash
GETBIT key offset
```
### Example:
```bash
redis-cli SETBIT bitkey 5 1
redis-cli GETBIT bitkey 5
```
### ✅ Output:
```text
1
```
- Sets the 5th bit of `bitkey` to `1` and retrieves its value.

---

## 5. **STRLEN** – Get the length of the value stored in a key
### Syntax:
```bash
STRLEN key
```
### Example:
```bash
redis-cli SET message "Hello World"
redis-cli STRLEN message
```
### ✅ Output:
```text
11
```
- Returns the length of the string stored at the key.

---

## 6. **DECR** – Decrement a key's integer value by 1
### Syntax:
```bash
DECR key
```
### Example:
```bash
redis-cli SET count 10
redis-cli DECR count
redis-cli GET count
```
### ✅ Output:
```text
9
```
- Decrements the value of `count` by 1.

---

## 7. **INCRBYFLOAT** – Increment a key's value by a float value
### Syntax:
```bash
INCRBYFLOAT key increment
```
### Example:
```bash
redis-cli SET balance 100.5
redis-cli INCRBYFLOAT balance 5.3
redis-cli GET balance
```
### ✅ Output:
```text
105.8
```
- Increments the value by a floating-point number.

---

## 8. **DECRBY** – Decrement a key's integer value by a specified value
### Syntax:
```bash
DECRBY key decrement
```
### Example:
```bash
redis-cli SET count 20
redis-cli DECRBY count 5
redis-cli GET count
```
### ✅ Output:
```text
15
```
- Decreases the value by a specific integer.

---

## 9. **MSETNX** – Set multiple keys only if none of the keys exist
### Syntax:
```bash
MSETNX key value [key value ...]
```
### Example:
```bash
redis-cli MSETNX user:1 "Alice" user:2 "Bob"
redis-cli MSETNX user:1 "Charlie" user:3 "David"
redis-cli GET user:1
redis-cli GET user:3
```
### ✅ Output:
```text
"Alice"   -- user:1 was already set, so MSETNX fails
(nil)     -- user:3 was not set due to failure
```
- Fails if **ANY key already exists**.

---

## 10. **SETEX** – Set a key with a value and expiration time in seconds
### Syntax:
```bash
SETEX key seconds value
```
### Example:
```bash
redis-cli SETEX session 10 "active"
redis-cli TTL session
```
### ✅ Output:
```text
10  -- Key will expire in 10 seconds
```
- Sets a key with a value and expiration in seconds.

---

## 11. **SETRANGE** – Overwrite part of a string at a specific offset
### Syntax:
```bash
SETRANGE key offset value
```
### Example:
```bash
redis-cli SET message "Hello World"
redis-cli SETRANGE message 6 "Redis"
redis-cli GET message
```
### ✅ Output:
```text
"Hello Redis"
```
- Overwrites the string starting at the specified offset.

---

## 12. **PSETEX** – Set a key with a value and expiration time in milliseconds
### Syntax:
```bash
PSETEX key milliseconds value
```
### Example:
```bash
redis-cli PSETEX session 5000 "active"
redis-cli PTTL session
```
### ✅ Output:
```text
5000   -- Key will expire in 5000 milliseconds (5 seconds)
```
- Sets a key with a value and expiration in milliseconds.

---

## ✅ **Summary of Usage**
| Command | Description |
|---------|-------------|
| `APPEND` | Append value to existing key |
| `GETRANGE` | Get substring of value |
| `GETSET` | Set new value and return old value |
| `GETBIT` | Get the bit value at offset |
| `STRLEN` | Get length of value |
| `DECR` | Decrement integer value |
| `INCRBYFLOAT` | Increment float value |
| `DECRBY` | Decrement by a specific value |
| `MSETNX` | Set multiple keys only if none exist |
| `SETEX` | Set value with expiration (seconds) |
| `SETRANGE` | Overwrite part of a string |
| `PSETEX` | Set value with expiration (milliseconds) |

---

### 🚀 **Best Practices:**
✅ Use `PSETEX` or `SETEX` for setting time-to-live (TTL).  
✅ Use `GETSET` carefully in atomic operations.  
✅ `APPEND`, `INCR`, `DECR` work well for counters and logs.  
✅ `MSETNX` is useful for setting unique values.  

Let me know if you'd like to explore more! 😎
