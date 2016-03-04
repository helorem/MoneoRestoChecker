#!/bin/sh
cd "/var/www/moneoresto-checker/api"
exec python -B moneoresto-checker.py > /var/log/moneoresto-checker.log 2>&1
