from utils.db import get_db_connection

def authenticate_user(email, password):

    conn = get_db_connection()
    cur = conn.cursor()

    # Consultar na tabela de professores
    cur.execute("SELECT * FROM professors WHERE email = %s AND password = %s", [email, password])
    professor = cur.fetchone()

    # Consultar na tabela de alunos
    cur.execute("SELECT * FROM students WHERE email = %s AND password = %s", [email, password])
    student = cur.fetchone()

    cur.close()
    conn.close()

    # Retorna o tipo de usuário encontrado (professor ou aluno) e o ID do usuário
    if professor:
        user_id = professor[0]  # Supondo que o ID do professor esteja na primeira coluna
        return 'professor', user_id, professor
    elif student:
        user_id = student[0]  # Supondo que o ID do aluno esteja na primeira coluna
        return 'student', user_id, student
    else:
        return None, None, None
