-- Keep a log of any SQL queries you execute as you solve the mystery.

--Explore the tables that are available
.schema

--Get crime scene report to understand what happened:
SELECT description
FROM crime_scene_reports
WHERE month = 7 AND day = 28
AND street = 'Humphrey Street'

--Read through the interviews for that day
SELECT name, transcript
FROM interviews
WHERE month = 7 AND day = 28;

--disoveries
--a) thief left bakery parking lot in a car, maybe cameras got the plates
--b) thief was seen withdrawing money from an atm earlier that morning
--c) thief made a phone call to someone when leaving the bakery
--d) thief was planning to take a flight purchased by accomplace the day after the robbery

--There were only several withrdawls from legget street atm that day o I'll cross reference that with something else
SELECT *
FROM atm_transactions
WHERE month = 7 AND day = 28
AND atm_location = 'Leggett Street'

--this will give me license plates of people who used the atm to withdraw money from leggett street atm
SELECT people.name, people.license_plate
FROM atm_transactions
JOIN bank_accounts
ON atm_transactions.account_number = bank_accounts.account_number
JOIN people
ON people.id = bank_accounts.person_id
WHERE month = 7 AND day = 28
AND atm_location = 'Leggett Street'
AND transaction_type = 'withdraw';

--did a cross reference with the security camera plates caught leaving and narrowed down to five suspects:
--Bruce, Diana, Iman, Loca, Taylor
SELECT people.name, people.license_plate
FROM atm_transactions
JOIN bank_accounts
ON atm_transactions.account_number = bank_accounts.account_number
JOIN people
ON people.id = bank_accounts.person_id
WHERE month = 7 AND day = 28
AND atm_location = 'Leggett Street'
AND transaction_type = 'withdraw'
AND people.license_plate IN
(SELECT license_plate FROM bakery_security_logs
WHERE month = 7 AND day = 28 AND activity = 'exit');

--cross referening who made calls of less than 60 seconds reveals Bruce, Taylor and Diana
SELECT *, people.name FROM phone_calls
JOIN people
ON people.phone_number = phone_calls.caller
WHERE month = 7 AND day = 28
AND caller in
(SELECT people.phone_number
FROM atm_transactions
JOIN bank_accounts
ON atm_transactions.account_number = bank_accounts.account_number
JOIN people
ON people.id = bank_accounts.person_id
WHERE month = 7 AND day = 28
AND atm_location = 'Leggett Street'
AND transaction_type = 'withdraw'
AND people.license_plate IN
(SELECT license_plate FROM bakery_security_logs
WHERE month = 7 AND day = 28 AND activity = 'exit'))
AND duration < 60;

--next I checked if any left on the earliest flight out, Bruce and Taylor were on the earlier flight the next day:
SELECT *, people.name FROM FLIGHTS
JOIN passengers
ON passengers.flight_id = flights.id
JOIN people
ON people.passport_number = passengers.passport_number
WHERE month = 7 AND day = 29
AND people.name in
(SELECT people.name FROM phone_calls
JOIN people
ON people.phone_number = phone_calls.caller
WHERE month = 7 AND day = 28
AND caller in
(SELECT people.phone_number
FROM atm_transactions
JOIN bank_accounts
ON atm_transactions.account_number = bank_accounts.account_number
JOIN people
ON people.id = bank_accounts.person_id
WHERE month = 7 AND day = 28
AND atm_location = 'Leggett Street'
AND transaction_type = 'withdraw'
AND people.license_plate IN
(SELECT license_plate FROM bakery_security_logs
WHERE month = 7 AND day = 28 AND activity = 'exit'))
AND duration < 60)

--Robin, James, and Philipp were receivers of a call from the potential robber, lets check their atm activity
--Robin had over 200 in deposits after the day of the robbery, more than the amounts of the other potential accomplices, not conclusive but very suspicious
SELECT SUM(amount) FROM atm_transactions
JOIN bank_accounts
ON bank_accounts.account_number = atm_transactions.account_number
JOIN people
ON people.id = bank_accounts.person_id
WHERE atm_transactions.account_number IN
(SELECT account_number FROM phone_calls
JOIN people
ON people.phone_number = phone_calls.receiver
JOIN bank_accounts
ON people.id = bank_accounts.person_id
WHERE month = 7 AND day = 28
AND caller in
(SELECT people.phone_number
FROM atm_transactions
JOIN bank_accounts
ON atm_transactions.account_number = bank_accounts.account_number
JOIN people
ON people.id = bank_accounts.person_id
WHERE month = 7 AND day = 28
AND atm_location = 'Leggett Street'
AND transaction_type = 'withdraw'
AND people.license_plate IN
(SELECT license_plate FROM bakery_security_logs
WHERE month = 7 AND day = 28 AND activity = 'exit'))
AND duration < 60)
AND TRANSACTION_TYPE = 'deposit'
AND DAY > 27
AND people.name = 'Robin';

--Assuming Robin is the thief, that means that the caller who is Bruce is the thief:
SELECT name FROM people
WHERE phone_number =
(SELECT caller FROM phone_calls
JOIN people
ON people.phone_number = phone_calls.receiver
WHERE month = 7 AND day = 28
AND caller in
(SELECT people.phone_number
FROM atm_transactions
JOIN bank_accounts
ON atm_transactions.account_number = bank_accounts.account_number
JOIN people
ON people.id = bank_accounts.person_id
WHERE month = 7 AND day = 28
AND atm_location = 'Leggett Street'
AND transaction_type = 'withdraw'
AND people.license_plate IN
(SELECT license_plate FROM bakery_security_logs
WHERE month = 7 AND day = 28 AND activity = 'exit'))
AND duration < 60
AND NAME = 'Robin');

--Bruce flew to New York City the next day:
SELECT city FROM airports
WHERE id =
(SELECT destination_airport_id FROM FLIGHTS
JOIN passengers
ON passengers.flight_id = flights.id
JOIN people
ON people.passport_number = passengers.passport_number
WHERE month = 7 AND day = 29
AND people.name in
(SELECT people.name FROM phone_calls
JOIN people
ON people.phone_number = phone_calls.caller
WHERE month = 7 AND day = 28
AND caller in
(SELECT people.phone_number
FROM atm_transactions
JOIN bank_accounts
ON atm_transactions.account_number = bank_accounts.account_number
JOIN people
ON people.id = bank_accounts.person_id
WHERE month = 7 AND day = 28
AND atm_location = 'Leggett Street'
AND transaction_type = 'withdraw'
AND people.license_plate IN
(SELECT license_plate FROM bakery_security_logs
WHERE month = 7 AND day = 28 AND activity = 'exit'))
AND duration < 60
AND NAME = 'Bruce'));
