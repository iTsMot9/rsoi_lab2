from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
import psycopg2

app = FastAPI()

DB_CONFIG = {
    "host": "postgres",
    "database": "cars",
    "user": "program",
    "password": "test"
}

@app.get("/manage/health")
def health():
    return JSONResponse(content={"status": "OK"})

@app.get("/api/v1/cars")
def get_cars(page: int = Query(0), size: int = Query(10), showAll: bool = Query(False)):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        if showAll:
            cur.execute("""
                SELECT car_uid, brand, model, registration_number, power, price, type, availability
                FROM cars ORDER BY id LIMIT %s OFFSET %s
            """, (size, page * size))
        else:
            cur.execute("""
                SELECT car_uid, brand, model, registration_number, power, price, type, availability
                FROM cars WHERE availability = true ORDER BY id LIMIT %s OFFSET %s
            """, (size, page * size))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        cars = [
            {
                "carUid": str(r[0]),
                "brand": r[1],
                "model": r[2],
                "registrationNumber": r[3],
                "power": r[4],
                "price": r[5],
                "type": r[6],
                "availability": r[7]
            }
            for r in rows
        ]
        return JSONResponse(content=cars)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/v1/cars/{car_uid}/reserve")
def reserve_car(car_uid: str):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("UPDATE cars SET availability = false WHERE car_uid = %s", (car_uid,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Car not found")
        conn.commit()
        cur.close()
        conn.close()
        return JSONResponse(content={"status": "reserved"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/v1/cars/{car_uid}/release")
def release_car(car_uid: str):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("UPDATE cars SET availability = true WHERE car_uid = %s", (car_uid,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Car not found")
        conn.commit()
        cur.close()
        conn.close()
        return JSONResponse(content={"status": "released"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
