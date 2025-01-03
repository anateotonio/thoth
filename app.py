from flask import Flask, render_template
from flask import Blueprint, request, jsonify
from routes.student_routes import student_routes
from routes.professor_routes import professor_routes
from routes.auth_routes import auth_routes
from services.professor_service import *
from services.student_service import *
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, methods=["GET", "POST", "OPTIONS"], supports_credentials=True)

app.secret_key = 'NXHSBWHDE774YRT46R4GEYBXbsyw!'

# Registro das rotas
app.register_blueprint(student_routes)
app.register_blueprint(professor_routes)
app.register_blueprint(auth_routes)

@app.route('/')
def login():
    return render_template('telas/index.html')

@app.route('/estudante/exercicios-tot/tot/<int:tot_id>', methods=['GET'])
def list_exercises_for_tot_student(tot_id):
    try:
        # Obter os exercícios do TOT
        exercises = get_exercises_by_tot_service(tot_id)
        if 'error' in exercises:
            return render_template('erro.html', error=exercises['error'])
        return render_template('telas/listar_exercicios_estudante.html', exercises=exercises)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/cadastro')
def register():
    return render_template('telas/register.html')

@app.route('/estudante/badges')
def badges():
    return render_template('telas/badges.html')

@app.route('/estudante/perfil')
def student_profile():
    return render_template('telas/perfil_estudante.html')

@app.route('/estudante/home')
def student_home():
    return render_template('telas/home_estudante.html')

@app.route('/professor/home')
def professor_home():
    return render_template('telas/home_professor.html')

@app.route('/estudante/home')
def estudante_home():
    return render_template('telas/home_estudante.html')

@app.route('/professor/criar_tot')
def create_tot():
    return render_template('telas/criar_tot.html')

@app.route('/professor/tots')
def list_tots():
    return render_template('telas/tots_professor.html')

@app.route('/professor/exercicios')
def list_exercises():
    return render_template('telas/exercicios_professor.html')

@app.route('/professor/criar_exercicio/<int:tot_id>', methods=['GET'])
def criar_exercicio(tot_id):
    # Busca o TOT pelo ID para garantir que ele existe
    tot = get_tot_by_id(tot_id)
    if not tot:
        return "TOT não encontrado", 404
    # Renderiza a página de criação de exercício, passando o tot_id
    return render_template('telas/criar_exercicio.html', tot=tot)

@app.route('/professor/editar_tot/<int:tot_id>')
def edit_tot(tot_id):
    # Busca o TOT pelo ID
    tot = get_tot_by_id(tot_id)
    if not tot:
        return "TOT não encontrado", 404
    # Renderiza o template com o TOT encontrado
    return render_template('telas/editar_tot.html', tot=tot)

@app.route('/professor/editar_exercicio/<int:exercise_id>', methods=['GET', 'POST'])
def edit_exercise(exercise_id):
    # Busca o exercício pelo ID
    exercise = get_exercise_by_id_service(exercise_id)
    if 'message' in exercise:
        return exercise['message'], 404  # Caso não encontre o exercício

    if request.method == 'POST':
        # Pega os dados que foram passados via JSON pelo JavaScript
        data = request.json  # Aqui vamos esperar os dados em formato JSON

        # Chama o serviço para editar o exercício
        result = edit_exercise_service(exercise_id, data)
        if 'message' in result:
            return jsonify(result), 200  # Exibição da mensagem de sucesso no formato JSON

        return jsonify({"message": "Erro ao editar exercício"}), 400  # Caso haja algum erro no processo

    # Caso a requisição seja GET, renderiza o template de edição com os dados do exercício
    return render_template('telas/editar_exercicio.html', exercise=exercise)

@app.route('/estudante/visualizar_exercicio/<int:exercise_id>', methods=['GET', 'POST'])
def view_exercise(exercise_id):
    exercise = get_exercise_by_id_service(exercise_id)
    if 'message' in exercise:
        return exercise['message'], 404  # Caso não encontre o exercício
    # Caso a requisição seja GET, renderiza o template de edição com os dados do exercício
    return render_template('telas/responder_exercicio.html', exercise=exercise)

@app.route('/professor/exercicios-tot/tot/<int:tot_id>', methods=['GET'])
def list_exercises_for_tot(tot_id):
    try:
        # Obter os exercícios do TOT
        exercises = get_exercises_by_tot_service(tot_id)
        if 'error' in exercises:
            return render_template('erro.html', error=exercises['error'])
        return render_template('telas/listar_exercicios_tot_prof.html', exercises=exercises)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/leaderboard')
def leaderboard_page():
    leaderboard = get_leaderboard_service()
    if "error" in leaderboard:
        return render_template('telas/error.html', error=leaderboard["error"])

    return render_template('telas/leaderboard.html', leaderboard=leaderboard)

@app.route('/estudante/visualizar_tot/<int:tot_id>', methods=['GET'])
def view_tot_page(tot_id):
    tot = get_tot_by_id_service(tot_id)
    if "error" in tot:
        return render_template('telas/error.html', error=tot["error"])
    return render_template('telas/visualizar_conteudo.html', tot=tot)

@app.route('/estudante/tots_por_categoria/<category>', methods=['GET'])
def view_tots_by_category(category):
    """
    Rota para exibir os tópicos de uma categoria específica.
    :param category: str (categoria dos tópicos)
    :return: Renderiza o template com os tópicos ou erro
    """
    # Chamando a função que retorna os tópicos por categoria
    categories = get_tots_by_subject_area_service(category)
    
    if "error" in categories:
        return render_template('telas/error.html', error=categories["error"])
    
    # Passando os tópicos por categoria para o template
    return render_template('telas/disciplinas_topicos.html', categories=categories)





if __name__ == '__main__':
    app.run(debug=True)
