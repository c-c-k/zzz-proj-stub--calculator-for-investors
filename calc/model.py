import csv
from pathlib import Path

from sqlalchemy import create_engine, String, Float
from sqlalchemy.orm import DeclarativeBase, sessionmaker, mapped_column

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


