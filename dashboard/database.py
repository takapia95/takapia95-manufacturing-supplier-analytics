import pandas as pd
from sqlalchemy import create_engine


def get_engine():
    return create_engine(
        "mysql+pymysql://root@127.0.0.1:3306/supplier_quality_analytics",
        connect_args={"connect_timeout": 5}
    )


def run_query(query):
    engine = get_engine()
    return pd.read_sql(query, engine)


def load_supplier_performance():
    return run_query("SELECT * FROM vw_supplier_performance")


def load_monthly_trends():
    return run_query("SELECT * FROM vw_monthly_supplier_trends")


def load_delivery_summary():
    return run_query("SELECT * FROM vw_delivery_summary")


def load_inventory_summary():
    return run_query("SELECT * FROM vw_inventory_summary")


def load_corrective_action_status():
    return run_query("SELECT * FROM vw_corrective_action_status")


def load_executive_kpis():
    return run_query("SELECT * FROM vw_executive_kpis")