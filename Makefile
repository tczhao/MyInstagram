init-local:  ## create local python virtualenv and install packages for local dev
	pip3 install pipenv 
	# sudo -H pip3 install -U pipenv
	# sudo apt install pipenv
	pipenv --python 3.7.7
	pipenv install

init-django:
	django-admin startproject MyInstagram .

shell:
	pipenv shell

run:
	python manage.py runserver