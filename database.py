from peewee import PostgresqlDatabase

db = PostgresqlDatabase(
    'smartticket',
    user='postgres',
    password = '',
    host='localhost',
    port =5432
)


