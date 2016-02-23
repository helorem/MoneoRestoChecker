PWD:=$(shell pwd)

deb: clean
	mkdir -p bin/moneoresto_checker
	cp -r build/DEBIAN bin/moneoresto_checker/DEBIAN
	mkdir -p bin/moneoresto_checker/etc/init.d/
	cp conf/moneoresto_checker.service bin/moneoresto_checker/etc/init.d/moneoresto_checker
	mkdir -p bin/moneoresto_checker/etc/nginx/sites-available/
	cp conf/nginx_default.conf bin/moneoresto_checker/etc/nginx/sites-available/moneoresto_checker
	mkdir -p bin/moneoresto_checker/var/www/moneoresto_checker/
	cp -r src/* bin/moneoresto_checker/var/www/moneoresto_checker/
	mkdir -p bin/moneoresto_checker/usr/bin/
	mv bin/moneoresto_checker/var/www/moneoresto_checker/api/moneoresto_checker.sh bin/moneoresto_checker/usr/bin/
	dpkg-deb --build bin/moneoresto_checker bin/moneoresto_checker.deb

clean:
	rm -rf bin

deploy: deb
	cp build/Dockerfile.deploy bin/Dockerfile
	docker build -t moneoresto_checker bin

run:
	docker stop moneoresto_checker | exit 0
	docker rm moneoresto_checker | exit 0
	docker run -dit --name=moneoresto_checker --expose=80 moneoresto_checker
	docker exec -ti moneoresto_checker service moneoresto_checker start
	docker exec -ti moneoresto_checker service nginx start

deploy-dev:
	cp build/Dockerfile.dev bin/Dockerfile
	docker build -t moneoresto_checker bin

run-dev:
	docker stop moneoresto_checker | exit 0
	docker rm moneoresto_checker | exit 0
	docker run -dit --name=moneoresto_checker -v "$(PWD)":"/mnt/src" --expose=80 moneoresto_checker
	docker exec -ti moneoresto_checker /mnt/src/build/install_dev.sh
	docker exec -ti moneoresto_checker service moneoresto_checker start
	docker exec -ti moneoresto_checker service nginx start

exec:
	docker exec -ti moneoresto_checker bash -l

install_nginx:
	build/install_nginx.sh

deploy-all: deploy run install_nginx

deploy-dev-all: deploy-dev run-dev install_nginx

