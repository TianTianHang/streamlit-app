from sqlalchemy.exc import SQLAlchemyError
from model.Word import Word
from model.WordCategory import WordCategory
from model.WordInfo import WordInfo


def add_word_category(session, name):
    try:
        category = WordCategory(name=name)
        session.add(category)
        session.commit()
        return category
    except SQLAlchemyError as e:
        session.rollback()
        raise e


def add_word(session, name, category_id):
    try:
        word = Word(name=name, category_id=category_id)
        session.add(word)
        session.commit()
        return word
    except SQLAlchemyError as e:
        session.rollback()
        raise e


def add_word_info(session, word_id, title, content):
    try:
        info = WordInfo(word_id=word_id, title=title, content=content)
        session.add(info)
        session.commit()
        return info
    except SQLAlchemyError as e:
        session.rollback()
        raise e


def get_word_category(session, category_id):
    return session.query(WordCategory).filter_by(id=category_id).first()


def get_word_category_id(session, category):
    return session.query(WordCategory).filter_by(category=category).first()


def get_word(session, word_id):
    return session.query(Word).filter_by(id=word_id).first()


def get_word_id(session, word):
    return session.query(Word).filter_by(name=word).first()


def get_word_info(session, info_id):
    return session.query(WordInfo).filter_by(id=info_id).first()


def update_word_by_id(session, word_id, new_name):
    try:
        row_num = session.query(Word).filter_by(id=word_id).update(name=new_name)
        return row_num > 0
    except SQLAlchemyError as e:
        session.rollback()
        raise e


def delete_word(session, word_id):
    try:
        row_num = session.query(Word).filter_by(id=word_id).delete()
        return row_num > 0
    except SQLAlchemyError as e:
        session.rollback()
        raise e


def get_all_words(session):
    try:
        word_categories = session.query(WordCategory).all()
        word_dict = {}

        for category in word_categories:
            words = session.query(Word).filter_by(category_id=category.id).all()
            word_dict[category.name] = [word for word in words]

        return word_dict
    except SQLAlchemyError as e:
        session.rollback()
        raise e
