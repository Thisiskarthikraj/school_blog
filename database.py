from motor.motor_asyncio import AsyncIOMotorClient

DATABASE_URL = "mongodb://localhost:27017"  # Adjust as needed
client = AsyncIOMotorClient(DATABASE_URL)
db = client.schoolblog  # Replace with your database name
