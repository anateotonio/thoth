from utils.db import get_db_connection
from models.student import Student
import random

def register_student(student: Student):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO students (email, password, name) VALUES (%s, %s, %s)",
            (student.email, student.password, student.name)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Cadastro de aluno realizado com sucesso!"}
    except Exception as e:
        return {"error": str(e)}

def get_all_students():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        cursor.close()
        conn.close()
        return students
    except Exception as e:
        return {"error": str(e)}
    
def get_random_tots_service(count):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Selecionar Tots aleatórios
        cursor.execute("""
            SELECT id, professor_id, subject_area, category, subcategory
            FROM tots
            ORDER BY RANDOM()
            LIMIT %s
        """, (count,))

        tots = cursor.fetchall()
        cursor.close()
        conn.close()

        # Formatar os Tots como dicionário
        tots_list = [
            {
                "id": tot[0],
                "professor_id": tot[1],
                "subject_area": tot[2],
                "category": tot[3],
                "subcategory": tot[4]
            }
            for tot in tots
        ]
        return tots_list
    except Exception as e:
        return {"error": str(e)}
    
def get_leaderboard_service():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Consulta para obter estudantes ordenados pela pontuação
        cursor.execute("""
            SELECT name, quantidadedepontos
            FROM Students
            ORDER BY quantidadedepontos DESC
        """)

        students = cursor.fetchall()
        cursor.close()
        conn.close()

        # Retornar como lista de dicionários
        leaderboard = [
            {"name": student[0], "points": student[1]}
            for student in students
        ]
        return leaderboard
    except Exception as e:
        return {"error": str(e)}
    
def get_student_by_id_service(student_id):
    """
    Busca os dados de um estudante específico pelo ID no banco de dados.
    :param student_id: str
    :return: dict com os dados do estudante ou erro
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Consulta SQL para obter os dados do estudante pelo ID
        cursor.execute("""
            SELECT id, name, quantidadedepontos, exerciciosconcluidos
            FROM Students
            WHERE id = %s
        """, (student_id,))

        student = cursor.fetchone()
        cursor.close()
        conn.close()

        if student:
            return {
                "id": student[0],
                "name": student[1],
                "points": student[2],
                "exercisesCompleted": student[3]
            }
        else:
            return None
    except Exception as e:
        return {"error": str(e)}
    
def get_tot_by_id_service(tot_id):
    """
    Busca os dados de um TOT específico pelo ID no banco de dados, incluindo seus conteúdos.
    :param tot_id: int
    :return: dict com os dados do TOT e seus conteúdos ou erro
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Consulta SQL para obter os dados do TOT pelo ID
        cursor.execute("""
            SELECT id, professor_id, subject_area, category, subcategory, created_at
            FROM tots
            WHERE id = %s
        """, (tot_id,))

        tot = cursor.fetchone()

        if tot:
            # Consulta para obter os conteúdos associados ao TOT
            cursor.execute("""
                SELECT content_type, content_data
                FROM contents
                WHERE tot_id = %s
            """, (tot_id,))
            
            contents = cursor.fetchall()

            # Organizando os conteúdos em um dicionário
            contents_data = {
                content[0]: content[1] for content in contents
            }

            cursor.close()
            conn.close()

            # Retornando os dados do TOT com seus conteúdos
            return {
                "id": tot[0],
                "professor_id": tot[1],
                "subject_area": tot[2],
                "category": tot[3],
                "subcategory": tot[4],
                "created_at": tot[5],
                "contents": contents_data
            }
        else:
            cursor.close()
            conn.close()
            return None

    except Exception as e:
        return {"error": str(e)}
    
def process_student_answer_service(student_id, exercise_id, chosen_option_id):
    """
    Processa a resposta do aluno e atualiza os pontos se estiver correta.
    :param student_id: int
    :param exercise_id: int
    :param chosen_option_id: int
    :return: dict com status do processamento e novos pontos
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Verificar se a opção escolhida está correta
        cursor.execute("""
            SELECT is_correct
            FROM alternatives
            WHERE exercise_id = %s AND id = %s
        """, (exercise_id, chosen_option_id))
        correct = cursor.fetchone()

        if correct and correct[0]:  # Se a resposta está correta
            # Obter os pontos do exercício
            cursor.execute("""
                SELECT points
                FROM exercises
                WHERE id = %s
            """, (exercise_id,))
            exercise_points = cursor.fetchone()[0]

            # Atualizar os pontos do aluno
            cursor.execute("""
                UPDATE students
                SET quantidadedepontos = quantidadedepontos + %s,
                    exerciciosconcluidos = exerciciosconcluidos + 1
                WHERE id = %s
                RETURNING quantidadedepontos
            """, (exercise_points, student_id))
            new_points = cursor.fetchone()[0]

            conn.commit()
            cursor.close()
            conn.close()

            return {"success": True, "new_points": new_points}
        else:
            cursor.close()
            conn.close()
            return {"success": False, "error": "Resposta incorreta"}
    except Exception as e:
        return {"success": False, "error": str(e)}
    
def get_student_with_badges(student_id):
    """
    Busca os dados de um estudante específico pelo ID e calcula os badges desbloqueados.
    :param student_id: str
    :return: dict com os dados do estudante e badges ou erro
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Consulta SQL para obter os dados do estudante pelo ID
        cursor.execute("""
            SELECT id, name, quantidadedepontos, exerciciosconcluidos
            FROM Students
            WHERE id = %s
        """, (student_id,))

        student = cursor.fetchone()
        cursor.close()
        conn.close()

        if student:
            student_data = {
                "id": student[0],
                "name": student[1],
                "points": student[2],
                "exercisesCompleted": student[3]
            }

            # Dados estáticos de badges
            badges = [
                {"id": 1, "name": "Explorador do Conhecimento", "required_points": 1000},
                {"id": 2, "name": "Mestre dos Quizzes", "required_points": 5000},
                {"id": 3, "name": "Guardião das Respostas", "required_points": 10000},
                {"id": 4, "name": "Mago da Sabedoria", "required_points": 20000},
                {"id": 5, "name": "Sábio Supremo", "required_points": 30000},
            ]

            # Adiciona a informação se o estudante desbloqueou cada badge
            for badge in badges:
                badge["unlocked"] = student[2] >= badge["required_points"]

            student_data["badges"] = badges
            return student_data
        else:
            return None
    except Exception as e:
        return {"error": str(e)}
    
def get_random_missions_service():
    """
    Busca 5 missões aleatórias no banco de dados.
    :return: lista de missões ou erro
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Consulta SQL para pegar todas as missões disponíveis
        cursor.execute("""
            SELECT id, name, description, points, progress, goal
            FROM Missions
        """)
        all_missions = cursor.fetchall()
        cursor.close()
        conn.close()

        if all_missions:
            # Seleciona aleatoriamente 5 missões
            random_missions = random.sample(all_missions, 5)

            # Prepara a lista de missões a ser retornada
            missions_data = []
            for mission in random_missions:
                mission_data = {
                    "id": mission[0],
                    "name": mission[1],
                    "description": mission[2],
                    "points": mission[3],
                    "progress": mission[4],
                    "goal": mission[5]
                }
                missions_data.append(mission_data)

            return missions_data
        else:
            return None
    except Exception as e:
        return {"error": str(e)}
    
def search_tots_service(query):
    """
    Busca TOTs no banco de dados com base na consulta.
    :param query: str
    :return: lista de TOTs encontrados
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Consulta para buscar TOTs, removendo os acentos para fazer a comparação sem acentuação
        cursor.execute("""
            SELECT id, subject_area, category, subcategory, created_at
            FROM tots
            WHERE unaccent(LOWER(subject_area)) LIKE unaccent(%s)
               OR unaccent(LOWER(category)) LIKE unaccent(%s)
               OR unaccent(LOWER(subcategory)) LIKE unaccent(%s)
        """, (f"%{query}%", f"%{query}%", f"%{query}%"))
        
        results = cursor.fetchall()
        conn.close()

        # Transformar os resultados em um formato amigável
        return [{
            "id": row[0],
            "subject_area": row[1],
            "category": row[2],
            "subcategory": row[3],
            "created_at": row[4].isoformat() if row[4] else None
        } for row in results]
    except Exception as e:
        return {"error": str(e)}










