#!/bin/sh

rm -f /etc/init.d/moneoresto_checker
ln -s /mnt/src/conf/moneoresto_checker.service /etc/init.d/moneoresto_checker

rm -f /usr/bin/moneoresto_checker.sh
ln -s /mnt/src/src/api/moneoresto_checker.sh /usr/bin/moneoresto_checker.sh

rm -rf /var/www/moneoresto_checker
ln -s /mnt/src/src /var/www/moneoresto_checker

rm -f /etc/nginx/sites-available/moneoresto_checker
ln -s /mnt/src/conf/nginx_default.conf /etc/nginx/sites-available/moneoresto_checker
ln -s /etc/nginx/sites-available/moneoresto_checker /etc/nginx/sites-enabled/moneoresto_checker

sqlite3 /var/www/moneoresto_checker/api/moneoresto_checker.db < /var/www/moneoresto_checker/api/moneoresto_checker.sql
chown -R www-data:www-data /var/www/moneoresto_checker/api


