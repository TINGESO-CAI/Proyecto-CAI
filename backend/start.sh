#!/bin/sh
cd backend
flask db upgrade
flask run --host=0.0.0.0