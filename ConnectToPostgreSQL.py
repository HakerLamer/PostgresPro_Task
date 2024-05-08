import psycopg2 #pip install paramiko
print("Login:")
log=input()
print("Password:")
pas=input()
print("Database Name:")
dbname=input()
print("host-ip of Database:")
ip=input()
print("port:")
ip=input()
try:
        connection = psycopg2.connect(
            dbname=dbname,
            user=log,
            password=pas,
            host=ip,
            port=port
        )
        print("Успешное подключение к PostgreSQL")
except Exception as e:
        print("Ошибка при подключении к PostgreSQL:", e)