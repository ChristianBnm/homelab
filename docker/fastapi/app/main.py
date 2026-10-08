import os

import psycopg
from fastapi import FastAPI

app = FastAPI(title="Home Lab API")


def get_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )


@app.get("/")
def root():
    return {
        "message": "Home Lab API funcionando"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/servers")
def get_servers():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id, nombre, servicio FROM servidores ORDER BY id"
            )
            rows = cursor.fetchall()

    return [
        {
            "id": row[0],
            "nombre": row[1],
            "servicio": row[2],
        }
        for row in rows
    ]