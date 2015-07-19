setup: deps db

deps:
	@pip install -r requirements.txt

sandbox_run:
	@env PYTHONPATH=sandbox:.:$$PYTHONPATH python sandbox/manage.py runserver

sandbox_shell:
	@env PYTHONPATH=sandbox:.:$$PYTHONPATH python sandbox/manage.py shell

pyvows:
	@env PYTHONPATH=sandbox:.:$$PYTHONPATH pyvows -c -l django_pyvows --profile-threshold 95 vows/

ci_test: db
	@env PYTHONPATH=sandbox:.:$$PYTHONPATH pyvows -c -l django_pyvows --profile-threshold 95 -r django_pyvows.coverage.xml vows/

db:
	@env PYTHONPATH=$$PYTHONPATH:. python sandbox/manage.py syncdb --noinput
