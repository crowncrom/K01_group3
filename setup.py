from setuptools import setup, find_packages

setup(
    name="smart_trash_can",
    version='2.1',
    author='K01_Group03',
    url='https://github.com/crowncrom/K01_group3',
    packages=find_packages(where='.'),
    package_dir={'smart_trash_can':'smart_trash_can','servo':'servo','usb_camera':'usb_camera','prediction':'prediction'},
    entry_points="""
      [console_scripts]
      smart_trash_can = smart_trash_can.cli:execute
    """,
    install_requires=open('requirements.txt').read().splitlines(),
)
