test:
	cd tests && nosetests -s

# updates README.md from README.md.in
update_readme:
	python setup.py update_readme

pip_update:
	sudo pip uninstall progressio && sudo pip install .

upload:
	python setup.py sdist
	python setup.py sdist upload

register:
	python setup.py register

ctags:
	ctags -R .
