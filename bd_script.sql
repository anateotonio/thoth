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

ALTER TABLE Students ADD COLUMN exerciciosconcluidos INT DEFAULT 0;


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

 CREATE TABLE missions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    points INT NOT NULL,
    progress INT DEFAULT 0,
    goal INT NOT NULL
);


INSERT INTO missions (name, description, points, progress, goal) VALUES
('Login por 7 dias consecutivos', 'Ganhe 100 pontos por entrar no Thoth por 7 dias consecutivos', 100, 0, 7),
('Completar 10 exercícios corretamente', 'Ganhe 300 pontos por acertar 10 exercícios corretamente', 300, 0, 10),
('Completar 10 exercícios', 'Ganhe 200 pontos por realizar 10 exercícios', 200, 0, 10),
('Alcançar o Nível 5', 'Ganhe 500 pontos ao alcançar o Nível 5', 500, 0, 1),
('Finalizar 5 missões', 'Ganhe 150 pontos ao completar 5 missões', 150, 0, 5),
('Ganhar 1000 pontos', 'Ganhe 1000 pontos no total', 1000, 0, 1000),
('Compartilhar perfil nas redes sociais', 'Ganhe 50 pontos ao compartilhar seu perfil nas redes sociais', 50, 0, 1),
('Completar todos os desafios diários', 'Ganhe 200 pontos ao completar todos os desafios diários', 200, 0, 1),
('Assistir 5 vídeos educativos', 'Ganhe 100 pontos por assistir a 5 vídeos educativos', 100, 0, 5),
('Participar de uma discussão em grupo', 'Ganhe 150 pontos por participar de uma discussão em grupo', 150, 0, 1);

