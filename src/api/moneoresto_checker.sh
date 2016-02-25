#!/bin/sh
cd "/var/www/moneoresto_checker"
exec python server.py > moneoresto_checker.log 2>&1
