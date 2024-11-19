class Student:
    def __init__(self, email, password, name):
        self.email = email
        self.password = password
        self.name = name
        # O 'id' pode ser gerado automaticamente ao salvar no banco de dados
