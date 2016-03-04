#!/bin/sh

PATTERN="#GENERATED moneoresto-checker"

mkdir -p bin

# Prepare addon
ip="$(docker inspect --format '{{ .NetworkSettings.IPAddress }}' moneoresto-checker)"
cp build/nginx_host.conf bin/nginx_host.conf
sed -i "s/@IP@/$ip/g" bin/nginx_host.conf

# Remore old addon
cp /etc/nginx/sites-available/default bin/default
sed -i "/ $PATTERN/d" bin/default
sudo rm /etc/nginx/conf.d/moneoresto-checker

# Apply
sed -i "s@location / {@location / {\ninclude conf.d/moneoresto-checker; $PATTERN@g" bin/default

# Move
sudo mv bin/nginx_host.conf /etc/nginx/conf.d/moneoresto-checker
sudo mv bin/default /etc/nginx/sites-available/default

# Restart nginx
sudo service nginx reload

