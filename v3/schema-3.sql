CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Cars table
CREATE TABLE cars (
    id SERIAL PRIMARY KEY,
    car_uid UUID UNIQUE NOT NULL DEFAULT uuid_generate_v4(),
    brand VARCHAR(80) NOT NULL,
    model VARCHAR(80) NOT NULL,
    registration_number VARCHAR(20) NOT NULL,
    power INT,
    price INT NOT NULL,
    type VARCHAR(20) CHECK (type IN ('SEDAN', 'SUV', 'MINIVAN', 'ROADSTER')),
    availability BOOLEAN NOT NULL
);

INSERT INTO cars (car_uid, brand, model, registration_number, power, price, type, availability)
VALUES ('109b42f3-198d-4c89-9276-a7520a7120ab', 'Mercedes Benz', 'GLA 250', 'ЛО777Х799', 249, 3500, 'SEDAN', true);
--INSERT INTO cars (car_uid, brand, model, registration_number, power, price, type, availability)
--VALUES ('109b42f3-198d-4c89-9276-a7520a7120ac', 'BMW', 'M5', 'ЛО888Х799', 249, 3499, 'SEDAN', true);
--INSERT INTO cars (car_uid, brand, model, registration_number, power, price, type, availability)
--VALUES ('109b42f3-198d-4c89-9276-a7520a7120ad', 'Audi', '100', 'ЛО555Х799', 450, 4500, 'SEDAN', true);
--INSERT INTO cars (car_uid, brand, model, registration_number, power, price, type, availability)
--VALUES ('109b42f3-198d-4c89-9276-a7520a7120ae', 'Porshe', '911', 'ЛО666Х799', 500, 6500, 'SEDAN', true);
--INSERT INTO cars (car_uid, brand, model, registration_number, power, price, type, availability)
--VALUES ('109b42f3-198d-4c89-9276-a7520a7120af', 'Ferrari', '12Cilindri', 'ЛО999Х799', 600, 7500, 'SEDAN', true);
--INSERT INTO cars (car_uid, brand, model, registration_number, power, price, type, availability)
--VALUES ('109b42f3-198d-4c89-9276-a7520a7120ag', 'Skoda', 'Octavia', 'ЛО000Х799', 150, 1500, 'SEDAN', true);
--INSERT INTO cars (car_uid, brand, model, registration_number, power, price, type, availability)
--VALUES ('109b42f3-198d-4c89-9276-a7520a7120ah', 'Mercedes Benz', 'B180', 'ЛО111Х799', 180, 2000, 'SEDAN', true);
--INSERT INTO cars (car_uid, brand, model, registration_number, power, price, type, availability)
--VALUES ('109b42f3-198d-4c89-9276-a7520a7120ai', 'Audi', 'Q8', 'ЛО222Х799', 0, 8500, 'SEDAN', true);
--INSERT INTO cars (car_uid, brand, model, registration_number, power, price, type, availability)
--VALUES ('109b42f3-198d-4c89-9276-a7520a7120aj', 'Porshe', 'Tycan', 'ЛО333Х799', 0, 8500, 'SEDAN', true);
--INSERT INTO cars (car_uid, brand, model, registration_number, power, price, type, availability)
--VALUES ('109b42f3-198d-4c89-9276-a7520a7120ak', 'Reno', 'Logan', 'ЛО444Х799', 100, 500, 'SEDAN', true);
--INSERT INTO cars (car_uid, brand, model, registration_number, power, price, type, availability)
--VALUES ('109b42f3-198d-4c89-9276-a7520a7120al', 'Lada', 'Vesta', 'ЛО777Х999', 1000, 1000, 'SEDAN', true);
--INSERT INTO cars (car_uid, brand, model, registration_number, power, price, type, availability)
--VALUES ('109b42f3-198d-4c89-9276-a7520a7120am', 'GAZ', 'Volga', 'ЛО000Х799', 110, 2700, 'SEDAN', true);
--INSERT INTO cars (car_uid, brand, model, registration_number, power, price, type, availability)
--VALUES ('109b42f3-198d-4c89-9276-a7520a7120an', 'Jeep', 'Rubicon', 'ЛО666Х666', 666, 6666, 'SEDAN', true);

-- Rental table
CREATE TABLE rental (
    id SERIAL PRIMARY KEY,
    rental_uid UUID UNIQUE NOT NULL DEFAULT uuid_generate_v4(),
    username VARCHAR(80) NOT NULL,
    payment_uid UUID NOT NULL,
    car_uid UUID NOT NULL,
    date_from TIMESTAMP WITH TIME ZONE NOT NULL,
    date_to TIMESTAMP WITH TIME ZONE NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('IN_PROGRESS', 'FINISHED', 'CANCELED'))
);

-- Payment table
CREATE TABLE payment (
    id SERIAL PRIMARY KEY,
    payment_uid UUID NOT NULL DEFAULT uuid_generate_v4(),
    status VARCHAR(20) NOT NULL CHECK (status IN ('PAID', 'CANCELED')),
    price INT NOT NULL
);
