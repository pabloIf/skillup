from logs.crud import LogRepository
from skills.crud import SkillRepository

class UnitOfWork:
    def __init__(self, connection):
        self.conn = connection
    
    def __enter__(self):
        self.cursor = self.conn.cursor()

        self.logs = LogRepository(cursor=self.cursor)
        self.skills = SkillRepository(cursor=self.cursor)

        return self
    
    def __exit__(self, exc_type, exc, tb):
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()