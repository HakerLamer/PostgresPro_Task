import paramiko #pip install paramiko
import psycopg2 #pip install psycopg2
import time # Импорт модуля time для расчета времени выполнения команды 
import os # Импорт модуля os для переменных окружения
from dotenv import load_dotenv, dotenv_values #pip install python-dotenv
# загрузка значений из .env файла
load_dotenv()

def run_psql(ssh_client):
    # Вызываем psql и отправляем команду
    child = ssh_client.invoke_shell()
    child.send(list_commands[7]+"\n")
    child.send(password+"\n")  # Пароль для sudo
    time.sleep(4)  # Даем время для завершения команды su - postgres
    # Теперь запускаем psql
    child.send(list_commands[8]+"\n")
    time.sleep(4)  # Даем время для запуска psql
    # Отправляем команду в psql
    child.send(list_commands[9]+"\n")
    time.sleep(4)  # Даем время для выполнения команды
    # Читаем вывод
    output = ''
    while True:
        if child.recv_ready():
            chunk = child.recv(1024).decode()
            #print(chunk, end='')  # выводим вывод по мере его поступления
            output += chunk
            if "postgres=#" in output:  # проверяем, появилась ли приглашение psql в выводе
                break

    return output


def replace_part_of_text(array, old_part, new_part):
    for i in range(len(array)):
        array[i] = array[i].replace(old_part, new_part)
    return array

try:
    ip=os.getenv("IP")
    us=os.getenv("USER_COMP")
    password=os.getenv("PASS_COMP")
    # Создаем клиент SSH
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # Загружаем SSH-ключ (Для Windows)
    private_key = paramiko.RSAKey.from_private_key_file("C:\\Users\\egors\\.ssh\\id_rsa")
    # Загружаем SSH-ключ (Для Mac OS и других Unix систем)
    #private_key = paramiko.RSAKey.from_private_key_file("/Users/egors/.ssh/id_rsa")
    # Подключаемся к удаленному устройству
    client.connect(ip, username=us, pkey=private_key)
    print(f"Подключение успешно установлено: {client.get_transport().is_active()}")
    i=0
    list_commands = [
        "sudo -S apt-get update",
        # Обновление локальных репозиториев
        "sudo -S apt-get install -y postgresql",
        # Установка 
        "echo $(psql --version | awk '{print $3}' | awk -F'.' '{print $1}')",
        # Выбор версии PostgreSQL
        "sudo -S echo \"listen_addresses = \'*\'\" | sudo tee -a /etc/postgresql/VER/main/postgresql.conf",
        # Изменение конфигурации pg_hba.conf
        "sudo -S echo \"host    all             all             0.0.0.0/0               md5\" | sudo tee -a /etc/postgresql/VER/main/pg_hba.conf",
        #Автозапуск PostgreSQL при загрузке системы
        "sudo -S systemctl enable postgresql",
        # Перезапуск PostgreSQL
        "sudo -S systemctl restart postgresql",
        # Вход под юзера postgres
        "sudo -S su - postgres",
        # Запуск Псевдотерминала psql
        "psql",
        # Sql-скрипт на проверку о наличии обратной связи БД
        "SELECT 1;"]
        # Запуск Псевдотерминала psql
    while i<len(list_commands)-3:
        # Выполняем команду на удаленном устройстве
        print(i+1, "- команда")
        print(list_commands[i]) 
        #if exec_command=='exit': 
        #    client.close()
        #    break
        start_time = time.time()
        stdin, stdout, stderr = client.exec_command(list_commands[i])
        if(i==2): 
            ver=stdout.channel.recv(1024).decode().strip()
            replace_part_of_text(list_commands,"VER",ver)
            # Передаем пароль в stdin для sudo команд
        if list_commands[i].startswith("sudo -S"):
            stdin, stdout, stderr = client.exec_command(list_commands[i], get_pty=True)
            stdin.write(password+"\n") #Пароль для sudo 
            stdin.flush()
        # Читаем и печатаем вывод из stdout и stderr до тех пор, пока каналы не закроются
        while not stdout.channel.exit_status_ready() or not stderr.channel.exit_status_ready():
            # Читаем и печатаем вывод из stdout
            if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode().strip())
            # Читаем и печатаем ошибки из stderr
            if stderr.channel.recv_stderr_ready():
                print(stderr.channel.recv_stderr(1024).decode().strip())
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Время выполнения: {elapsed_time} секунд")
        i+=1
    output = run_psql(client)
    print(output)
except Exception as e:
    print(str(e))

