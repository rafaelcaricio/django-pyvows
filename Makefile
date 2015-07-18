setup: deps db

deps:
	@pip install -r requirements.txt

sandbox_shell:
	@env PYTHONPATH=$$PYTHONPATH:vows/sandbox/:. python vows/sandbox/manage.py shell

pyvows:
	@env PYTHONPATH=$$PYTHONPATH:vows/sandbox/:. pyvows -c -l django_pyvows --profile-threshold 95 vows/

ci_test:
	@env PYTHONPATH=$$PYTHONPATH:vows/sandbox/:. python vows/sandbox/manage.py syncdb && pyvows --no_color --cover --cover_package=django_pyvows --cover_threshold=100 -r django_pyvows.coverage.xml -x vows/

db:
	@env PYTHONPATH=$$PYTHONPATH:. python vows/sandbox/manage.py syncdb
