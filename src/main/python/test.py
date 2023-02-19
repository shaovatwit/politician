import data.postgres_connection

con, cur, db = data_schema.get_db()

def setup():
    insert_politician = 'INSERT INTO Politician (politician_id, name, gov_link, campaign_link, email, phone, address, party, date_elected, biography, district) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
    politician_values = (1, "John Doe", "link", "cLink", "john@doe.com", "617-352-1241", "123 adddress", "democrat", "1999-01-08", "wee woo", "idek")

    insert_city = 'INSERT INTO City (city_id, politician_id, name, state) VALUES (%s, %s, %s, %s)'
    city_value = (1, 1, "Boston", "MA")

    db(insert_politician, politician_values, insert_city, city_value)
    con.commit()