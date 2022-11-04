from mysql.connector import connect
from src.config import db_password

class db:
    '''
    This class contains method regularly used by me to create
    tables in a db that are used by the trading methods to save
    what trades were made and when they were made.
    '''
    def __init__(self, table): # Creates a connection to a local database called "Purchase History" (must be premade in MYSQL)
        self.table = table
        self.cnx = connect(
            host="localhost",
            port=3306,
            user="root",
            password=db_password,
            database="purchase_history")
        self.cursor = self.cnx.cursor(buffered=True)
    
    def table_inserter(self, insertions): # insert table into database
        insert_query = f"""
        INSERT INTO {self.table} (ticker, status, amount, price, date, account_value)
        VALUES(%s, %s, %s, %s, %s, %s)
        """
        self.cursor.executemany(insert_query, insertions)
        self.cnx.commit()
             
    def table_creator(self): # creates SQL table
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
        self.cursor.execute(create_table_query)
        self.cursor.execute(show_table_query)
        result = self.cursor.fetchall()
        self.cnx.commit()
        return result
    
    def table_contents(self): # Retrieves Contents from a table
        select_query = f"SELECT * FROM {self.table}"
        self.cursor.execute(select_query)
        result = self.cursor.fetchall() # gonna wanna get that date time from the orders to then inser into here
        fresult = [str(row) for row in result]
        return fresult

    
# uncomment to make tables here
# db_thing = db("reddit_method") # table name
# db_thing.table_creator() # Create Table