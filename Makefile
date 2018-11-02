DB=baseball_db

init-db:
	- docker stop ${DB}
	docker run --rm --name ${DB} -e MYSQL_ROOT_PASSWORD=baseball_pass -e MYSQL_USER=baseball_user -e MYSQL_PASSWORD=baseball_pass -e MYSQL_DATABASE=${DB} -d -v `pwd`/mysql/db_init:/docker-entrypoint-initdb.d -v `pwd`/mysql/cnf:/etc/mysql/conf.d -p 3306:3306 mysql:5.7

dump-db:
	mysqldump -u baseball_user -h 127.0.0.1 -p baseball_db > dump_test.sql

connect-db:
	mysql -u baseball_user -h 127.0.0.1 -p baseball_db

build: init-db
	docker build -t scrapy:0.1 -f `pwd`/baseball/Dockerfile .

crawl: build
	docker run -it --rm --name scrapy --link baseball_db:baseball_db -v `pwd`/baseball:/usr/src/app scrapy:0.1 bash

up-jupyter:
	docker build -t jupyter-japanese:0.1  -f `pwd`/jupyter/Dockerfile .
	docker run -it --rm --name notebook -p 8888:8888 --link baseball_db:baseball_db -v `pwd`/jupyter/notes:/home/jovyan/work jupyter-japanese:0.1
