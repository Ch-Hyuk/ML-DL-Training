from pymongo import MongoClient
import json
import os

# MongoDB 서버에 연결
client = MongoClient("")

print("Current Working Directory: ", os.getcwd())
print(client)

# 데이터베이스 선택
db = client['']

# 컬렉션 선택
collection = db['']

# 데이터 삽입
post = {"name": "ch_hyuk", "text": "Mongo test start!", "tags": ["mongodb", "python", "pymongo"]}
post_id = collection.insert_one(post)
print(f"Inserted post with ID: {post_id}")

# 데이터 조회
for post in collection.find():
    print(post)

# 특정 데이터 조회
specific_post = collection.find_one({"name": "ch_hyuk"})
print(f"Post fetched: {specific_post}")
