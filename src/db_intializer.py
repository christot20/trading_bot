from mysql.connector import connect
from src.config import db_password

class db:
    def __init__(self, table):
        self.table = table
        self.cnx = connect(
            host="localhost",
            port=3306,
            user="root",
            password=db_password,
            database="purchase_history")
        self.cursor = self.cnx.cursor(buffered=True)
    
    def table_inserter(self, insertions):
        insert_query = f"""
        INSERT INTO {self.table} (ticker, status, amount, price, date, account_value)
        VALUES(%s, %s, %s, %s, %s, %s)
        """
        self.cursor.executemany(insert_query, insertions)
        self.cnx.commit()
             
    def table_creator(self):
        create_table_query = f"""
        CREATE TABLE {self.table}(
            id INT AUTO_INCREMENT PRIMARY KEY,
            ticker VARCHAR(5),
            status VARCHAR(4),
            amount INT,
            price DECIMAL(9,2),
            date DATETIME,
            account_value DECIMAL(9,2)
        )
        """
        show_table_query = f"DESCRIBE {self.table}" 
        # maybe add another column to show how much account costs?
        
        self.cursor.execute(create_table_query)
        self.cursor.execute(show_table_query)
        result = self.cursor.fetchall()
        self.cnx.commit()
        return result
    
    def table_contents(self):
        select_query = f"SELECT * FROM {self.table}"
        self.cursor.execute(select_query)
        result = self.cursor.fetchall() # gonna wanna get that date time from the orders to then inser into here
        fresult = [str(row) for row in result]
        return fresult

    

# db_thing = db("reddit_method")
# insertions = [
#         ("AMC", 45, 18.36, "2022-08-16 13:23:44", 140533.69),
#         ("GME", 13, 41.89, "2022-08-17 09:33:15", 93532.01),
#         ("BBBY", 7, 32.54, "2022-08-17 15:45:21", 1543765.72)
#     ]
# db_thing.table_inserter(insertions)
# db_thing.table_creator()


# uncomment to use

    # # Connect to server
    # with mysql.connector.connect(
    #     host="localhost",
    #     port=3306,
    #     user="root",
    #     password=db_password,
    #     database="purchase_history"
    # ) as connection:
    # #     create_table_query = """
    # # CREATE TABLE ai_method(
    # #     id INT AUTO_INCREMENT PRIMARY KEY,
    # #     ticker VARCHAR(5),
    # #     amount INT,
    # #     price FLOAT,
    # #     date DATETIME
    # # )
    # # """
    # #     show_table_query = "DESCRIBE ai_method"

    #     # insert_query = """
    #     # INSERT INTO reddit_method (ticker, amount, price, date)
    #     # VALUES(%s, %s, %s, %s)
    #     # """

    #     # insertions = [
    #     #     ("AMC", 45, 18.36, "2022-08-16 13:23:44", 140533.69),
    #     #     ("GME", 13, 41.89, "2022-08-17 09:33:15", 93532.01),
    #     #     ("BBBY", 7, 32.54, "2022-08-17 15:45:21", 1543765.72)
    #     # ]

    #     select_query = "SELECT * FROM reddit_method"
    #     with connection.cursor() as cursor:
    #         # cursor.executemany(insert_query, insertions)
    #         cursor.execute(select_query)
    #         result = cursor.fetchall() # gonna wanna get that date time from the orders to then inser into here
    #         for row in result: # along with all other info
    #             print(row) # queries used were above, you can make a list of tuples and send it over to execute
    #         # connection.commit()

    #         # make test for db function and other function
    #         # have this function require name of table (such as reddit_method so query can use it like
    #         # INSERT INTO {table}) as well as the array of tuples to put the data in




