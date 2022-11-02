# run pytest .\tests\db_tests.py
from src.db_intializer import db

def test_table_creator(): # check if able to connect to db and create tables
    db_thing = db("test")
    assert db_thing.table_creator() == [
        ('id', b'int', 'NO', 'PRI', None, 'auto_increment'), 
        ('ticker', b'varchar(5)', 'YES', '', None, ''), 
        ('status', b'varchar(4)', 'YES', '', None, ''),
        ('amount', b'int', 'YES', '', None, ''), 
        ('price', b'decimal(9,2)', 'YES', '', None, ''), 
        ('date', b'datetime', 'YES', '', None, ''), 
        ('account_value', b'decimal(9,2)', 'YES', '', None, '')
    ]

def test_table_inserter(): # check if able to insert data into tables
    db_thing = db("test")
    insertions = [
        ("AMC", "BUY", 45, 18.36, "2022-08-16 13:23:44", 140533.69),
        ("GME", "SELL", 13, 41.89, "2022-08-17 09:33:15", 93532.01),
        ("BBBY", "BUY", 7, 32.54, "2022-08-17 15:45:21", 1543765.72)
    ]
    db_thing.table_inserter(insertions)
    assert db_thing.table_contents() == [
        "(1, 'AMC', 'BUY', 45, Decimal('18.36'), datetime.datetime(2022, 8, 16, 13, 23, 44), Decimal('140533.69'))", 
        "(2, 'GME', 'SELL', 13, Decimal('41.89'), datetime.datetime(2022, 8, 17, 9, 33, 15), Decimal('93532.01'))", 
        "(3, 'BBBY', 'BUY', 7, Decimal('32.54'), datetime.datetime(2022, 8, 17, 15, 45, 21), Decimal('1543765.72'))"
        ]

