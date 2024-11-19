from utils.db import get_db_connection
from models.professor import Professor
from models.tot import Tot

def register_professor(professor: Professor):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO professors (email, password, name, cpf, full_name, birth_date, subject_area) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (professor.email, professor.password, professor.name,
             professor.cpf, professor.full_name, professor.birth_date, professor.subject_area)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Cadastro de professor realizado com sucesso!"}
    except Exception as e:
        return {"error": str(e)}
    
def create_tot_service(data):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Inserir o Tot no banco de dados
        cursor.execute("""
            INSERT INTO tots (professor_id, subject_area, category, subcategory)
            VALUES (%s, %s, %s, %s) RETURNING id
        """, (data.professor_id, data.subject_area, data.category, data.subcategory))  # Acessando atributos diretamente
        tot_id = cursor.fetchone()[0]

        # Inserir os conteúdos associados ao Tot
        for content in data.contents:  # Iterando sobre 'contents' que é uma lista
            cursor.execute("""
                INSERT INTO contents (tot_id, content_type, content_data)
                VALUES (%s, %s, %s)
            """, (tot_id, content['type'], content['value']))

        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Tot criado com sucesso!", "tot_id": tot_id}
    except Exception as e:
        return {"error": str(e)}

    

## def get_professor_tots(professor_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Buscar todos os Tots do professor
        cursor.execute("""
            SELECT id, subject_area, category, subcategory
            FROM tots
            WHERE professor_id = %s
        """, (professor_id,))
        tots = cursor.fetchall()

        cursor.close()
        conn.close()
        return {"tots": tots}
    except Exception as e:
        return {"error": str(e)} 
    
def get_professor_tots(professor_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Buscar todos os Tots do professor
        cursor.execute("""
            SELECT id, subject_area, category, subcategory, created_at
            FROM tots
            WHERE professor_id = %s
            ORDER BY created_at DESC
        """, (professor_id,))
        
        tots = cursor.fetchall()
        tots_list = [
            {
                "id": tot[0],
                "subject_area": tot[1],
                "category": tot[2],
                "subcategory": tot[3],
                "created_at": tot[4].strftime("%d/%m/%Y")
            }
            for tot in tots
        ]

        cursor.close()
        conn.close()
        return {"tots": tots_list}
    except Exception as e:
        return {"error": str(e)}

    
def get_tot_count(professor_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Contar o número de Tots do professor
        cursor.execute("SELECT COUNT(*) FROM tots WHERE professor_id = %s", (professor_id,))
        count = cursor.fetchone()[0]

        cursor.close()
        conn.close()
        return count
    except Exception as e:
        return {"error": str(e)}

def get_first_five_tots(professor_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Buscar os 5 primeiros Tots do professor
        cursor.execute("""
            SELECT id, subject_area, category, subcategory
            FROM tots
            WHERE professor_id = %s
            ORDER BY created_at ASC
            LIMIT 5
        """, (professor_id,))
        tots = cursor.fetchall()

        # Estruturar os dados como uma lista de dicionários
        tots_list = [
            {"id": tot[0], "subject_area": tot[1], "category": tot[2], "subcategory": tot[3]}
            for tot in tots
        ]

        cursor.close()
        conn.close()
        return tots_list
    except Exception as e:
        return {"error": str(e)}

    
def get_professor_exercises(professor_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Buscar os 5 primeiros Exercícios do professor
        cursor.execute("""
            SELECT e.id, e.title, t.subject_area AS subject_area
            FROM exercises e
            JOIN tots t ON e.tot_id = t.id
            WHERE e.professor_id = %s
        """, (professor_id,))
        exercises = cursor.fetchall()

        cursor.close()
        conn.close()
        return {"exercises": exercises}
    except Exception as e:
        return {"error": str(e)}

def get_tot_by_id(tot_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM tots WHERE id = %s", (tot_id,))
        tot = cursor.fetchone()  # Recupera o primeiro resultado
        if tot:
            # Supondo que a tabela "tots" tenha as colunas: tot_id, category, subject_area, subcategory, created_at
            tot_data = {
                "id": tot[0],
                "category": tot[3],
                "subject_area": tot[2],
                "subcategory": tot[4],
                "created_at": tot[5]
            }
            return tot_data
        else:
            return None  # Retorna None se não encontrar o TOT
    except Exception as e:
        print(f"Erro ao buscar o TOT: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def update_tot_service(tot_id, data):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Atualizar o TOT no banco de dados
        cursor.execute("""
            UPDATE tots
            SET subject_area = %s, category = %s, subcategory = %s
            WHERE id = %s
        """, (data['subject_area'], data['category'], data['subcategory'], tot_id))

        # Atualizar os conteúdos associados
        if 'contents' in data:
            cursor.execute("DELETE FROM contents WHERE tot_id = %s", (tot_id,))
            for content in data['contents']:
                cursor.execute("""
                    INSERT INTO contents (tot_id, content_type, content_data)
                    VALUES (%s, %s, %s)
                """, (tot_id, content['type'], content['value']))

        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "TOT atualizado com sucesso!"}
    except Exception as e:
        return {"error": str(e)}
    

# Remover TOT
def delete_tot_service(tot_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Remover conteúdos associados
        cursor.execute("DELETE FROM contents WHERE tot_id = %s", (tot_id,))

        # Remover o TOT
        cursor.execute("DELETE FROM tots WHERE id = %s", (tot_id,))

        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "TOT removido com sucesso!"}
    except Exception as e:
        return {"error": str(e)}





def get_all_professors():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM professors")
        professors = cursor.fetchall()
        cursor.close()
        conn.close()
        return professors
    except Exception as e:
        return {"error": str(e)}

def get_tot_contents_service(tot_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Buscar os conteúdos associados ao TOT
        cursor.execute("""
            SELECT content_type, content_data
            FROM contents
            WHERE tot_id = %s
        """, (tot_id,))
        contents = cursor.fetchall()

        # Estruturar os conteúdos como uma lista de dicionários
        contents_list = [
            {"type": content[0], "value": content[1]}
            for content in contents
        ]

        cursor.close()
        conn.close()
        return {"contents": contents_list}
    except Exception as e:
        return {"error": str(e)}

def edit_tot_contents_service(tot_id, data):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Atualizar os dados principais do TOT
        cursor.execute("""
            UPDATE tots
            SET subject_area = %s, category = %s, subcategory = %s
            WHERE id = %s
        """, (data['subject_area'], data['category'], data['subcategory'], tot_id))

        # Atualizar ou adicionar novos conteúdos
        if 'contents' in data:
            # Excluir conteúdos existentes
            cursor.execute("DELETE FROM contents WHERE tot_id = %s", (tot_id,))
            # Inserir novos conteúdos
            for content in data['contents']:
                cursor.execute("""
                    INSERT INTO contents (tot_id, content_type, content_data)
                    VALUES (%s, %s, %s)
                """, (tot_id, content['type'], content['value']))

        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "TOT e conteúdos atualizados com sucesso!"}
    except Exception as e:
        return {"error": str(e)}
    
def create_exercise_service(tot_id, data):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Inserir o exercício na tabela exercises
        cursor.execute("""
            INSERT INTO exercises (tot_id, title, professor_id, points, statement)
            VALUES (%s, %s, %s, %s, %s) RETURNING id
        """, (tot_id, data['title'], data['professor_id'], data['points'], data['statement']))

        # Obter o ID do exercício recém-criado
        exercise_id = cursor.fetchone()[0]

        # Inserir as alternativas na tabela alternatives
        for alternative in data['alternatives']:
            cursor.execute("""
                INSERT INTO alternatives (exercise_id, alternative, is_correct)
                VALUES (%s, %s, %s)
            """, (exercise_id, alternative['answer'], alternative['is_correct']))

        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Exercício criado com sucesso!"}
    except Exception as e:
        return {"error": str(e)}

def get_exercise_by_id_service(exercise_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Consulta para obter os detalhes do exercício
        cursor.execute("""
            SELECT id, title, statement, points
            FROM exercises
            WHERE id = %s
        """, (exercise_id,))
        exercise = cursor.fetchone()

        if not exercise:
            return {"message": "Exercício não encontrado"}

        # Consulta para obter as alternativas do exercício
        cursor.execute("""
            SELECT alternative, is_correct
            FROM alternatives
            WHERE exercise_id = %s
        """, (exercise_id,))
        alternatives = [
            {"answer": alt[0], "is_correct": alt[1]}
            for alt in cursor.fetchall()
        ]

        cursor.close()
        conn.close()

        return {
            "id": exercise[0],
            "title": exercise[1],
            "statement": exercise[2],
            "points": exercise[3],
            "alternatives": alternatives
        }
    except Exception as e:
        return {"error": str(e)}



def edit_exercise_service(exercise_id, data):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Verificar se o exercício existe
        cursor.execute("""
            SELECT id
            FROM exercises
            WHERE id = %s
        """, (exercise_id,))
        if not cursor.fetchone():
            return {"message": "Exercício não encontrado"}

        # Atualizar os detalhes do exercício
        cursor.execute("""
            UPDATE exercises
            SET title = %s, statement = %s, points = %s
            WHERE id = %s
        """, (data['title'], data['statement'], data['points'], exercise_id))

        # Remover as alternativas existentes
        cursor.execute("""
            DELETE FROM alternatives
            WHERE exercise_id = %s
        """, (exercise_id,))

        # Inserir as novas alternativas
        for alt in data.get('alternatives', []):
            cursor.execute("""
                INSERT INTO alternatives (exercise_id, alternative, is_correct)
                VALUES (%s, %s, %s)
            """, (exercise_id, alt['answer'], alt['is_correct']))

        conn.commit()
        cursor.close()
        conn.close()

        return {"message": "Exercício atualizado com sucesso"}
    except Exception as e:
        return {"error": str(e)}

def get_exercises_service(professor_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Buscar os exercícios do professor
        cursor.execute("""
            SELECT e.id, e.title, e.statement, e.points
            FROM exercises e
            WHERE e.professor_id = %s
        """, (professor_id,))
        
        # Recupera todos os resultados
        exercises = cursor.fetchall()

        conn.close()

        # Converte os dados em um formato adequado para o JSON
        exercise_list = [
            {"id": ex[0], "title": ex[1], "statement": ex[2], "points": ex[3]}
            for ex in exercises
        ]

        return {"exercises": exercise_list}  # Retorna um dicionário com os exercícios

    except Exception as e:
        return {"error": str(e)}
    
def get_exercises_by_tot_service(tot_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Buscar os exercícios do TOT específico
        cursor.execute("""
            SELECT e.id, e.title, e.statement, e.points
            FROM exercises e
            JOIN tots t ON e.tot_id = t.id
            WHERE t.id = %s
        """, (tot_id,))
        
        # Recupera todos os resultados
        exercises = cursor.fetchall()

        conn.close()

        # Converte os dados em um formato adequado para o JSON
        exercise_list = [
            {"id": ex[0], "title": ex[1], "statement": ex[2], "points": ex[3]}
            for ex in exercises
        ]

        return {"exercises": exercise_list}  # Retorna um dicionário com os exercícios

    except Exception as e:
        return {"error": str(e)}
    

def delete_exercise_service(exercise_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Remover alternativas associadas ao exercício (caso exista uma tabela separada para alternativas)
        cursor.execute("DELETE FROM alternatives WHERE exercise_id = %s", (exercise_id,))

        # Remover o exercício
        cursor.execute("DELETE FROM exercises WHERE id = %s", (exercise_id,))

        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Exercício removido com sucesso!"}
    except Exception as e:
        return {"error": str(e)}


