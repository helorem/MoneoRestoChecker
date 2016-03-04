PWD:=$(shell pwd)

deb: clean
	mkdir -p bin/moneoresto-checker
	cp -r build/DEBIAN bin/moneoresto-checker/DEBIAN
	mkdir -p bin/moneoresto-checker/etc/systemd/system/
	cp conf/moneoresto-checker.service bin/moneoresto-checker/etc/systemd/system/moneoresto-checker.service
	mkdir -p bin/moneoresto-checker/etc/nginx/sites-available/
	cp conf/nginx_default.conf bin/moneoresto-checker/etc/nginx/sites-available/moneoresto-checker
	mkdir -p bin/moneoresto-checker/var/www/moneoresto-checker/
	cp -r src/* bin/moneoresto-checker/var/www/moneoresto-checker/
	mkdir -p bin/moneoresto-checker/usr/bin/
	mv bin/moneoresto-checker/var/www/moneoresto-checker/api/moneoresto-checker.sh bin/moneoresto-checker/usr/bin/
	dpkg-deb --build bin/moneoresto-checker bin/moneoresto-checker.deb

clean:
	docker stop moneoresto-checker | exit 0
	docker rm moneoresto-checker | exit 0
	rm -rf bin
	rm -f src/api/moneoresto-checker.db
	rm -f src/api/moneoresto-checker.log

deploy: deb
	cp build/Dockerfile.deploy bin/Dockerfile
	docker build -t moneoresto-checker bin
	sleep 2 # let systemd start

run:
	docker stop moneoresto-checker | exit 0
	docker rm moneoresto-checker | exit 0
	docker run --privileged=true -v /sys/fs/cgroup:/sys/fs/cgroup:ro -dit --name=moneoresto-checker --expose=80 moneoresto-checker /lib/systemd/systemd systemd.unit=emergency.service
	docker exec -ti moneoresto-checker systemctl start moneoresto-checker
	docker exec -ti moneoresto-checker systemctl start nginx

deploy-dev:
	cp build/Dockerfile.dev bin/Dockerfile
	docker build -t moneoresto-checker bin

run-dev:
	docker stop moneoresto-checker | exit 0
	docker rm moneoresto-checker | exit 0
	docker run --privileged=true -v /sys/fs/cgroup:/sys/fs/cgroup:ro -dit --name=moneoresto-checker -v "$(PWD)":"/mnt/src" --expose=80 moneoresto-checker /lib/systemd/systemd systemd.unit=emergency.service
	docker exec -ti moneoresto-checker /mnt/src/build/install_dev.sh
	docker exec -ti moneoresto-checker systemctl start moneoresto-checker
	docker exec -ti moneoresto-checker systemctl start nginx

exec:
	docker exec -ti moneoresto-checker bash -l

install_nginx:
	build/install_nginx.sh

deploy-all: deploy run install_nginx

deploy-dev-all: deploy-dev run-dev install_nginx

