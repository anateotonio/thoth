/* podman run --name postgres-db -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=admin -e POSTGRES_DB=thothdb -p 5432:5432 -d postgres:latest


 podman exec -it postgres-db psql -U admin -d thothdb
*/

 
 CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    name VARCHAR(100) NOT NULL
);

ALTER TABLE students
ADD COLUMN quantidadeDePontos INT DEFAULT 0;

CREATE TABLE professors (
    id SERIAL PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    name VARCHAR(100) NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    birth_date DATE NOT NULL,
    subject_area VARCHAR(50) NOT NULL
);

-- Tabela de Tots
CREATE TABLE tots (
    id SERIAL PRIMARY KEY,
    professor_id INT NOT NULL,
    subject_area VARCHAR(255) NOT NULL,
    category VARCHAR(255) NOT NULL,
    subcategory VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (professor_id) REFERENCES professors (id) ON DELETE CASCADE
);

-- Tabela de Conteúdos associados ao Tot
CREATE TABLE contents (
    id SERIAL PRIMARY KEY,
    tot_id INT NOT NULL,
    content_type VARCHAR(50) NOT NULL, -- texto, link, vídeo, imagem, citação
    content_data TEXT NOT NULL,
    FOREIGN KEY (tot_id) REFERENCES tots (id) ON DELETE CASCADE
);

CREATE TABLE exercises (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    tot_id INT NOT NULL,
    professor_id INT NOT NULL,
    points INT,
    statement TEXT,
    FOREIGN KEY (tot_id) REFERENCES tots(id),
    FOREIGN KEY (professor_id) REFERENCES professors(id)
);

CREATE TABLE alternatives (
    id SERIAL PRIMARY KEY,
    exercise_id INT NOT NULL,
    alternative VARCHAR(255) NOT NULL,
    is_correct BOOLEAN NOT NULL,
    FOREIGN KEY (exercise_id) REFERENCES exercises(id) ON DELETE CASCADE
);

