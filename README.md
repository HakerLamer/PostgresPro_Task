# Инструкция по подключению к удаленному хосту

Перед запуском программы необходимо написать свой путь до файла с **открытым ключом** для подключения по SSH к удалённому хосту. 
> По умолчанию путь прописан в формате для Windows.
> В зависимости от операционной системы, необходимо использовать **один из вариантов формата пути**, а другой стереть.  

Пример написания пути до файла:
![Варианты выбора написания пути](https://github.com/HakerLamer/PostgresPro_Task/blob/main/example_2.jpg?raw=true)

Данный код имеет набор команд, который от предназначен для установки PostgreSql на удаленном хосте, на котором установлена операционная система **Ubuntu 22.04**

Также, необходимо убедиться в корректности подключения по SSH, иначе после ввода данных для подключения появится следующая ошибка:

![Ошибка подключения по SSH](https://github.com/HakerLamer/PostgresPro_Task/blob/main/example_3.jpg?raw=true)

# Запуск программы

Для того, чтобы запустить код **по установке PostgreSql**, необходимо в директории, где находится файл, запустить следующую команду:

`py ControlPostgre.py`

В консоли команда выглядит следующим образом:
![Пример запуска](https://github.com/HakerLamer/PostgresPro_Task/blob/main/example_1.jpg?raw=true)

Далее необходимо ввести данные по подключению к хосту:
* ip адрес хоста
* имя пользователя хоста
* пароль пользователя

На моём примере были использованы следующие данные:
* ip адрес хоста: `192.168.80.131`
* имя пользователя хоста: `tomt`
* пароль пользователя: `1306`

В случае удачного подключения, появится строка об успешном подключении:

![Пример успешного подключения](https://github.com/HakerLamer/PostgresPro_Task/blob/main/example_4.jpg?raw=true)

Далее поэтапно будут запускаться команды с их порядковым номером, выводом терминала о запуске команды и временем выполнения.

Пример:
![Пример выполнения](https://github.com/HakerLamer/PostgresPro_Task/blob/main/example_5.jpg?raw=true)

При установке базы данных на удаленный хост, выводится результат:

`postgres@tomt-virtual-machine:~$ psql`
`psql (14.11 (Ubuntu 14.11-0ubuntu0.22.04.1))`
`Type "help" for help.`

`postgres=# SELECT 1;`
 `?column?`
`----------`
`        1`
`(1 row)`

`postgres=#`

# Дополнительно

Для того, чтобы запустить проверку на **подключение к PostgreSql**, необходимо в директории, где находится файл запустить следующую команду:

`py ConnectToPostgreSQL.py`

> Нужно учитывать, что устанавливается чистый PostgreSql, для проверки необходимо создать в базе данных пользователя с паролем

Пример исполнения кода:
![enter image description here](https://github.com/HakerLamer/PostgresPro_Task/blob/main/example_6.jpg?raw=true)

# Ошибки, с которыми я повстречался и их решением

**Как корректно удалить PostgreSql из Linux?**
> Основной вариант, как можно удалить все зависимости и все, что связано с PostgreSql
> sudo apt-get --purge remove postgresql\* && sudo apt-get autoremove

> Или можно попробовать выбрано отобрать и удалить пакеты по очередно
Остановка службы PostgreSQL, если она запущена 

`sudo systemctl stop postgresql`

Отключение/включение автозапуска службы PostgreSQL при загрузке

`sudo systemctl disable/enable postgresql`

Удаление всех файлов данных PostgreSQL

`sudo rm -r /var/lib/postgresql/`

Удаление пользователя postgres и его домашнего каталога

`sudo userdel -r postgres`

Удаление всех файлов конфигурации PostgreSQL

`sudo rm -r /etc/postgresql/`

Удаление всех файлов журналов PostgreSQL

`sudo rm -r /var/log/postgresql/`

Удаление всех файлов документации PostgreSQL

`sudo rm -r /usr/share/doc/postgresql/`

Удаление всех файлов дампов баз данных PostgreSQL

`sudo rm -r /var/lib/postgresql/backups/`

Удаление всех оставшихся файлов конфигурации PostgreSQL из каталога /etc/

`sudo apt-get autoremove --purge`

Наконец, удаление всех файлов, связанных с PostgreSQL из каталога /var/lib/postgresql/

`sudo rm -rf /var/lib/postgresql/`

**Повстречался с проблемой, связанной в погружение из одного терминала в другой/псевдотерминал**
А именно на таком примере:

`tomt@tomt-virtual-machine:~$ sudo -S su - postgres`
`[sudo] password for tomt:`
`postgres@tomt-virtual-machine:~$ psql`

Решил её путем invok'a из оболочки и прописывая с задержкой команды в несколько секунд, чтобы не застрять в каком либо псевдоконсоли.

Вот функция:



