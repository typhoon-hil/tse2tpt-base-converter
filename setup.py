from setuptools import setup, find_packages

setup(
    name='tse_to_third_party_tools_converter',
    version='1.0',
    packages=find_packages(),
    install_requires=["typhoon-hil-api"],
    url='https://www.typhoon-hil.com/',
    include_package_data=True,
    license='MIT',
    author='Marcos Moccelini',
    author_email=f'marcos.moccelini@typhoon-hil.com',
    description='Typhoon HIL Schematic Editor to third-party tools converter'
)
