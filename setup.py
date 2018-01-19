from setuptools import find_packages, setup

setup(name='async_binace',
      version='0.0.1',
      url = "https://github.com/znypah777/async_binance",
      packages=find_packages(exclude=[".docs/", ".venv/"]),
      install_requires=["aiohttp==2.3.7",
                        "async-timeout==2.0.0",
                        "chardet==3.0.4",
                        "idna==2.6",
                        "multidict==4.0.0",
                        "yarl==0.18.0"],
      description='async Python bindings for binance API.',
      author='Halcyon Ramirez',
      author_email='znypah777@gmail.com',
      classifiers=[
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.6',
          'Operating System :: OS Independent',
          'Topic :: Office/Business :: Financial',
      ])