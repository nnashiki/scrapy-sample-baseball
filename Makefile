DB=baseball_db

initdb:
	- docker stop ${DB}
	docker run --rm --name ${DB} -e MYSQL_ROOT_PASSWORD=baseball_pass -e MYSQL_USER=baseball_user -e MYSQL_PASSWORD=baseball_pass -e MYSQL_DATABASE=${DB} -d -v `pwd`/mysql/db_init:/docker-entrypoint-initdb.d -v `pwd`/mysql/cnf:/etc/mysql/conf.d -p 3306:3306 mysql:5.7

build:
	docker build -t scrapy:0.1 -f `pwd`/baseball/Dockerfile .

crawl: build
	docker run -it --rm --name scrapy --link baseball_db:baseball_db scrapy:0.1 bash

upjupyter:
	docker build -t jupyter-japanese:0.1  -f `pwd`/jupyter/Dockerfile .
	docker run -it --rm --name notebook -p 8888:8888 jupyter-japanese:0.1
