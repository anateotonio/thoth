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


