/* podman run --name postgres-db -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=admin -e POSTGRES_DB=thothdb -p 5432:5432 -d postgres:latest
 podman exec -it postgres-db psql -U admin -d thothdb
*/

/*  CRIAR AS TABELAS */

CREATE DATABASE thothdb;

CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    name VARCHAR(100) NOT NULL,
    quantidadeDePontos INT DEFAULT 0,
    exerciciosconcluidos INT DEFAULT 0
);

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


/*  INSERTS */

INSERT INTO professors (email, password, name, cpf, full_name, birth_date, subject_area) 
VALUES 
('joao.silva@exemplo.com', 'senha123', 'Professor João', '12345678901', 'João da Silva', '1980-01-01', 'Matemática'),
('ana.souza@exemplo.com', 'senha456', 'Professora Ana', '23456789012', 'Ana Souza', '1985-02-02', 'Física');

INSERT INTO students (email, password, name, quantidadeDePontos, exerciciosconcluidos)
VALUES 
('lucas.oliveira@exemplo.com', 'senha123', 'Lucas Oliveira', 5000, 5),
('maria.santos@exemplo.com', 'senha456', 'Maria Santos', 1000, 3);

-- Inserir Tots para o Professor João (id = 1)
INSERT INTO tots (professor_id, subject_area, category, subcategory) 
VALUES 
(1, 'Matemática', 'Álgebra', 'Equações Lineares'),
(1, 'Matemática', 'Geometria', 'Cálculo de Áreas'),
(1, 'Matemática', 'Cálculo', 'Derivadas'),
(1, 'Matemática', 'Álgebra', 'Matrizes'),
(1, 'Matemática', 'Geometria', 'Teorema de Pitágoras'),
(1, 'Matemática', 'Cálculo', 'Limites'),
(1, 'Matemática', 'Álgebra', 'Fatores'),
(1, 'Matemática', 'Geometria', 'Volumes de sólidos'),
(1, 'Matemática', 'Cálculo', 'Integrais'),
(1, 'Matemática', 'Álgebra', 'Determinantes');

-- Inserir conteúdos para os Tots do Professor João
INSERT INTO contents (tot_id, content_type, content_data) 
VALUES
(1, 'texto', 'A equação linear é uma equação de primeiro grau. Exemplo: 2x + 3 = 5.'),
(1, 'citação', '“Uma equação linear é uma equação algébrica em que a variável aparece no primeiro grau. Exemplo clássico é a equação 2x + 3 = 5.” - Stewart, James, "Cálculo: O que todo estudante de cálculo precisa saber", 2019');
(1, 'link', 'https://www.youtube.com/embed/nvT15exeXOA'),
(1, 'imagem', 'https://content.prodigioeducacao.com/prodigio/upload/7077b3fa-fdde-442a-96f3-e74590714d00.jpeg');

(2, 'texto', 'O cálculo de áreas é uma disciplina fundamental da geometria que trata da determinação da quantidade de espaço contido dentro de uma figura plana ou bidimensional. Esse conceito é essencial para a compreensão e aplicação de muitas áreas da matemática, física, engenharia e até mesmo em problemas do cotidiano, como no cálculo de materiais para construção, plantio de áreas agrícolas ou até no planejamento de terrenos urbanos.'),
(2, 'link', 'https://www.youtube.com/embed/W-JObyKKhyc');

(3, 'texto', 'A derivada de uma função indica a taxa de variação de uma função.'),
(3, 'link', 'https://www.youtube.com/watch?v=video3'),
(3, 'imagem', 'https://example.com/imagem_derivada.jpg'),

(4, 'texto', 'Uma matriz é uma tabela organizada de números, símbolos ou expressões.'),
(4, 'link', 'https://www.youtube.com/watch?v=video4'),
(4, 'imagem', 'https://example.com/imagem_matriz.jpg'),

(5, 'texto', 'Teorema de Pitágoras: em um triângulo retângulo, o quadrado da hipotenusa é igual à soma dos quadrados dos catetos.'),
(5, 'link', 'https://www.youtube.com/watch?v=video5'),
(5, 'imagem', 'https://example.com/imagem_pitagoras.jpg'),

(6, 'texto', 'Limites são usados para estudar o comportamento das funções em pontos específicos.'),
(6, 'link', 'https://www.youtube.com/watch?v=video6'),
(6, 'imagem', 'https://example.com/imagem_limite.jpg'),

(7, 'texto', 'Fatores são números ou expressões que podem ser multiplicados para dar um produto.'),
(7, 'link', 'https://www.youtube.com/watch?v=video7'),
(7, 'imagem', 'https://example.com/imagem_fatores.jpg'),

(8, 'texto', 'Volume de sólidos é o espaço ocupado por um objeto tridimensional.'),
(8, 'link', 'https://www.youtube.com/watch?v=video8'),
(8, 'imagem', 'https://example.com/imagem_volume.jpg'),

(9, 'texto', 'Integral é a operação inversa da derivada, usada para calcular áreas sob curvas.'),
(9, 'link', 'https://www.youtube.com/watch?v=video9'),
(9, 'imagem', 'https://example.com/imagem_integral.jpg'),

(10, 'texto', 'Determinantes são valores numéricos associados a matrizes quadradas, importantes em várias áreas da álgebra linear.'),
(10, 'link', 'https://www.youtube.com/watch?v=video10'),
(10, 'imagem', 'https://example.com/imagem_determinante.jpg');

-- Inserir Tots para a Professora Ana (id = 2)
INSERT INTO tots (professor_id, subject_area, category, subcategory) 
VALUES 
(2, 'Física', 'Mecânica', 'Leis de Newton'),
(2, 'Física', 'Óptica', 'Reflexão e Refração'),
(2, 'Física', 'Termodinâmica', 'Leis da Termodinâmica'),
(2, 'Física', 'Eletromagnetismo', 'Campos Elétricos'),
(2, 'Física', 'Ondas', 'Som e Luz')

-- Inserir conteúdos para os Tots da Professora Ana
INSERT INTO contents (tot_id, content_type, content_data) 
VALUES
(11, 'texto', 'As leis de Newton descrevem a relação entre os movimentos de um objeto e as forças que agem sobre ele.'),
(11, 'link', 'https://www.youtube.com/watch?v=video11'),
(11, 'imagem', 'https://example.com/imagem_newton.jpg'),

(12, 'texto', 'Reflexão e refração são fenômenos ópticos que envolvem a mudança na direção da luz.'),
(12, 'link', 'https://www.youtube.com/watch?v=video12'),
(12, 'imagem', 'https://example.com/imagem_reflexao_reflexao.jpg'),

(13, 'texto', 'As leis da termodinâmica governam a transferência de energia em sistemas físicos.'),
(13, 'link', 'https://www.youtube.com/watch?v=video13'),
(13, 'imagem', 'https://example.com/imagem_termodinamica.jpg'),

(14, 'texto', 'Campos elétricos são gerados por cargas elétricas e influenciam outras cargas próximas.'),
(14, 'link', 'https://www.youtube.com/watch?v=video14'),
(14, 'imagem', 'https://example.com/imagem_campo_eletrico.jpg'),

(15, 'texto', 'Ondas sonoras e luminosas se propagam através de meios materiais e do vácuo.'),
(15, 'link', 'https://www.youtube.com/watch?v=video15'),
(15, 'imagem', 'https://example.com/imagem_ondas.jpg'),

/* Inserir Exercícios para o Professor João (id = 1) */
INSERT INTO exercises (title, tot_id, professor_id, points, statement) 
VALUES 
('Equação Linear 1', 1, 1, 10, 'Resolva a equação 2x + 3 = 5.'),
('Cálculo de Áreas 1', 2, 1, 15, 'Determine a área de um círculo com raio 7cm.'),
('Derivada 1', 3, 1, 20, 'Calcule a derivada de f(x) = x² + 3x.'),
('Matrizes 1', 4, 1, 25, 'Calcule a multiplicação das matrizes A e B.'),
('Teorema de Pitágoras 1', 5, 1, 15, 'Calcule o valor da hipotenusa de um triângulo retângulo com catetos de 3 e 4 metros.'),
('Limites 1', 6, 1, 20, 'Calcule o limite de f(x) = (x² - 1)/(x - 1) quando x tende a 1.'),
('Fatores 1', 7, 1, 10, 'Encontre os fatores de x² - 9.'),
('Volume de Sólidos 1', 8, 1, 30, 'Determine o volume de uma esfera de raio 6cm.'),
('Integral 1', 9, 1, 25, 'Calcule a integral de f(x) = 2x + 5.'),
('Determinantes 1', 10, 1, 20, 'Calcule o determinante da matriz A = [[2, 3], [1, 4]].');

/* Inserir Alternativas para Exercícios do Professor João */
INSERT INTO alternatives (exercise_id, alternative, is_correct) 
VALUES 
(43, 'x = 1', TRUE),
(43, 'x = -1', FALSE),
(43, 'x = 0', FALSE),
(43, 'x = 2', FALSE);

(2, 'Área = 153.94 cm²', TRUE),
(2, 'Área = 123.56 cm²', FALSE),
(2, 'Área = 100 cm²', FALSE),
(2, 'Área = 50 cm²', FALSE),

(3, 'Derivada = 2x + 3', TRUE),
(3, 'Derivada = x + 3', FALSE),
(3, 'Derivada = 2x', FALSE),
(3, 'Derivada = 3x + 2', FALSE),

(4, 'Resultado = [[5, 7], [9, 12]]', TRUE),
(4, 'Resultado = [[5, 5], [9, 8]]', FALSE),
(4, 'Resultado = [[7, 8], [5, 6]]', FALSE),
(4, 'Resultado = [[2, 1], [6, 3]]', FALSE),

(5, 'Hipotenusa = 5m', TRUE),
(5, 'Hipotenusa = 6m', FALSE),
(5, 'Hipotenusa = 4m', FALSE),
(5, 'Hipotenusa = 3m', FALSE),

(6, 'Limite = 2', TRUE),
(6, 'Limite = 1', FALSE),
(6, 'Limite = 0', FALSE),
(6, 'Limite = -1', FALSE),

(7, 'Fatores: (x - 3)(x + 3)', TRUE),
(7, 'Fatores: (x - 4)(x + 4)', FALSE),
(7, 'Fatores: (x - 5)(x + 5)', FALSE),
(7, 'Fatores: (x - 6)(x + 6)', FALSE),

(8, 'Volume = 904.32 cm³', TRUE),
(8, 'Volume = 123.56 cm³', FALSE),
(8, 'Volume = 314.16 cm³', FALSE),
(8, 'Volume = 500.00 cm³', FALSE),

(9, 'Integral = x² + 5x + C', TRUE),
(9, 'Integral = x² + 3x + C', FALSE),
(9, 'Integral = x² + 4x + C', FALSE),
(9, 'Integral = x² + 2x + C', FALSE),

(10, 'Determinante = 5', TRUE),
(10, 'Determinante = 4', FALSE),
(10, 'Determinante = 6', FALSE),
(10, 'Determinante = 10', FALSE);


/* Inserir Exercícios para a Professora Ana (id = 2) */
INSERT INTO exercises (title, tot_id, professor_id, points, statement) 
VALUES 
('Leis de Newton 1', 11, 2, 20, 'Enuncie a Primeira Lei de Newton.'),
('Reflexão e Refração 1', 12, 2, 15, 'Descreva o fenômeno da refração da luz.'),
('Leis da Termodinâmica 1', 13, 2, 25, 'Explique a Segunda Lei da Termodinâmica.'),
('Campos Elétricos 1', 14, 2, 20, 'Defina o conceito de campo elétrico.'),
('Ondas 1', 15, 2, 30, 'Explique como se propagam as ondas sonoras e luminosas.');

/* Inserir Alternativas para Exercícios da Professora Ana */
INSERT INTO alternatives (exercise_id, alternative, is_correct) 
VALUES 
(11, 'Primeira Lei: Um corpo em repouso permanecerá em repouso, e um corpo em movimento permanecerá em movimento, a menos que uma força externa atue sobre ele.', TRUE),
(11, 'Primeira Lei: A aceleração de um corpo é sempre positiva.', FALSE),
(11, 'Primeira Lei: A velocidade de um corpo nunca muda.', FALSE),
(11, 'Primeira Lei: A força é sempre inversamente proporcional à aceleração.', FALSE),

(12, 'A refração ocorre quando a luz passa de um meio para outro e sua velocidade muda.', TRUE),
(12, 'A refração é a curvatura da luz ao passar por uma superfície. ', FALSE),
(12, 'A refração ocorre quando a luz é refletida. ', FALSE),
(12, 'A refração é a dispersão da luz. ', FALSE),

(13, 'A Segunda Lei da Termodinâmica afirma que a entropia de um sistema isolado nunca diminui.', TRUE),
(13, 'A Segunda Lei da Termodinâmica afirma que a energia se conserva em todos os sistemas. ', FALSE),
(13, 'A Segunda Lei da Termodinâmica afirma que a entropia é uma medida de temperatura. ', FALSE),
(13, 'A Segunda Lei da Termodinâmica afirma que o calor se transfere sempre de um corpo quente para um corpo frio.', FALSE),

(14, 'Campo elétrico é uma região onde uma carga elétrica experimenta uma força.', TRUE),
(14, 'Campo elétrico é uma região onde não há interação entre as cargas. ', FALSE),
(14, 'Campo elétrico é uma força que age sobre objetos não carregados.', FALSE),
(14, 'Campo elétrico é uma onda de radiação. ', FALSE),

(15, 'Ondas sonoras são mecânicas e necessitam de um meio material para se propagar, enquanto as ondas luminosas são eletromagnéticas e podem se propagar no vácuo.', TRUE),
(15, 'Ondas sonoras não se propagam em meios materiais. ', FALSE),
(15, 'Ondas sonoras são eletromagnéticas. ', FALSE),
(15, 'Ondas luminosas não se propagam no vácuo. ', FALSE);


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


/*    Caso queira resetar os inserts executar

TRUNCATE TABLE alternatives CASCADE;
TRUNCATE TABLE exercises CASCADE;
TRUNCATE TABLE contents CASCADE;
TRUNCATE TABLE tots CASCADE;
TRUNCATE TABLE professors CASCADE;
TRUNCATE TABLE students RESTART IDENTITY;

*/