export FLASK_APP="app.py"

if [[ "$MODE" == "DEBUG" ]];
then
  export FLASK_ENV="development"

  # TODO: wait on quit?
#  firefox --new-window http://127.0.0.1:5000/
else
  echo "RELEASE setup TODO"
fi

flask run
