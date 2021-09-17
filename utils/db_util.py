from typing import List
from utils.json_util import try_get_from_dict
from icecream import ic
from sqlalchemy import Integer, Column, String, create_engine, BigInteger, ForeignKey, BOOLEAN, REAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, InstrumentedAttribute, relationship
import commands
import config_interpreter
import constant

path_alchemy_local = config_interpreter.alchemy_db_path

Base = declarative_base()


# todo create db_util tests
# region db engine
def create_db():
    engine_db = get_engine_by_path(engine_path=path_alchemy_local)
    Base.metadata.create_all(bind=engine_db)


def _get_session():
    engine_session = get_engine_by_path(engine_path=path_alchemy_local)
    session_creator = sessionmaker(bind=engine_session)
    return session_creator()


def get_engine_by_path(engine_path):
    """put db path to create orm engine"""
    # --echo back to true, show all sqlalchemy debug info
    engine_path = create_engine(engine_path, echo=False)
    return engine_path


session = _get_session()


# endregion


# region tables
class UserStatements(Base):
    __tablename__ = "user_statements"

    chat_id = Column('chat_id', Integer, unique=True, primary_key=True)
    statement = Column('statement', String, unique=False)
    username = Column('username', String, unique=False)

    def __repr__(self):
        return '{}{}{}'.format(self.chat_id, self.statement, self.username)


class Admin(Base):
    __tablename__ = 'admin_table'

    chat_id = Column('chat_id', Integer, unique=True, primary_key=True)
    username = Column('username', String, unique=False)

    def __repr__(self):
        return 'ADMIN-{}{}'.format(self.chat_id, self.username)


class FreeFlat(Base):
    __tablename__ = 'free_flat'

    flat_id = Column('flat_id', BigInteger, unique=True, primary_key=True, autoincrement=True)
    price = Column('price', BigInteger, default=0, unique=False)
    price_m2 = Column('price_m2', BigInteger, default=0, unique=False)
    currency = Column('currency', String, unique=False)
    rooms = Column('rooms', Integer, default=1, unique=False)
    floor = Column('floor', Integer, default=1, unique=False)
    total_area = Column('total_area', REAL, default=0, unique=False)
    section_id = Column('house_section_id', BigInteger, ForeignKey('house_section.section_id'))
    section = relationship('HouseSection', back_populates="flats")


class HouseSection(Base):
    __tablename__ = 'house_section'
    section_id = Column('section_id', BigInteger, unique=True, primary_key=True, autoincrement=True, )
    section_name = Column('section_name', String, unique=False)
    house_obj_id = Column('house_obj_id_foreign', BigInteger, ForeignKey('house_obj.house_id'))
    parking = Column('parking', BOOLEAN, unique=False, default=False)
    house = relationship('HouseObj', back_populates="sections")
    flats = relationship("FreeFlat", back_populates="section")
    # solved create tables


class HouseObj(Base):
    __tablename__ = 'house_obj'
    house_id = Column('house_id', BigInteger, unique=True, primary_key=True, autoincrement=True)
    house_name = Column('house_name', String, unique=False)
    location = Column('location', String, unique=False)
    sections = relationship(HouseSection, back_populates="house")


# endregion


# region crud methods
def from_db_get_statement(chat_id, message_text, first_name):
    chat_id = chat_id
    message_is_command = commands.select_statement_via_present_command(message_text)
    # check for new user
    with session:
        # if user not created
        user = session.query(UserStatements).filter_by(chat_id=chat_id).first()
        if not (user and user.statement):
            # user creating
            session.query(UserStatements).filter_by(chat_id=chat_id).delete()
            session.commit()
            user = UserStatements()
            # user created
            user.statement = constant.StartMenu.START_MENU
            user.chat_id = chat_id
            user.username = first_name
            session.add(user)
            command_st = user.statement
        else:
            assert isinstance(user, UserStatements)
            command_st = user.statement

        # get statement
        if message_is_command:
            command_st = message_is_command
            assert isinstance(user, UserStatements)
            #  must update statement
            user.statement = command_st
        session.commit()

    return command_st


# endregion


# region abstract get_from_db
def get_from_db_in_filter(table_class, identifier, value, get_type):
    """:param table_class - select table
    :param identifier - select filter column
    :param value - enter value to column
    :param get_type - string 'many' or 'one'"""
    many = 'many'
    one = 'one'
    assert isinstance(identifier, InstrumentedAttribute)
    with session:
        if get_type == one:
            obj = session.query(table_class). \
                filter(identifier.contains(value)).first()

            return obj
        elif get_type == many:
            objs = session.query(table_class). \
                filter(identifier.contains(value)).all()

            return objs


def get_from_db_eq_filter_not_editing(table_class, identifier=None, value=None, get_type='one', eq: bool = True,
                                      all_objects: bool = None):
    """WARNING! DO NOT USE THIS OBJECT TO EDIT DATA IN DATABASE! IT ISN`T WORK!
    USE ONLY TO SHOW DATA...
    :param table_class - select table
    :param identifier - select filter column
    :param value - enter value to column
    :param get_type - string 'many' or 'one'
    :param eq - choose the value equals to column or not
    :param all_objects - return all rows from table"""
    many = 'many'
    one = 'one'
    with session:
        if all_objects is True:
            objs = session.query(table_class).all()

            return objs
        assert isinstance(identifier, InstrumentedAttribute)
        if get_type == one:
            if eq:
                obj = session.query(table_class). \
                    filter(identifier == value).first()
            else:
                obj = session.query(table_class). \
                    filter(identifier != value).first()

            return obj
        elif get_type == many:
            if eq:
                objs = session.query(table_class). \
                    filter(identifier == value).all()
            else:
                objs = session.query(table_class). \
                    filter(identifier != value).all()

            return objs


def get_from_db_multiple_filter(table_class, identifier_to_value: list, get_type='one',
                                all_objects: bool = None):
    """WARNING! DO NOT USE THIS OBJECT TO EDIT DATA IN DATABASE! IT ISN`T WORK!
    USE ONLY TO SHOW DATA...
    :param table_class - select table
    :param identifier_to_value: - select filter column example [UserStatements.statement == 'hello_statement',next]
    note that UserStatements.statement is instrumented attribute
    :param get_type - string 'many' or 'one'
    :param all_objects - return all rows from table"""
    many = 'many'
    one = 'one'
    with session:
        if all_objects is True:
            objects = session.query(table_class).all()

            return objects
        if get_type == one:
            obj = session.query(table_class).filter(*identifier_to_value).first()

            return obj
        elif get_type == many:
            objects = session.query(table_class).filter(*identifier_to_value).all()

            return objects


# endregion


# region abstract write


def write_obj_to_table(table_class, identifier=None, value=None, **column_name_to_value):
    """column name to value must be exist in table class in columns"""
    # get obj
    with session:
        is_new = False
        if identifier:
            tab_obj = session.query(table_class).filter(identifier == value).first()
        else:
            tab_obj = table_class()
            is_new = True

        # is obj not exist in db, we create them
        if not tab_obj:
            tab_obj = table_class()
            is_new = True
        for col_name, val in column_name_to_value.items():
            tab_obj.__setattr__(col_name, val)
        # if obj created jet, we add his to db
        if is_new:
            session.add(tab_obj)
        # else just update
        session.commit()


def write_objects_to_table(table_class, object_list: List[dict], params_to_dict: list, params_to_db: list, identifier,
                           value_name):
    """column name to value must be exist in table class in columns"""
    # get obj
    with session:
        # is obj not exist in db, we create them
        for dict_obj in object_list:
            is_new = False
            tab_obj = get_from_db_eq_filter_not_editing(table_class, identifier, dict_obj[value_name])
            if not tab_obj:
                is_new = True
                tab_obj = table_class()
            for d_value, column in zip(params_to_dict, params_to_db):
                value = dict_obj[d_value]
                tab_obj.__setattr__(column, value)

            # if obj created jet, we add his to db
            if is_new:
                session.add(tab_obj)
                session.commit()
            else:
                # else just update
                session.commit()


# endregion


# region abstract edit
# test this method
def edit_obj_in_table(table_class, identifier=None, value=None, **column_name_to_value):
    """column name to value must be exist in table class in columns"""
    # get bj
    with session:
        tab_obj = session.query(table_class).filter(identifier == value).first()

        if tab_obj:
            for col_name, val in column_name_to_value.items():
                tab_obj.__setattr__(col_name, val)
        session.commit()


# endregion


# region abstract delete from db
def delete_obj_from_table(table_class, identifier=None, value=None):
    """column name to value must be exist in table class in columns"""
    with session:
        result = session.query(table_class).filter(identifier == value).delete()
        ic('affected {} rows'.format(result))
        session.commit()


# endregion


# region arithmetics
def get_count(table_class):
    with session:
        rows = session.query(table_class).count()

        return rows


def get_first(table_class):
    # work on func min
    with session:
        row = session.query(table_class).first()

        return row

    # solved save data in db


def save_obj_house(obj_house: dict):
    print("save obj house: ", obj_house, "...")
    name, house_id = try_get_from_dict(obj_house, ['value_tuple'])
    location = "undefined"
    write_obj_to_table(table_class=HouseObj,
                       identifier=HouseObj.house_id,
                       value=house_id,
                       house_id=house_id,
                       house_name=name,
                       location=location)
    print(f'house {name} saved.')


def save_house_sections(house_section: dict):
    print("save house section: ", house_section, "...")
    section_id, parking, house_id = try_get_from_dict(house_section, ['value_tuple'])
    section_name = f"{house_id}#{section_id}"
    write_obj_to_table(table_class=HouseSection,
                       identifier=HouseSection.section_id,
                       value=section_id,
                       section_name=section_name,
                       parking=True if parking == '1' else False,
                       house_obj_id=house_id,
                       section_id=section_id)
    print(f'house section {section_name} saved.')


def save_flat_list(flat_list: List[dict]):
    if flat_list:
        target_flat = flat_list[0]
        params_to_dict = ['price', 'flat_id', 'rooms', 'floor', 'area', 'section_id', 'price_m2', 'currency']
        params_to_db = ['price', 'flat_id', 'rooms', 'floor', 'total_area', 'section_id', 'price_m2', 'currency']
        # solved check this moment
        write_objects_to_table(table_class=FreeFlat,
                               object_list=flat_list,
                               params_to_dict=params_to_dict,
                               params_to_db=params_to_db,
                               identifier=FreeFlat.flat_id,
                               value_name='flat_id')


def save_data_to_db(prepared_data: dict):
    ic('save data in DATA...base')
    house_obj = try_get_from_dict(prepared_data, ['house_obj'])
    sections = try_get_from_dict(prepared_data, ['house_obj', 'sections'])
    # save house obj
    save_obj_house(house_obj)
    for pre_section in sections:
        section = try_get_from_dict(pre_section, ['section'])
        # save section
        save_house_sections(section)
        flats_in_section = try_get_from_dict(section, ['free_flats'])
        # dave flats
        if flats_in_section:
            save_flat_list(flats_in_section)
    print(prepared_data)

# endregion
