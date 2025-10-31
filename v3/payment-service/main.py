from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
import uuid

app = FastAPI()

DB_CONFIG = {
    "host": "postgres",
    "database": "payments",
    "user": "program",
    "password": "test"
}

@app.get("/manage/health")
def health():
    return {"status": "OK"}

class CreatePaymentRequest(BaseModel):
    price: int

@app.post("/api/v1/payment")
def create_payment(req: CreatePaymentRequest):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        payment_uid = str(uuid.uuid4())
        cur.execute(
            "INSERT INTO payment (payment_uid, status, price) VALUES (%s, %s, %s)",
            (payment_uid, "PAID", req.price)
        )
        conn.commit()
        cur.close()
        conn.close()
        return {"paymentUid": payment_uid, "status": "PAID", "price": req.price}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/payment/{payment_uid}")
def get_payment(payment_uid: str):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT payment_uid, status, price FROM payment WHERE payment_uid = %s", (payment_uid,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        if not row:
            raise HTTPException(status_code=404, detail="Payment not found")
        return {"paymentUid": str(row[0]), "status": row[1], "price": row[2]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/v1/payment/{payment_uid}")
def cancel_payment(payment_uid: str):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("UPDATE payment SET status = 'CANCELED' WHERE payment_uid = %s", (payment_uid,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Payment not found")
        conn.commit()
        cur.close()
        conn.close()
        return {"status": "CANCELED"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
