from setuptools import setup, find_packages
import subprocess

# Set the version according to GitHub Releases
p = subprocess.Popen(["git", "describe", "--always", "--tag"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, errors = p.communicate()
if not errors:
    __version__ = output.strip()
    # When your tag is pre-release, the tag number isn't just 0.0.0 so, this.
    __version__ = __version__.split('-')[0]
else:
    __version__ = '0.0.0'

setup(
    name='nsq2kafka',
    version=__version__,
    description="Reads from NSQ, Publishes to Kafka",
    long_description=open('README.md').read(),
    keywords=['NSQ', 'Kafka'],
    author='Russ Bradberry',
    author_email='rbradberry@simplereach.com',
    url='https://github.com/simplereach/nsq2kafka',
    license='Apache License 2.0',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "pynsq==0.7.0",
        "kafka-python==1.2.5"
    ],
    entry_points={
        'console_scripts': ['nsq2kafka = nsq2kafka.__main__:main']
    },
)
