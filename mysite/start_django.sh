#!/bin/bash
source /home/yuchen/myprojectenv/bin/activate
exec python3 /home/yuchen/Django_database/mysite/manage.py runserver 0.0.0.0:8000
