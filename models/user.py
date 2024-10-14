from bson import ObjectId

from config.database import db

def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "role": user["role"]
    }

users_collection = db["users"]

class UserModel:
    @staticmethod
    async def get_all_users():
        users = []
        async for user in users_collection.find():
            users.append(user_helper(user))
        return users

    @staticmethod
    async def get_user_by_id(user_id: str):
        user = await users_collection.find_one({"_id": ObjectId(user_id)})
        if user:
            return user_helper(user)
        return None

    @staticmethod
    async def create_user(user_data: dict):
        new_user = await users_collection.insert_one(user_data)
        created_user = await users_collection.find_one({"_id": new_user.inserted_id})
        return user_helper(created_user)

    @staticmethod
    async def update_user(user_id: str, user_data: dict):
        updated_user = await users_collection.update_one(
            {"_id": ObjectId(user_id)}, {"$set": user_data}
        )
        if updated_user.modified_count:
            return await UserModel.get_user_by_id(user_id)
        return None

    @staticmethod
    async def delete_user(user_id: str):
        deleted_user = await users_collection.delete_one({"_id": ObjectId(user_id)})
        return deleted_user.deleted_count