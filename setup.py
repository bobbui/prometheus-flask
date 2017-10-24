from setuptools import setup



setup(
    name='Flask-Prometheus',
    version='0.0.1',
    packages=['flask_prometheus'],
    platforms='any',
    install_requires=[
        'Flask>=0.10',
        'prometheus-client>=0.0.14'
    ]
)
