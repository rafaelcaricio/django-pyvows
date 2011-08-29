pyvows:
	@env PYTHONPATH=$$PYTHONPATH:vows/sandbox/:. pyvows --cover --cover_package=django_pyvows --cover_threshold=95 vows/

ci_test:
	@env PYTHONPATH=$$PYTHONPATH:vows/sandbox/:. python vows/sandbox/manage.py syncdb && pyvows --cover --cover_package=django_pyvows --cover_threshold=100 -r django_pyvows.coverage.xml -x vows/

db:
	@env PYTHONPATH=$$PYTHONPATH:. mysql -u root -e 'DROP DATABASE IF EXISTS django_pyvows' && mysql -u root -e 'CREATE DATABASE IF NOT EXISTS django_pyvows' && python vows/sandbox/manage.py syncdb
