### 📌 **Redis List, Set, and Sorted Set Examples**
Redis provides three key data structures — **List**, **Set**, and **Sorted Set** — each designed for specific use cases. Let’s explore them with practical examples:

---

## ✅ **1. Redis List**
A **list** in Redis is a collection of ordered elements where elements can be added or removed from both the **head** and the **tail**.

### 📚 **Commands for Lists:**
| Command | Description |
|---------|-------------|
| `LPUSH key value` | Insert value at the **head** of the list |
| `RPUSH key value` | Insert value at the **tail** of the list |
| `LPOP key` | Remove and return the first element from the list |
| `RPOP key` | Remove and return the last element from the list |
| `LRANGE key start stop` | Get elements from a list between `start` and `stop` index |
| `LLEN key` | Get the length of the list |
| `LREM key count value` | Remove the element matching value from the list |
| `LSET key index value` | Set an element at a specific index |
| `LINDEX key index` | Get the element at a specific index |

---

### 🧪 **Example 1: Adding Elements to a List**
Add elements to a list from both head and tail:
```bash
LPUSH fruits "apple"
LPUSH fruits "banana"
RPUSH fruits "orange"
```
✅ List order becomes:
```
banana, apple, orange
```

---

### 🧪 **Example 2: Get Elements from a List**
Get all elements in the list:
```bash
LRANGE fruits 0 -1
```
**Output:**
```
1) "banana"
2) "apple"
3) "orange"
```

---

### 🧪 **Example 3: Remove Elements from a List**
Remove the first element:
```bash
LPOP fruits
```
**Output:**
```
"banana"
```

✅ List becomes:
```
apple, orange
```

---

### 🧪 **Example 4: Remove Specific Elements from a List**
Remove `"apple"` from the list:
```bash
LREM fruits 1 "apple"
```

✅ List becomes:
```
orange
```

---

### 🧪 **Example 5: Get List Length**
```bash
LLEN fruits
```
**Output:**
```
(integer) 1
```

---

### 🌟 **When to Use Lists:**
✅ Maintain order of elements  
✅ Implement queues or stacks  
✅ Fast push/pop at both ends  

---

## ✅ **2. Redis Set**
A **Set** in Redis is an **unordered collection** of **unique** elements. Sets automatically remove duplicates.

### 📚 **Commands for Sets:**
| Command | Description |
|---------|-------------|
| `SADD key value` | Add value to the set |
| `SREM key value` | Remove value from the set |
| `SMEMBERS key` | Get all members of the set |
| `SCARD key` | Get the number of elements in the set |
| `SISMEMBER key value` | Check if a value exists in the set |
| `SUNION key1 key2` | Get union of two sets |
| `SINTER key1 key2` | Get intersection of two sets |
| `SDIFF key1 key2` | Get difference of two sets |

---

### 🧪 **Example 1: Adding Elements to a Set**
```bash
SADD colors "red"
SADD colors "blue"
SADD colors "green"
SADD colors "red"
```
✅ Set becomes:
```
red, blue, green
```
(Duplicates are automatically removed)

---

### 🧪 **Example 2: Get All Elements in a Set**
```bash
SMEMBERS colors
```
**Output:**
```
1) "red"
2) "blue"
3) "green"
```

---

### 🧪 **Example 3: Check Membership**
```bash
SISMEMBER colors "red"
```
**Output:**
```
(integer) 1
```

---

### 🧪 **Example 4: Remove an Element from a Set**
```bash
SREM colors "red"
```
✅ Set becomes:
```
blue, green
```

---

### 🧪 **Example 5: Set Union**
```bash
SADD set1 "a" "b" "c"
SADD set2 "c" "d" "e"
SUNION set1 set2
```
**Output:**
```
1) "a"
2) "b"
3) "c"
4) "d"
5) "e"
```

---

### 🧪 **Example 6: Set Intersection**
```bash
SINTER set1 set2
```
**Output:**
```
1) "c"
```

---

### 🧪 **Example 7: Set Difference**
```bash
SDIFF set1 set2
```
**Output:**
```
1) "a"
2) "b"
```

---

### 🌟 **When to Use Sets:**
✅ Fast membership checking  
✅ Removing duplicates  
✅ Storing unique tags or user IDs  
✅ Union and intersection operations  

---

## ✅ **3. Redis Sorted Set**
A **Sorted Set** is similar to a regular set, but each element is associated with a **score** that determines the order.

### 📚 **Commands for Sorted Sets:**
| Command | Description |
|---------|-------------|
| `ZADD key score member` | Add member to a sorted set with score |
| `ZREM key member` | Remove member from a sorted set |
| `ZRANGE key start stop [WITHSCORES]` | Get members in range |
| `ZRANK key member` | Get the rank of a member |
| `ZREVRANGE key start stop [WITHSCORES]` | Get members in reverse order |
| `ZCARD key` | Get number of elements in a sorted set |
| `ZSCORE key member` | Get score of a member |
| `ZINCRBY key increment member` | Increment score of a member |

---

### 🧪 **Example 1: Add Elements to a Sorted Set**
```bash
ZADD leaderboard 100 "Player1"
ZADD leaderboard 200 "Player2"
ZADD leaderboard 150 "Player3"
```
✅ Set becomes:
```
Player1 -> 100
Player3 -> 150
Player2 -> 200
```

---

### 🧪 **Example 2: Get Elements by Rank**
```bash
ZRANGE leaderboard 0 -1 WITHSCORES
```
**Output:**
```
1) "Player1"
2) "100"
3) "Player3"
4) "150"
5) "Player2"
6) "200"
```

---

### 🧪 **Example 3: Get Rank of a Member**
```bash
ZRANK leaderboard "Player3"
```
**Output:**
```
(integer) 1
```

---

### 🧪 **Example 4: Increment Score**
```bash
ZINCRBY leaderboard 10 "Player1"
```
✅ New score for `Player1`:
```
110
```

---

### 🧪 **Example 5: Get Elements in Descending Order**
```bash
ZREVRANGE leaderboard 0 -1 WITHSCORES
```
**Output:**
```
1) "Player2"
2) "200"
3) "Player3"
4) "150"
5) "Player1"
6) "110"
```

---

### 🌟 **When to Use Sorted Sets:**
✅ Leaderboards  
✅ Task Scheduling  
✅ Ordered Events  
✅ Priority Queues  

---

## 🔥 **Comparison of Lists, Sets, and Sorted Sets**
| Feature | List | Set | Sorted Set |
|---------|------|-----|------------|
| **Order** | Preserved | Unordered | Sorted by score |
| **Duplicates** | Allowed | Not allowed | Not allowed |
| **Lookup Time** | O(1) for head/tail | O(1) | O(log N) |
| **Use Case** | Queues, stacks | Unique elements | Leaderboards, scheduling |

---

## 🚀 **Summary:**
1. **List** → Ordered, allows duplicates → Best for queues and stacks.  
2. **Set** → Unordered, unique elements → Best for uniqueness and fast lookup.  
3. **Sorted Set** → Ordered by score → Best for leaderboards and priority handling.
