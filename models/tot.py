from datetime import datetime

class Tot():

    def __init__(self, professor_id, subject_area, category, subcategory, contents=None):
        self.professor_id = professor_id
        self.subject_area = subject_area
        self.category = category
        self.subcategory = subcategory
        self.contents = contents or []
        


