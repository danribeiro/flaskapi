from flask_restful import Resource, reqparse
from models.hotel  import HotelModel
from flask_jwt_extended import jwt_required



class Hoteis(Resource):
    def get(self):
        return {'hoteis':[hotel.json() for hotel in HotelModel.query.all()]}


class Hotel(Resource):

    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True,help="the file 'nome' cannot be left blank")
    argumentos.add_argument('estrelas', type=float, required=True,help="the file 'estrelas' cannot be left blank")
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    def get(self, hotel_id):
        """
        Retorna Hotel
        """
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'hotel not found'}, 404 # not found

    @jwt_required
    def post(self, hotel_id):
        """
        Cria hotel
        """
        if HotelModel.find_hotel(hotel_id):
            return {"message":"Hotel id '{}' already exists.".format(hotel_id)}, 400 # bad request
        
        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        
        try:
            hotel.save_hotel()
        except expression as identifier:
            return {'message':'An internal server error occured trying to save hotel.'}
        
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
                return {'message':'An internal server error occured trying to save hotel.'}
            return novo_encontrado.json(), 200 # updated
        
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except expression as identifier:
            return {'message':'An internal server error occured trying to save hotel.'}
        return hotel.json(), 201 # created

    @jwt_required
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
        
            try:
                hotel.delete_hotel()
            except expression as identifier:
                return {'message':'An internal server error occured trying to delete hotel.'}
            
            return {"message": "Hotel deleted."}
        return {"message": 'Hotel not found'}, 404