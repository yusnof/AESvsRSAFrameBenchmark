from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
import time as dt 
import csv 
import os 



class AESvsRSAFrameBenchmark:
   def __init__(self):
      self.aes_key = get_random_bytes(32)
      self.key = RSA.generate(2048)
      self.private_key = self.key
      self.public_key = self.key.publickey() 
   

     
    
# RSA encryption function
def rsa_encrypt(data, public_key):
    cipher = PKCS1_OAEP.new(public_key)
    return cipher.encrypt(data)

# RSA decryption function
def rsa_decrypt(ciphertext, private_key):
    cipher = PKCS1_OAEP.new(private_key)
    return cipher.decrypt(ciphertext)

# AES encryption function
def aes_encrypt(data, key):
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return cipher.nonce, ciphertext, tag

# AES decryption function
def aes_decrypt(nonce, ciphertext, tag, key):
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)

# AES en/de that returns time as a tuple 
def aes_num_encrypt_decrypt(aes_key,data,numberOfTimes):
    enresults = []
    deresults = []
    correct = True

    cnt = numberOfTimes
    while cnt > 0:
     start_time = dt.perf_counter()
     nonce, aes_ciphertext, tag = aes_encrypt(data, aes_key)
     aes_encrypt_time = dt.perf_counter() - start_time
     
     aes_decrypted = aes_decrypt(nonce, aes_ciphertext, tag, aes_key)
     aes_decrypt_time = dt.perf_counter() - start_time - aes_encrypt_time
    
     enresults.append(aes_encrypt_time)
     deresults.append(aes_decrypt_time)
     cnt -= 1 
     correct = correct and (aes_decrypted == data)
    return [sum(enresults), sum(deresults), correct]

def rsa_num_encrypt_decrypt(rsa_public_key,rsa_private_key, data,numberOfTimes):
    enresults = []
    deresults = []
    correct = True

    cnt = numberOfTimes
    while cnt > 0:
     start_time = dt.perf_counter()
     rsa_encrypt1 = rsa_encrypt(data, rsa_public_key)
     rsa_encrypt_time = dt.perf_counter() - start_time
     
     rsa_decryped1 = rsa_decrypt(rsa_encrypt1, rsa_private_key)
     rsa_encrypt_time = dt.perf_counter() - start_time - rsa_encrypt_time
    
     enresults.append(rsa_encrypt_time)
     deresults.append(rsa_encrypt_time)
     cnt -= 1 
     correct = correct and (rsa_decryped1 == data)

    return [sum(enresults), sum(deresults), correct]

# CSV file setup
csv_file = "results.csv"
write_header = not os.path.exists(csv_file)  # Write header only if file doesn't exist

# List to store results
results = []

# Run 10 iterations
for i in range(1,10000,1000):
    # Generate 128 bytes of random data
    byte_data = get_random_bytes(128)  # Keep as bytes, do NOT decode
    

    p1 = AESvsRSAFrameBenchmark()


    aes_key = p1.aes_key
    private_key = p1.private_key
    public_key = p1.public_key

    aes_encrypt_time, aes_decrypt_time, aes_correct = aes_num_encrypt_decrypt(aes_key,byte_data,i)
    rsa_encrypt_time, rsa_decrypt_time, rsa_correct = rsa_num_encrypt_decrypt(public_key,private_key,byte_data,i)
  

    results.append(["RSA", i, (i * 128)/1000, f"{rsa_encrypt_time:.6f}", f"{rsa_decrypt_time:.6f}", rsa_correct])
    results.append(["AES", i, (i * 128)/1000, f"{aes_encrypt_time:.6f}", f"{aes_decrypt_time:.6f}", aes_correct])

    #print(results.pop())
    # print(results.pop())

# Write results to CSV
with open(csv_file, mode="a", newline="") as f:
    writer = csv.writer(f)
    # Write header if file is new
    if write_header:
        writer.writerow(["Algorithm", "Iteration", "fileSize (kBytes)", "Encryption Time (s)", "Decryption Time (s)", "Decryption Correct"])
    # Write all results
    writer.writerows(results)