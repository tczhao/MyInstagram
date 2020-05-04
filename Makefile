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

create-app:
	python manage.py startapp $(app)

makemigrations: # traverse models.py in app to calculate the difference to the latest migration and generate the migration to database
	python manage.py makemigrations

migrate: # apply all migration that hasn't been applied to the database
	python manage.py migrate

createsuperser: # to view content management system
	python manage.py createsuperuser

run:
	python manage.py runserver