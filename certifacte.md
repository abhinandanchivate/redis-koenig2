To create a **TLS certificate** for Redis running in a **Docker container**, follow these steps:

---

### **Step 1: Install OpenSSL**
Ensure OpenSSL is installed on your system. For Windows users, OpenSSL can be installed using Chocolatey or other package managers.

```bash
sudo apt update
sudo apt install openssl -y
```

---

### **Step 2: Generate Certificates for TLS**
Run the following commands to generate the necessary certificates and keys.

**1. Create a root CA certificate:**
```bash
openssl genrsa -out ca.key 4096
openssl req -x509 -new -nodes -key ca.key -sha256 -days 365 -out ca.crt \
-subj "/C=US/ST=State/L=City/O=CompanyName/OU=IT Department/CN=RootCA"
```

**2. Generate a server certificate for Redis:**
```bash
openssl genrsa -out redis.key 4096
openssl req -new -key redis.key -out redis.csr \
-subj "/C=US/ST=State/L=City/O=CompanyName/OU=IT Department/CN=redis-server"
```

**3. Sign the server certificate with the CA:**
```bash
openssl x509 -req -in redis.csr -CA ca.crt -CAkey ca.key \
-CAcreateserial -out redis.crt -days 365 -sha256
```

**4. Generate a Diffie-Hellman (DH) parameter file:**
```bash
openssl dhparam -out dhparam.pem 2048
```

---

### **Step 3: Configure Redis for TLS**
1. Create a directory to store the TLS files:
```bash
mkdir -p redis_tls
mv ca.crt redis.crt redis.key dhparam.pem redis_tls/
```

2. Create a **redis.conf** file with TLS settings:

**`redis.conf`**
```
tls-port 6379
port 0
tls-cert-file /usr/local/etc/redis/redis_tls/redis.crt
tls-key-file /usr/local/etc/redis/redis_tls/redis.key
tls-ca-cert-file /usr/local/etc/redis/redis_tls/ca.crt
tls-dh-params-file /usr/local/etc/redis/redis_tls/dhparam.pem
tls-auth-clients no
```

---

### **Step 4: Create a Docker Container with Redis and TLS Configuration**
Create a `Dockerfile` for Redis with TLS support.

**`Dockerfile`**
```dockerfile
FROM redis:latest
COPY redis.conf /usr/local/etc/redis/redis.conf
COPY redis_tls /usr/local/etc/redis/redis_tls
CMD ["redis-server", "/usr/local/etc/redis/redis.conf"]
```

---

### **Step 5: Build and Run the Docker Container**
Run the following commands to build and run the Redis container:

```bash
docker build -t redis-tls .
docker run -d --name redis-tls -p 6379:6379 redis-tls
```

---

### **Step 6: Connect to Redis Using TLS**
To connect to Redis with TLS enabled:

```bash
redis-cli --tls \
  --cert /path/to/redis.crt \
  --key /path/to/redis.key \
  --cacert /path/to/ca.crt \
  -h localhost -p 6379
```

---

### **Step 7: Verify TLS Configuration**
1. Check logs in your Redis container:
```bash
docker logs redis-tls
```

2. Use `openssl` to test the TLS certificate:
```bash
openssl s_client -connect localhost:6379 -CAfile ca.crt
```

---

### **Key Notes:**
✅ Ensure that the certificate files are properly mapped in the container.  
✅ Verify that the Redis configuration file (`redis.conf`) points to the correct paths for TLS certificates.  
✅ For production, use stronger security practices like client authentication.

