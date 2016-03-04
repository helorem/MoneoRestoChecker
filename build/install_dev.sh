#!/bin/sh

rm -f /etc/init.d/moneoresto-checker
ln -s /mnt/src/conf/moneoresto-checker.service /etc/systemd/system/moneoresto-checker.service

rm -f /usr/bin/moneoresto-checker.sh
ln -s /mnt/src/src/api/moneoresto-checker.sh /usr/bin/moneoresto-checker.sh

rm -rf /var/www/moneoresto-checker
ln -s /mnt/src/src /var/www/moneoresto-checker

rm -f /etc/nginx/sites-available/moneoresto-checker
ln -s /mnt/src/conf/nginx_default.conf /etc/nginx/sites-available/moneoresto-checker
ln -s /etc/nginx/sites-available/moneoresto-checker /etc/nginx/sites-enabled/moneoresto-checker

rm -f /var/www/moneoresto-checker/api/moneoresto-checker.db
sqlite3 /var/www/moneoresto-checker/api/moneoresto-checker.db < /var/www/moneoresto-checker/api/moneoresto-checker.sql
chown www-data:www-data /var/www/moneoresto-checker/api/moneoresto-checker.db
touch /var/log/moneoresto-checker.log
chown www-data:www-data /var/log/moneoresto-checker.log
mv /var/log/moneoresto-checker.log /var/www/moneoresto-checker/api/moneoresto-checker.log
ln -s /var/www/moneoresto-checker/api/moneoresto-checker.log /var/log/moneoresto-checker.log
