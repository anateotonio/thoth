class Exercise:
    def __init__(self, title, statement, points, professor_id):
        self.title = title
        self.statement = statement
        self.points = points
        self.professor_id = professor_id
        self.alternatives = []  # Lista de alternativas associadas ao exercício
    
    def add_alternative(self, alternative):
        self.alternatives.append(alternative)
