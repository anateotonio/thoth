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