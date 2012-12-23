test:
	cd tests && nosetests -s

# updates README.md from README.md.in
update_readme:
	python setup.py update_readme

pip_update:
	sudo pip uninstall progress && sudo pip install .
