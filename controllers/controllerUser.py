from models.auth import User
from models.user import UserModel
from schemas.user import CreateUser


class UserController:
    @staticmethod
    async def get_all_users():
        return await UserModel.get_all_users()

    @staticmethod
    async def get_user_by_id(user_id: str):
        return await UserModel.get_user_by_id(user_id)

    @staticmethod
    async def create_user(user: CreateUser):
        user_data = user.dict()
        return await UserModel.create_user(user_data)

    @staticmethod
    async def update_user(user_id: str, user: User):
        user_data = user.dict(exclude_unset=True)
        return await UserModel.update_user(user_id, user_data)

    @staticmethod
    async def delete_user(user_id: str):
        return await UserModel.delete_user(user_id)