pyvows:
	@env PYTHONPATH=$$PYTHONPATH:. pyvows --cover --cover_package=django_pyvows --cover_threshold=100 vows/

db:
	@env PYTHONPATH=$$PYTHONPATH:. mysql -u root -e 'DROP DATABASE IF EXISTS django_pyvows' && mysql -u root -e 'CREATE DATABASE IF NOT EXISTS django_pyvows' && python vows/sandbox/manage.py syncdb
