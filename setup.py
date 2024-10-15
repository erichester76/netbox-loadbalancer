from setuptools import find_packages, setup

setup(
    name='netbox-loadbalancer',
    version='1.0.0',
    description = 'LoadBalancing Management with Netbox',
    author='HuyTM',
    license='Apache 2.0',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    package_data={
        'netbox_loadbalancer': ['templates/**'],
    },
    entry_points={
        'netbox_plugins': [
            'netbox_loadbalancer = netbox_loadbalancer:Plugin',
        ],
    },
)
