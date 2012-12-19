test:
	cd tests && nosetests -s

# updates README from README.in
update_readme:
	python setup.py update_readme

pip_update:
	sudo pip uninstall progress && sudo pip install .
