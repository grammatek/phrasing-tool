from setuptools import setup, find_packages

setup(
	name='phrasing-tool',
	version='0.1.0',
	description='A phrasing tool that inserts pause tags into text based on phrases',
	author='Helga Svala Sigurðardóttir',
	author_email='helgas@ru.is',
	url='https://github.com/grammatek/text-cleaner',
	packages=find_packages(),
	install_requires=[
		'setuptools',
	],
	python_requires='>=3.5',
	entry_points={
			'console_scripts': [
				'phrasing=phrasing.phrasing:main'
							]
				}
	)

