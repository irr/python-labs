try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

config = {
	'description': 'My Test Project',
	'author': 'author',
	'url': 'http://www.testproject.org/',
	'download_url': 'http://testproject.org/testpkg/testpkg-0.1.tar.gz',
	'author_email': 'author@email',
	'version': '0.1',
	'install_requires': [],
	'packages': ['testpkg'],
	'scripts': [],
	'name': 'testpkg'
}

setup(**config)
