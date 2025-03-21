import redis
import json

# Connect to Redis
r = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

# Function to delete product by id
def delete_product_by_id(key, product_id):
    # Step 1: Get all products from the list
    products = r.lrange(key, 0, -1)
    
    # Step 2: Deserialize JSON strings to objects
    product_list = [json.loads(product) for product in products]
    
    # Step 3: Filter out the product with the matching ID
    updated_products = [product for product in product_list if product['id'] != product_id]
    
    if len(product_list) == len(updated_products):
        print(f"Product with id {product_id} not found.")
        return
    
    # Step 4: Clear the existing list
    r.delete(key)
    
    # Step 5: Push back the updated list
    for product in updated_products:
        r.rpush(key, json.dumps(product))
    
    print(f"Product with id {product_id} has been deleted.")

# Example usage
delete_product_by_id('products', 101)
