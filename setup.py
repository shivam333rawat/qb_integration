from setuptools import setup, find_packages

setup(
    name='qb_integration',
    version='0.0.1',
    description='Integration with QueueBuster POS',
    author='shivam333rawat',
    author_email='you@example.com',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['frappe'],
)
