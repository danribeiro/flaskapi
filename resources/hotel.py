import sqlite3
from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from models.site import SiteModel
from flask_jwt_extended import jwt_required
from resources.filtros import normalize_path_params, consulta_com_cidade, consulta_sem_cidade

path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=str)
path_params.add_argument('estrelas_min', type=float)
path_params.add_argument('estrelas_max', type=float)
path_params.add_argument('diaria_min', type=float)
path_params.add_argument('diaria_max', type=float)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset', type=float)


class Hoteis(Resource):
    def get(self):
        connection = sqlite3.connect('banco.db')
        cursor = connection.cursor()

        dados = path_params.parse_args()
        dados_validos = {chave: dados[chave]
                         for chave in dados if dados[chave] is not None}

        parametros = normalize_path_params(**dados_validos)
        if not parametros.get('cidade'):
            consulta = consulta_sem_cidade
            tupla = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta, tupla)
        else:
            consulta = consulta_com_cidade
            tupla = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta, tupla)

        hoteis = []
        for linha in resultado:
            hoteis.append({
                'hotel_id': linha[0],
                'nome': linha[1],
                'estrelas': linha[2],
                'diaria': linha[3],
                'cidade': linha[4],
                'site_id': linha[5]
            })

        return {'hoteis': hoteis}


class Hotel(Resource):

    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True,
                            help="the file 'nome' cannot be left blank")
    argumentos.add_argument('estrelas', type=float, required=True,
                            help="the file 'estrelas' cannot be left blank")
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')
    argumentos.add_argument('site_id', type=int, required=True,
                            help="Every hotel needs to be linked with site")

    def get(self, hotel_id):
        """
        Retorna Hotel
        """
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'hotel not found'}, 404  # not found

    @jwt_required
    def post(self, hotel_id):
        """
        Cria hotel
        """
        if HotelModel.find_hotel(hotel_id):
            # bad request
            return {"message": "Hotel id '{}' already exists.".format(hotel_id)}, 400

        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)

        if not SiteModel.find_by_id(dados.get('site_id')):
            return {'message': 'The hotel must be associated to a valid site id.'}, 400

        try:
            hotel.save_hotel()
        except expression as identifier:
            return {'message': 'An internal server error occured trying to save hotel.'}

        return hotel.json()

    @jwt_required
    def put(self, hotel_id):
        """
        Alterar Hotel
        """
        dados = Hotel.argumentos.parse_args()

        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            try:
                hotel.save_hotel()
            except expression as identifier:
                return {'message': 'An internal server error occured trying to save hotel.'}
            return novo_encontrado.json(), 200  # updated

        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except expression as identifier:
            return {'message': 'An internal server error occured trying to save hotel.'}
        return hotel.json(), 201  # created

    @jwt_required
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:

            try:
                hotel.delete_hotel()
            except expression as identifier:
                return {'message': 'An internal server error occured trying to delete hotel.'}

            return {"message": "Hotel deleted."}
        return {"message": 'Hotel not found'}, 404
