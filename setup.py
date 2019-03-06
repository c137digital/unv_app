from setuptools import setup, find_packages

setup(
    name='unv.app',
    version='0.1.3',
    description="""Core app package with settings manipulation""",
    url='http://github.com/c137digital/unv_app',
    author='Morty Space',
    author_email='morty.space@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=[
        'jsonschema==2.6.0',
        'Fabric3==1.14.post1',
        'unv.utils==0.1'
    ],
    zip_safe=True
)
