
import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = os.getenv("MONGO_URL")

if not MONGO_URL:
    raise RuntimeError("❌ MONGO_URL Not Found!")

# Motor async client
client = AsyncIOMotorClient(MONGO_URL)

# Use default DB from connection string OR fallback
db_name = os.getenv("MONGO_DB_NAME", "UTTAM-DB")
db = client[db_name]

gmuteh = db["GMUTE"]     # Async MotorCollection


async def is_gmuted(sender_id: int) -> bool:
    doc = await gmuteh.find_one({"sender_id": sender_id})
    return doc is not None


async def gmute(sender_id: int, reason="#GMuted"):
    await gmuteh.update_one(
        {"sender_id": sender_id},
        {"$set": {"sender_id": sender_id, "reason": reason}},
        upsert=True
    )


async def ungmute(sender_id: int):
    await gmuteh.delete_one({"sender_id": sender_id})
