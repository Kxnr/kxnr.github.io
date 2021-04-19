#! /bin/bash
source /home/kxnr/miniconda3/etc/profile.d/conda.sh
conda activate website

# TODO: setup configuration

if [[ "$MODE" == "DEBUG" ]];
then
  export FLASK_APP="app.py"
  export FLASK_ENV="development"
  flask run
else
  gunicorn --workers 1 --bind unix:gunicorn.sock app:app
fi
