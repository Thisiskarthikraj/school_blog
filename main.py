from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
from models import BlogPost, BlogPostInDB
import database
from bson import ObjectId

app = FastAPI()

@app.post("/posts/", response_model=BlogPostInDB)
async def create_post(post: BlogPost):
    post_dict = post.dict()
    result = await database.db.posts.insert_one(post_dict)
    new_post = await database.db.posts.find_one({"_id": result.inserted_id})
    return BlogPostInDB(**new_post)

@app.get("/posts/", response_model=List[BlogPostInDB])
async def read_posts():
    posts = []
    async for post in database.db.posts.find():
        posts.append(BlogPostInDB(**post))
    return posts

@app.get("/posts/{post_id}", response_model=BlogPostInDB)
async def read_post(post_id: str):
    post = await database.db.posts.find_one({"_id": ObjectId(post_id)})
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return BlogPostInDB(**post)

@app.put("/posts/{post_id}", response_model=BlogPostInDB)
async def update_post(post_id: str, post: BlogPost):
    await database.db.posts.update_one({"_id": ObjectId(post_id)}, {"$set": post.dict()})
    updated_post = await database.db.posts.find_one({"_id": ObjectId(post_id)})
    return BlogPostInDB(**updated_post)

@app.delete("/posts/{post_id}", response_model=dict)
async def delete_post(post_id: str):
    result = await database.db.posts.delete_one({"_id": ObjectId(post_id)})
    if result.deleted_count == 1:
        return {"message": "Post deleted successfully"}
    raise HTTPException(status_code=404, detail="Post not found")
