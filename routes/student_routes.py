from flask import Blueprint, request, jsonify
from services.student_service import *
from models.student import Student

student_routes = Blueprint('student_routes', __name__)

@student_routes.route('/students/register', methods=['POST'])
def register():
    data = request.json
    student = Student(data['email'], data['password'], data['name'])
    result = register_student(student)
    return jsonify(result)


@student_routes.route('/students/random_tots', methods=['GET'])
def get_random_tots():
    try:
        count = int(request.args.get('count', 10))  # Número de Tots aleatórios para retornar, default = 10
        tots = get_random_tots_service(count)
        return jsonify(tots)
    except Exception as e:
        return jsonify({"error": str(e)})
    
@student_routes.route('/students/leaderboard', methods=['GET'])
def get_leaderboard():
    try:
        leaderboard = get_leaderboard_service()
        if "error" in leaderboard:
            return jsonify({"error": leaderboard["error"]}), 500
        return jsonify(leaderboard)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@student_routes.route("/students/<student_id>", methods=["GET"])
def get_student(student_id):
    """
    Rota para obter os dados de um estudante pelo ID.
    :param student_id: str
    :return: JSON com os dados do estudante ou erro 404
    """
    student = get_student_by_id_service(student_id)
    if student:
        return jsonify(student), 200
    elif "error" in student:
        return jsonify(student), 500
    return jsonify({"error": "Estudante não encontrado"}), 404


@student_routes.route('/tot/<int:tot_id>', methods=["GET"])
def view_tot(tot_id):
    """
    Rota para visualizar um TOT e seus conteúdos pelo ID.
    :param tot_id: int
    :return: render_template com os dados do TOT ou erro 404
    """
    tot = get_tot_by_id_service(tot_id)
    if tot:
        return jsonify(tot), 200
    return jsonify({"error": "TOT não encontrado"}), 404

@student_routes.route('/exercise/<int:exercise_id>/submit', methods=["POST"])
def submit_exercise(exercise_id):
    """
    Processa a resposta do aluno para um exercício e atualiza seus pontos.
    :param exercise_id: int
    :return: JSON com resultado do processamento
    """
    data = request.get_json()
    student_id = data.get("student_id")
    chosen_option_id = data.get("chosen_option_id")

    if not student_id or not chosen_option_id:
        return jsonify({"error": "Dados incompletos"}), 400

    # Verificar resposta e atualizar pontos
    result = process_student_answer_service(student_id, exercise_id, chosen_option_id)

    if result.get("success"):
        return jsonify({"message": "Resposta processada com sucesso", "new_points": result["new_points"]}), 200
    else:
        return jsonify({"error": result.get("error", "Erro ao processar resposta")}), 400


