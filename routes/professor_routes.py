from flask import Blueprint, request, jsonify
from services.professor_service import *
from models.professor import Professor
from models.tot import Tot
professor_routes = Blueprint('professor_routes', __name__)

@professor_routes.route('/professors/register', methods=['POST'])
def register():
    data = request.json
    professor = Professor(
        data['email'], data['password'], data['name'],
        data['cpf'], data['full_name'], data['birth_date'], data['subject_area']
    )
    result = register_professor(professor)
    return jsonify(result)


@professor_routes.route('/professors/create_tot', methods=['POST'])
def create_tot():
    data = request.json

    tot = Tot(
        professor_id=data['professor_id'],
        subject_area=data['subject_area'],
        category=data['category'],
        subcategory=data['subcategory'],
        contents=data['contents']  # Assumindo que o campo 'contents' existe no JSON
    )

    result = create_tot_service(tot)  # Passando o objeto 'Tot' para a função de serviço
    return jsonify(result)


@professor_routes.route('/professors/<int:professor_id>/tots', methods=['GET'])
def professor_tots(professor_id):
    data = get_professor_tots(professor_id)
    return jsonify(data)


@professor_routes.route('/professors/<int:professor_id>/exercises', methods=['GET'])
def professor_exercises(professor_id):
    data = get_professor_exercises(professor_id)
    return jsonify(data)

@professor_routes.route('/professors', methods=['GET'])
def list_professors():
    result = get_all_professors()
    return jsonify(result)

@professor_routes.route('/professors/tots/<int:tot_id>', methods=['PUT'])
def update_tot(tot_id):
    data = request.json
    result = update_tot_service(tot_id, data)
    return jsonify(result)


@professor_routes.route('/professors/tots/<int:tot_id>/edit', methods=['POST'])
def edit_tot_api(tot_id):
    data = request.json
    result = update_tot_service(tot_id)
    return jsonify(result)

@professor_routes.route('/professors/tots/<int:tot_id>', methods=['DELETE'])
def delete_tot(tot_id):
    # Chamar o serviço para deletar o TOT usando apenas o ID
    result = delete_tot_service(tot_id)
    # Retornar o resultado como JSON
    return jsonify(result)


@professor_routes.route('/professors/tots/<int:tot_id>/contents', methods=['GET'])
def get_tot_contents(tot_id):
    result = get_tot_contents_service(tot_id)
    return jsonify(result)


@professor_routes.route('/professors/tots/<int:tot_id>/edit_contents', methods=['PUT'])
def edit_tot_contents(tot_id):
    data = request.json
    result = edit_tot_contents_service(tot_id, data)
    return jsonify(result)


@professor_routes.route('/professor/criar_exercicios/<int:tot_id>', methods=['POST'])
def criar_exercicio(tot_id):
    # Obtendo os dados enviados no corpo da requisição
    data = request.json
    
    # Chamando o serviço para criar o exercício
    result = create_exercise_service(tot_id, data)
    
    # Verificando o resultado e retornando a resposta adequada
    if result.get("message"):
        return jsonify({"message": result["message"]}), 201  # Sucesso na criação
    else:
        return jsonify({"error": result["error"]}), 400  # Erro na criação

@professor_routes.route('/professor/exercicio/<int:exercise_id>', methods=['GET'])
def get_exercise(exercise_id):
    exercise = get_exercise_by_id_service(exercise_id)
    return jsonify(exercise)


@professor_routes.route('/professor/editar_exercicio/<int:exercise_id>', methods=['PUT'])
def edit_exercise(exercise_id):
    data = request.json
    result = edit_exercise_service(exercise_id, data)
    return jsonify(result)

@professor_routes.route('/professor/exercicios/<int:professor_id>', methods=['GET'])
def get_exercises(professor_id):
    try:
        result = get_exercises_service(professor_id)
        return jsonify(result)  # Retorna o JSON
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@professor_routes.route('/professor/exercicios/tot/<int:tot_id>', methods=['GET'])
def get_exercises_for_tot(tot_id):
    try:
        result = get_exercises_by_tot_service(tot_id)
        return jsonify(result)  # Retorna os exercícios no formato JSON
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@professor_routes.route('/professor/remover/exercicio/<int:exercise_id>', methods=['DELETE'])
def excluir_exercicio(exercise_id):
    try:
        # Chame o serviço para excluir o exercício
        delete_exercise_service(exercise_id)
        return jsonify({"message": "Exercício excluído com sucesso!"}), 200
    except Exception as e:
        return jsonify({"message": f"Erro ao excluir exercício: {str(e)}"}), 500


