from setuptools import setup

setup(
    name='readiness_probe_test',
    install_requires=[
        'fastapi==0.88.0',
        'feedparser==6.0.10',
        'uvicorn==0.20.0',
        'pydantic==1.10.2',
        'requests==2.28.1',
        'python-statemachine==0.9.0'
    ],
    python_requires=">=3.10"
)
