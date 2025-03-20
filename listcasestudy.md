## 🚀 **Case Study: Managing a List of JSON Objects in Redis**  
In this case study, we'll design a simple **Product Management System** using Redis lists to store and manage JSON objects. Redis will act as the primary data store, and we'll perform **CRUD** (Create, Read, Update, Delete) operations on a list of product objects.

---

## 🎯 **Objective**
- Create a system to manage products using Redis lists.
- Each product will be represented as a **JSON object**.
- Perform the following operations:
  - **Create** – Add new products.
  - **Read** – Fetch list of products.
  - **Update** – Modify product details.
  - **Delete** – Remove product from the list.

---

## 🏢 **Business Context**  
An e-commerce platform wants to store product details in Redis for high-speed access and manipulation. Each product will have the following attributes:

| Field          | Type     | Description                      |
|---------------|----------|----------------------------------|
| `id`           | Integer   | Unique product ID                |
| `name`         | String    | Product name                     |
| `price`        | Float     | Product price                    |
| `category`     | String    | Product category                 |
| `stock`        | Integer   | Quantity available               |

---

## 📌 **Step 1: Data Model**
Each product will be represented as a JSON object:
```json
{
  "id": 101,
  "name": "iPhone 15",
  "price": 999.99,
  "category": "Electronics",
  "stock": 100
}
```

### ✅ Redis Key:
- Key: `products`
- Data Structure: `LIST`
- JSON objects stored as strings inside the list.

---

## 📥 **Step 2: Create (Insert Products)**
You can add products using the `RPUSH` command:

### Example:
```shell
RPUSH products '{"id": 101, "name": "iPhone 15", "price": 999.99, "category": "Electronics", "stock": 100}'
RPUSH products '{"id": 102, "name": "MacBook Pro", "price": 1999.99, "category": "Electronics", "stock": 50}'
RPUSH products '{"id": 103, "name": "Samsung Galaxy S23", "price": 899.99, "category": "Electronics", "stock": 75}'
```

### ✅ After Creation:
**List content in Redis:**
```json
[
  '{"id": 101, "name": "iPhone 15", "price": 999.99, "category": "Electronics", "stock": 100}',
  '{"id": 102, "name": "MacBook Pro", "price": 1999.99, "category": "Electronics", "stock": 50}',
  '{"id": 103, "name": "Samsung Galaxy S23", "price": 899.99, "category": "Electronics", "stock": 75}'
]
```

---

## 📤 **Step 3: Read (Get Products)**
Use `LRANGE` to retrieve products from Redis:

### Example:
Get all products:
```shell
LRANGE products 0 -1
```

**Output:**
```json
[
  "{\"id\": 101, \"name\": \"iPhone 15\", \"price\": 999.99, \"category\": \"Electronics\", \"stock\": 100}",
  "{\"id\": 102, \"name\": \"MacBook Pro\", \"price\": 1999.99, \"category\": \"Electronics\", \"stock\": 50}",
  "{\"id\": 103, \"name\": \"Samsung Galaxy S23\", \"price\": 899.99, \"category\": \"Electronics\", \"stock\": 75}"
]
```

Get the first product:
```shell
LRANGE products 0 0
```

**Output:**
```json
["{\"id\": 101, \"name\": \"iPhone 15\", \"price\": 999.99, \"category\": \"Electronics\", \"stock\": 100}"]
```

---

## 📝 **Step 4: Update (Modify Product Details)**
Use `LSET` to update a specific product by index.

### Example:
Update the price and stock of the second product (`index 1`):
```shell
LSET products 1 '{"id": 102, "name": "MacBook Pro", "price": 1899.99, "category": "Electronics", "stock": 45}'
```

### ✅ After Update:
**List content in Redis:**
```json
[
  '{"id": 101, "name": "iPhone 15", "price": 999.99, "category": "Electronics", "stock": 100}',
  '{"id": 102, "name": "MacBook Pro", "price": 1899.99, "category": "Electronics", "stock": 45}',
  '{"id": 103, "name": "Samsung Galaxy S23", "price": 899.99, "category": "Electronics", "stock": 75}'
]
```

---

## ❌ **Step 5: Delete (Remove Product)**
Use `LREM` to remove products by value.

### Example:
Remove the product with `id = 101`:
```shell
LREM products 1 '{"id": 101, "name": "iPhone 15", "price": 999.99, "category": "Electronics", "stock": 100}'
```

### ✅ After Deletion:
**List content in Redis:**
```json
[
  '{"id": 102, "name": "MacBook Pro", "price": 1899.99, "category": "Electronics", "stock": 45}',
  '{"id": 103, "name": "Samsung Galaxy S23", "price": 899.99, "category": "Electronics", "stock": 75}'
]
```

---

## 🚀 **Complete Code Example (Using Redis CLI)**
```shell
# CREATE
RPUSH products '{"id": 101, "name": "iPhone 15", "price": 999.99, "category": "Electronics", "stock": 100}'
RPUSH products '{"id": 102, "name": "MacBook Pro", "price": 1999.99, "category": "Electronics", "stock": 50}'
RPUSH products '{"id": 103, "name": "Samsung Galaxy S23", "price": 899.99, "category": "Electronics", "stock": 75}'

# READ
LRANGE products 0 -1

# UPDATE
LSET products 1 '{"id": 102, "name": "MacBook Pro", "price": 1899.99, "category": "Electronics", "stock": 45}'

# DELETE
LREM products 1 '{"id": 101, "name": "iPhone 15", "price": 999.99, "category": "Electronics", "stock": 100}'
```

---

## 📊 **Challenge**
1. Add a feature to search by product name or category.
2. Add a feature to delete products based on the `id` without knowing the index.
3. Create a backup system to store product data and reload it into Redis.

---

## ✅ **Best Practices**
✔️ Use JSON serialization/deserialization in your app layer.  
✔️ Redis is fast, but lists are not ideal for random access — consider using a Redis `HASH` for key-based access.  
✔️ Use `SCAN` or `LRANGE` for efficient retrieval of large data.  
✔️ RedisJSON module can simplify JSON storage and updates.  

---

