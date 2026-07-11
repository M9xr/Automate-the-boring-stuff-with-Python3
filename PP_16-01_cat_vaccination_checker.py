# Cat Vaccination Checker
# Download the sweigartcats.db database of my cats from the book's resources at xxx.com. Write a program that opens this database and lists
# all cats that don't have vaccines named 'rabies', 'FeLV', 'FVRCP'. Also, check the database for errors by finding 
# all vaccines that were administrated on a date before the cat's birthday.

import sqlite3

conn = sqlite3.connect('sweigartcats.db', isolation_level=None)
rows = conn.execute("""
        SELECT rowid, name
        FROM cats c
        WHERE
            NOT EXISTS (
                SELECT 1
                FROM vaccinations v
                WHERE v.cat_id = c.rowid
                AND v.vaccine = 'rabies'
                )
            OR NOT EXISTS (
                SELECT 1
                FROM vaccinations v
                WHERE v.cat_id = c.rowid
                AND v.vaccine = 'FeLV'
                )
            OR NOT EXISTS (
                SELECT 1
                FROM vaccinations v
                WHERE v.cat_id = c.rowid
                AND v.vaccine = 'FVRCP'
            );
""").fetchall()

print("Cats missing required vaccines:")
for row in rows:
    print(row)


rows = conn.execute("""
SELECT
    c.name,
    c.birthdate,
    v.vaccine,
    v.date_administered
FROM cats c
JOIN vaccinations v
ON c.rowid = v.cat_id
WHERE v.date_administered < c.birthdate;
""").fetchall()

print("\nVaccinations before birthdate:")
for row in rows:
    print(row)

conn.close()




