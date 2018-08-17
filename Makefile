DB=baseball_db

initdb:
	- docker stop ${DB}
	docker run --rm --name ${DB} -e MYSQL_ROOT_PASSWORD=baseball_pass -e MYSQL_USER=baseball_user -e MYSQL_PASSWORD=baseball_pass -e MYSQL_DATABASE=${DB} -d -v `pwd`/db_init:/docker-entrypoint-initdb.d -v `pwd`/mysql:/etc/mysql/conf.d -p 3306:3306 mysql:5.7
