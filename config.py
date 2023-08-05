import os

config = {
    'SQLALCHEMY_DATABASE_URI':  os.getenv('DATABASE_FILE', 'sqlite:///db/WordDB.db'),
    'SECRET_KEY': os.getenv('SECRET_KEY', 'dev')
}
