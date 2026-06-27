import pandas as pd
from sqlalchemy import create_engine

def get_engine():
    return create_engine(
        "mysql+pymysql://root@127.0.0.1:3306/supplier_quality_analytics",
        connect_args={"connect_timeout": 5}
    )

def load_supplier_performance():
    engine = get_engine()
    return pd.read_sql("SELECT * FROM vw_supplier_performance", engine)

def load_monthly_trends():
    engine = get_engine()
    return pd.read_sql("SELECT * FROM vw_monthly_supplier_trends", engine)