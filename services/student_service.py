from utils.db import get_db_connection
from models.student import Student

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






