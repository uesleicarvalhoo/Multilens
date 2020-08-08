from multilens.ext.db.models import Employees
from multilens.ext.db import db

def create_db():
    """Cria o banco de dados"""
    db.create_all()

def drop_db():
    """Limpa o banco de dados"""
    db.drop_all()

def populate_db():
    """Cria um usuario no banco de dados"""
    data = [
        Employees(),
    ]

    db.session.bulk_save_objects(data)
    db.session.commit()

    return Employees.query.all()

def validate_user(user: str, password: str):
    print(user, password)
    if user == 'uesleicarvalho' and password == 'ues11052011':
        return True

    return False

def list_employees():
    return "Lista com todos os funcionarios da Multilens"
