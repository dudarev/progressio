.PHONY: test_unit  test pip_update upload \
    register

# working on now
test_now:
	cd tests/unit && nosetests test_load.py:TestLoad.test_parse_item -s

test_unit:
	cd tests/unit && nosetests -s

test_functional:
	cd tests/functional && nosetests -s

test: test_unit test_functional

# updates README.md from README.md.in
readme:
	python setup.py update_readme

pip_update:
	sudo pip uninstall progressio && sudo pip install .

upload:
	python setup.py sdist
	python setup.py sdist upload

register:
	python setup.py register

tags:
	ctags -R .
