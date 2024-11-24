-- Keep a log of any SQL queries you execute as you solve the mystery.
-- Buscar el reporte del crimen del 28 de julio de 2023 en Humphrey Street
SELECT *
FROM crime_scene_reports
WHERE year = 2023 AND month = 7 AND day = 28 AND street = 'Humphrey Street';

-- Obtener declaraciones de los testigos que mencionan la panadería
SELECT *
FROM interviews
WHERE transcript LIKE '%bakery%' AND year = 2023 AND month = 7 AND day = 28;

-- Buscar transacciones en el cajero automático de Leggett Street el 28 de julio de 2023
SELECT *
FROM atm_transactions
WHERE atm_location = 'Leggett Street' AND year = 2023 AND month = 7 AND day = 28;

-- Identificar al propietario de la cuenta bancaria
SELECT people.*
FROM people
JOIN bank_accounts ON people.id = bank_accounts.person_id
WHERE bank_accounts.account_number IN (
    28500762, 28296815, 76054385, 49610011, 16153065, 25506511, 81061156, 26013199
);

-- Buscar vuelos que salieron poco después del robo
SELECT *
FROM flights
WHERE year = 2023 AND month = 7 AND day >= 28;

-- Verificar quién compró el boleto del vuelo del sospechoso
SELECT *
FROM passengers
WHERE flight_id IN (1, 2, 4, 6, 7, 8, 10, 11, 12, 17, 18, 19, 20, 22, 23, 24, 27, 31, 33, 34, 35, 36, 40, 41, 42, 43, 44, 47, 48, 51, 53, 54, 57, 58)
AND passport_number IN (5773159633, 3592750733, 4408372428, 9878712108, 7049073643, 8496433585, 1988161715, 9586786673);

-- Identificar destino del vuelo 36
SELECT a.city AS destination_city
FROM flights f
JOIN airports a ON f.destination_airport_id = a.id
WHERE f.id = 36;

-- Verificar pasajeros del vuelo 36
SELECT p.name
FROM passengers ps
JOIN people p ON ps.passport_number = p.passport_number
WHERE ps.flight_id = 36;

-- Revisar llamadas telefónicas del 28 de julio de 2023
SELECT *
FROM phone_calls
WHERE year = 2023 AND month = 7 AND day = 28;

-- Identificar el número de teléfono de Bruce
SELECT phone_number
FROM people
WHERE name = 'Bruce';

-- Buscar llamadas realizadas por Bruce el 28 de julio de 2023
SELECT *
FROM phone_calls
WHERE caller = '(367) 555-5533' AND year = 2023 AND month = 7 AND day = 28;

-- Identificar a los receptores de las llamadas de Bruce
SELECT name
FROM people
WHERE phone_number IN ('(375) 555-8161', '(344) 555-9601', '(022) 555-4052', '(704) 555-5790');
-- La llamada más larga es de Robin
