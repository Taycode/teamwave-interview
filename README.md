# teamwave-interview
an interview project for teamwave


Firstly, clone the repo

```
git clone https://github.com/Taycode/teamwave-interview.git
```

goto the project directory

```
cd ./teamwave-interview
```

create a virtual environment for the project 

```
python3 -m venv env
```

activate the virtual environment

For windows:

```
cd ./env/scripts && activate && {project directory}
```

for Linux:

```
source env/bin/activate
```

then install all the necessary dependencies

```
pip install -r requirements.txt
```

then make sure you have memcached server running

firstly, you install memcached

For Ubuntu:
```
$ sudo apt-get update
$ sudo apt-get install memcached
```
then start the memcached server
```
$ sudo systemctl start memcached
```
to confirm that memcached is running

```
$ sudo systemctl status memcached
```
then run the Django server:
```
python manage.py migrate && python manage.py runserver
```


now open your browser and visit http://localhost:8000/
