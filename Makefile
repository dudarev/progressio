test:
	cd tests && nosetests -s

update_version:
	python setup.py update_version

pip_update:
	sudo pip uninstall progress && sudo pip install .
