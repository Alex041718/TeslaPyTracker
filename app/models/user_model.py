from app import mongo
from bson import ObjectId
from datetime import datetime

class User:
    collection = mongo.db.users
    
    @staticmethod
    def get_all():
        return list(User.collection.find())
    
    @staticmethod
    def get_by_id(user_id):
        return User.collection.find_one({"_id": ObjectId(user_id)})
    
    @staticmethod
    def create(user_data):
        user_data['created_at'] = datetime.utcnow()
        result = User.collection.insert_one(user_data)
        return str(result.inserted_id)
    
    @staticmethod
    def update(user_id, user_data):
        user_data['updated_at'] = datetime.utcnow()
        User.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": user_data}
        )
        return User.get_by_id(user_id)
    
    @staticmethod
    def delete(user_id):
        User.collection.delete_one({"_id": ObjectId(user_id)})
        return True