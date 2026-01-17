[ -f tags ] && rm tags

ctags -R --exclude=.venv --exclude=.git --exclude="__pycache__" --exclude="*.pyc" .
