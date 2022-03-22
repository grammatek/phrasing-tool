from setuptools import setup, find_packages

setup(
	name='phrasing-tool',
	version='0.1.0',
	description='A tool for adding pauses to text based on phrases',
	author='Helga Svala Sigurðardóttir',
	author_email='helgas@ru.is',
	url='https://github.com/grammatek/phrasing-tool',
	packages=['phrasing'],
	install_requires=[
		'setuptools',
	],
	python_requires='>=3.5',

	)
