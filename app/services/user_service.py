from app.models.user_model import User
from app.schemas.user_schema import UserSchema
from werkzeug.security import generate_password_hash
from marshmallow import ValidationError

user_schema = UserSchema()

class UserService:
    @staticmethod
    def get_all_users():
        users = User.get_all()
        return user_schema.dump(users, many=True)
    
    @staticmethod
    def get_user_by_id(user_id):
        user = User.get_by_id(user_id)
        if not user:
            return None
        return user_schema.dump(user)
    
    @staticmethod
    def create_user(user_data):
        try:
            # Valider les données
            validated_data = user_schema.load(user_data)
            
            # Hacher le mot de passe
            validated_data['password'] = generate_password_hash(validated_data['password'])
            
            # Créer l'utilisateur
            user_id = User.create(validated_data)
            return {"message": "Utilisateur créé avec succès", "user_id": user_id}
        except ValidationError as e:
            return {"errors": e.messages}, 400
    
    @staticmethod
    def update_user(user_id, user_data):
        try:
            # Vérifier si l'utilisateur existe
            user = User.get_by_id(user_id)
            if not user:
                return {"message": "Utilisateur non trouvé"}, 404
            
            # Valider les données
            validated_data = user_schema.load(user_data, partial=True)
            
            # Hacher le mot de passe si fourni
            if 'password' in validated_data:
                validated_data['password'] = generate_password_hash(validated_data['password'])
            
            # Mettre à jour l'utilisateur
            updated_user = User.update(user_id, validated_data)
            return user_schema.dump(updated_user)
        except ValidationError as e:
            return {"errors": e.messages}, 400
    
    @staticmethod
    def delete_user(user_id):
        # Vérifier si l'utilisateur existe
        user = User.get_by_id(user_id)
        if not user:
            return {"message": "Utilisateur non trouvé"}, 404
        
        # Supprimer l'utilisateur
        User.delete(user_id)
        return {"message": "Utilisateur supprimé avec succès"}