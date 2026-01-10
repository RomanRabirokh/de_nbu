from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from db import get_client
from nbu.repository import Repository

def extract(**context):
    ds = context["ds"]
    date_str = datetime.strptime(ds, "%Y-%m-%d").strftime("%d.%m.%Y")
    
    repo = Repository()
    data = repo.get_rates(date=date_str)
    
    return data

def transform(**context):
    """
    Converting raw data from Extract to Load.
    raw_data: list[dict] — data from the API
    Returns: list[dict] — ready for Load
    """
    raw_data = context['ti'].xcom_pull(task_ids='extract')
    transformed = []

    for item in raw_data:
        # --- 1️⃣Date ---
        start_date = item.get("StartDate")
        if start_date and isinstance(start_date, str):
            day, month, year = map(int, start_date.split("."))
            date_obj = datetime(year, month, day).date()
        elif isinstance(start_date, datetime):
            date_obj = start_date.date()
        else:
            date_obj = start_date

        # --- 2️⃣Amount ---
        units = int(item.get("Units", 1))
        amount = float(item.get("Amount", 0))
        amount_per_unit = round(amount / units, 4)

        # --- 3️⃣Currency code ---
        currency_code = item.get("CurrencyCodeL", "").lower()

        # --- 4️⃣ Generate a unique ID ---
        id = f"{currency_code}_{date_obj.strftime('%Y%m%d')}"

        # --- 5️⃣ Putting together the finished recording ---
        db_record = {
            "id": id,
            "currency": currency_code,
            "rate": amount_per_unit,
            "date": date_obj,
            "updated_at": datetime.now()
        }

        transformed.append(db_record)

    return transformed

def load(**context):
    data = context['ti'].xcom_pull(task_ids='transform')
    
    client = get_client()
    # insert data
    rows = [
        (
            row['id'],
            row['currency'],
            row['rate'],
            row['date'],
            row['updated_at']
        )
        for row in data
    ]

    client.execute(
        'INSERT INTO nbu.rates (id, currency, rate, date, updated_at) VALUES',
        rows
    )

    print(f"Inserted {len(rows)} rows into ClickHouse")

with DAG(
    dag_id="nbu_rates",
    start_date=datetime(2026, 1, 1),
    schedule_interval="@daily",
    catchup=True,
    is_paused_upon_creation=False,
    tags=["nbu"],
) as dag:
    
    extract_operator = PythonOperator(
        task_id="extract",
        python_callable=extract,
        provide_context=True
    )

    transform_operator = PythonOperator(
        task_id="transform",
        python_callable=transform,
        provide_context=True
    )

    load_operator = PythonOperator(
        task_id='load',
        python_callable=load,
        provide_context=True
    )

    extract_operator >> transform_operator  >> load_operator
