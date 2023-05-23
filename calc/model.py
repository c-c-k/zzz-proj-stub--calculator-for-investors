import csv
import logging
from pathlib import Path

from sqlalchemy import create_engine, String, Float, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker, mapped_column

from .misc import COMPANIES_FIELDS, FINANCIAL_FIELDS

logger = logging.getLogger(__name__)

DB_PATH = Path("investor.db")
DB_URI = f"sqlite:///{DB_PATH.as_posix()}?check_same_thread=False"
engine = create_engine(DB_URI)
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class Companies(Base):
    __tablename__ = "companies"

    ticker = mapped_column(String, primary_key=True)
    name = mapped_column(String)
    sector = mapped_column(String)


class Financial(Base):
    __tablename__ = "financial"

    ticker = mapped_column(String, primary_key=True)
    ebitda = mapped_column(Float)
    sales = mapped_column(Float)
    net_profit = mapped_column(Float)
    market_price = mapped_column(Float)
    net_debt = mapped_column(Float)
    assets = mapped_column(Float)
    equity = mapped_column(Float)
    cash_equivalents = mapped_column(Float)
    liabilities = mapped_column(Float)


def load_data_from_csv(csv_path):
    data = []
    with open(csv_path) as csv_file:
        reader = csv.DictReader(csv_file)
        for csv_entry in reader:
            data_entry = {}
            for field, value in csv_entry.items():
                if str(value) == "":
                    data_entry[field] = None
                else:
                    data_entry[field] = value
            data.append(data_entry)
    return data


def load_data(session, data, model_cls):
    model_objs_to_add = [model_cls(**data_entry) for data_entry in data]
    session.add_all(model_objs_to_add)
    session.commit()


def init_db(force=False):
    if DB_PATH.exists():
        if force:
            DB_PATH.unlink()
        else:
            return False
    Base.metadata.create_all(engine)
    companies_data = load_data_from_csv('calc/datasets/companies.csv')
    financial_data = load_data_from_csv('calc/datasets/financial.csv')
    session = Session()
    load_data(session, companies_data, Companies)
    load_data(session, financial_data, Financial)
    session.close()
    return True


def split_company_data(company_data):
    companies_data = {
        field: company_data[field]
        for field in COMPANIES_FIELDS
    }
    financial_data = {
        field: company_data[field]
        for field in FINANCIAL_FIELDS
    }
    return companies_data, financial_data


def company_create(company_data):
    companies_data, financial_data = split_company_data(company_data)
    session = Session()
    companies_obj = Companies(**companies_data)
    financial_obj = Financial(**financial_data)
    session.add_all([companies_obj, financial_obj])
    session.commit()
    session.close()


def convert_model_objects_to_model_data(obj_list, model_fields):
    if len(obj_list) == 0:
        return None
    model_data = {
        getattr(obj, "ticker"): {field: getattr(obj, field) for field in model_fields}
        for obj in obj_list
    }
    return model_data


def companies_by_name(name):
    session = Session()
    companies = session.query(Companies) \
        .filter(Companies.name.contains(name)).all()
    # .filter(text("name LIKE '%:name%'")).params(name=name).all()
    session.close()
    companies_data = convert_model_objects_to_model_data(companies, COMPANIES_FIELDS)
    if companies_data is None:
        return None
    return companies_data.values()


def companies_get_all():
    session = Session()
    companies = session.query(Companies).order_by(Companies.ticker).all()
    session.close()
    return convert_model_objects_to_model_data(companies, COMPANIES_FIELDS).values()


def get_all_data():
    session = Session()
    companies = session.query(Companies).order_by(Companies.ticker).all()
    financial = session.query(Financial).order_by(Financial.ticker).all()
    session.close()
    companies_data = convert_model_objects_to_model_data(companies, COMPANIES_FIELDS)
    financial_data = convert_model_objects_to_model_data(financial, FINANCIAL_FIELDS)
    for ticker, company_data in companies_data.items():
        company_data.update(financial_data[ticker])
    return companies_data.values()


def company_read(company_data):
    session = Session()
    financial = session.query(Financial) \
        .filter(Financial.ticker == company_data['ticker']).one()
    session.close()
    company_data.update(
        {field: getattr(financial, field) for field in FINANCIAL_FIELDS}
    )
    return company_data


def company_update(company_data):
    companies_data, financial_data = split_company_data(company_data)
    session = Session()
    for model, data in (
            (Companies, companies_data), (Financial, financial_data)):
        model_obj = session.query(model) \
            .filter(model.ticker == data['ticker']).one()
        for field, new_value in data.items():
            setattr(model_obj, field, new_value)
    session.commit()
    session.close()


def company_delete(company_data):
    session = Session()
    company = session.query(Companies) \
        .filter(Companies.ticker == company_data['ticker']).one()
    financial = session.query(Financial) \
        .filter(Financial.ticker == company_data['ticker']).one()
    session.delete(company)
    session.delete(financial)
    session.commit()
