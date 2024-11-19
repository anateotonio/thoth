from flask import Blueprint, request, jsonify, session
from services.auth_service import authenticate_user  # Importe o serviço de autenticação

auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # Pegando o corpo da requisição em JSON
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email e senha são obrigatórios'}), 400

    # Chama o serviço de autenticação e descompacta os 3 valores retornados
    user_type, user_id, user = authenticate_user(email, password)

    # Verifica se o usuário foi autenticado corretamente
    if user_type and user:
        # Armazenar o ID do usuário e o tipo na sessão
        session['user_id'] = user_id
        session['user_type'] = user_type

        return jsonify({'message': 'Login bem-sucedido', 'user_type': user_type, 'user_id': user_id}), 200
    else:
        return jsonify({'error': 'Credenciais inválidas'}), 401

@auth_routes.route('/profile', methods=['GET'])
def profile():
    # Verifica se o usuário está logado
    user_id = session.get('user_id')
    user_type = session.get('user_type')

    if not user_id:
        return jsonify({'error': 'Usuário não autenticado'}), 401

    return jsonify({'user_id': user_id, 'user_type': user_type})
