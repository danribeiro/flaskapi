from flask_restful import Resource, reqparse
from models.usuario import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST

atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True,
                       help="the file 'login' cannot be left blank")
atributos.add_argument('senha', type=str, required=True,
                       help="the file 'senha' cannot be left blank")
atributos.add_argument('ativado', type=bool)


class User(Resource):
    # /usuarios/{user_id}
    def get(self, user_id):
        """
        Retorna User
        """
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'user not found'}, 404  # not found

    @jwt_required
    def delete(self, user_id):
        user = UserModel.find_hotel(hotel_id)
        if user:
            try:
                hotel.delete_hotel()
            except expression as identifier:
                return {'message': 'An internal server error occured trying to delete user.'}

            return {"message": "User deleted."}
        return {"message": 'User not found'}, 404


class UserRegister(Resource):
    # /cadastro
    # @jwt_required
    def post(self):

        dados = atributos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {"message": "The login '{}' already exists.".format(dados['login'])}

        user = UserModel(**dados)
        user.ativado = False
        user.save_user()
        return {"message": "user created successfully!"}, 201  # created


class UserLogin(Resource):

    @classmethod
    def post(cls):
        dados = atributos.parse_args()

        user = UserModel.find_by_login(dados['login'])

        if user and safe_str_cmp(user.senha, dados['senha']):
            if user.ativado:
                token_de_acesso = create_access_token(identity=user.user_id)
                return {'access_token': token_de_acesso}, 200
            return {'message': 'User not confirmed.'}, 400
        return {'message': 'The username or password is incorrect.'}, 401


class UserLogout(Resource):

    @jwt_required
    def post(self):
        jwt_id = get_raw_jwt()['jti']  # JWT Token Identity
        BLACKLIST.add(jwt_id)
        return {'message': 'Logged out successfully!'}, 200


class UserConfirm(Resource):
    # raiz do site/confirmacao/1
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_user(user_id)

        if not user:
            return {'message': "User id '{}' not found.".format(user_id)}, 404

        user.ativado = True
        user.save_user()
        return {'message': "User id '{}' confirmed successfully.".format(user_id)}, 200
