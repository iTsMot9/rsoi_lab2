from fastapi import FastAPI, HTTPException, Header, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import httpx
from datetime import datetime

app = FastAPI()

CARS_SERVICE = "http://cars-service:8070"
RENTAL_SERVICE = "http://rental-service:8060"
PAYMENT_SERVICE = "http://payment-service:8050"


@app.get("/manage/health")
def health():
    return JSONResponse(content={"status": "OK"})


@app.get("/api/v1/cars")
async def get_cars(page: int = Query(0), size: int = Query(10), showAll: bool = Query(False)):
    async with httpx.AsyncClient() as client:
        params = {"page": page, "size": size, "showAll": str(showAll).lower()}
        r = await client.get(f"{CARS_SERVICE}/api/v1/cars", params=params)
        r.raise_for_status()
        return JSONResponse(content={"data": r.json()})


@app.get("/api/v1/rental")
async def get_rentals(username: str = Header(..., alias="X-User-Name")):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{RENTAL_SERVICE}/api/v1/rental", headers={"X-User-Name": username})
        r.raise_for_status()
        return JSONResponse(content={"data": r.json()})


@app.get("/api/v1/rental/{rental_uid}")
async def get_rental(rental_uid: str, username: str = Header(..., alias="X-User-Name")):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{RENTAL_SERVICE}/api/v1/rental/{rental_uid}", headers={"X-User-Name": username})
        r.raise_for_status()
        return JSONResponse(content={"data": r.json()})


class RentalRequest(BaseModel):
    carUid: str
    dateFrom: str
    dateTo: str


@app.post("/api/v1/rental")
async def create_rental(req: RentalRequest, username: str = Header(..., alias="X-User-Name")):
    async with httpx.AsyncClient(timeout=10.0) as client:
        cars = await client.get(f"{CARS_SERVICE}/api/v1/cars?showAll=true")
        cars.raise_for_status()
        car = next((c for c in cars.json() if c["carUid"] == req.carUid), None)
        if not car:
            raise HTTPException(status_code=404, detail="Car not found")

        date_from = datetime.strptime(req.dateFrom, "%Y-%m-%d")
        date_to = datetime.strptime(req.dateTo, "%Y-%m-%d")
        days = (date_to - date_from).days
        total_price = car["price"] * days

        payment = await client.post(f"{PAYMENT_SERVICE}/api/v1/payment", json={"price": total_price})
        payment.raise_for_status()
        payment_data = payment.json()
        payment_uid = payment_data["paymentUid"]

        rental = await client.post(
            f"{RENTAL_SERVICE}/api/v1/rental",
            json={"carUid": req.carUid, "dateFrom": req.dateFrom, "dateTo": req.dateTo, "paymentUid": payment_uid},
            headers={"X-User-Name": username}
        )
        rental.raise_for_status()
        rental_data = rental.json()
        rental_uid = rental_data["rentalUid"]

        await client.put(f"{CARS_SERVICE}/api/v1/cars/{req.carUid}/reserve")

        return JSONResponse(content={"data": {
            "rentalUid": rental_uid,
            "carUid": req.carUid,
            "paymentUid": payment_uid,
            "dateFrom": req.dateFrom,
            "dateTo": req.dateTo,
            "status": "IN_PROGRESS"
        }})


@app.post("/api/v1/rental/{rental_uid}/finish")
async def finish_rental(rental_uid: str, username: str = Header(..., alias="X-User-Name")):
    async with httpx.AsyncClient() as client:
        rental = await client.get(f"{RENTAL_SERVICE}/api/v1/rental/{rental_uid}", headers={"X-User-Name": username})
        rental.raise_for_status()
        car_uid = rental.json()["carUid"]

        await client.put(f"{CARS_SERVICE}/api/v1/cars/{car_uid}/release")
        r = await client.post(f"{RENTAL_SERVICE}/api/v1/rental/{rental_uid}/finish", headers={"X-User-Name": username})
        r.raise_for_status()
        return JSONResponse(status_code=204)


@app.delete("/api/v1/rental/{rental_uid}")
async def cancel_rental(rental_uid: str, username: str = Header(..., alias="X-User-Name")):
    async with httpx.AsyncClient() as client:
        rental = await client.get(f"{RENTAL_SERVICE}/api/v1/rental/{rental_uid}", headers={"X-User-Name": username})
        rental.raise_for_status()
        car_uid = rental.json()["carUid"]
        payment_uid = rental.json()["paymentUid"]

        await client.delete(f"{PAYMENT_SERVICE}/api/v1/payment/{payment_uid}")
        await client.put(f"{CARS_SERVICE}/api/v1/cars/{car_uid}/release")
        r = await client.delete(f"{RENTAL_SERVICE}/api/v1/rental/{rental_uid}", headers={"X-User-Name": username})
        r.raise_for_status()
        return JSONResponse(status_code=204)
