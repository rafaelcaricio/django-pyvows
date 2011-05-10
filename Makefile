pyvows:
	@env PYTHONPATH=$$PYTHONPATH:. pyvows --cover --cover_package=django_pyvows --cover_threshold=100 vows/
