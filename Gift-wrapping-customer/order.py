import sqlite3


# this is the Customer order, it reflects the database structure
class Order:
    def __init__(self):
        self.account_id = None
        self.drop_off_date = None
        self.pick_up_date = None
        self.total_price = 0

# Once the order is completed it is uploaded to the databse

    def upload_order_to_database(self):
        conn = sqlite3.connect('../Gift wrapping database.db')
        cur = conn.cursor()

        cur.execute(f"INSERT INTO orders (account_id, drop_off_date, pick_up_date, total_price) VALUES (?,?,?,?)",
                    (self.account_id, self.drop_off_date, self.pick_up_date, self.total_price))
        conn.commit()
        conn.close()
