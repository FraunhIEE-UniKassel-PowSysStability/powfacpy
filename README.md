# powfacpy

[![PyPI](https://img.shields.io/pypi/v/powfacpy)](https://pypi.org/project/powfacpy/)
[![Python versions](https://img.shields.io/pypi/pyversions/powfacpy)](https://pypi.org/project/powfacpy/)
[![License](https://img.shields.io/pypi/l/powfacpy)](LICENSE)

This package is a wrapper around the Python API of PowerFactory (power system simulation software by DIgSILENT) with improved syntax and functionality compared to the native API. Please have a look at the [documentation](https://fraunhiee-unikassel-powsysstability.github.io/powfacpy/docs/) for further information.

*PowerFactory* and *DIgSILENT* are trademarks of DIgSILENT GmbH. *powfacpy* is an independent, community-maintained open source project and is not affiliated with, endorsed by, or sponsored by DIgSILENT GmbH. Using *powfacpy* requires your own valid PowerFactory license and installation.


## Installation
```
pip install powfacpy
```
Some features rely on optional dependencies (e.g. `pip install powfacpy[dynamic_modal_analysis]`) - see the [installation section](https://fraunhiee-unikassel-powsysstability.github.io/powfacpy/docs/index.html#installation) of the docs for the full list of extras, or `pip install powfacpy[all]` for everything.

Requires Python >= 3.11 and your own PowerFactory installation and license.


## Why use *powfacpy*?
There are a number of reasons why you should consider using *powfacpy*:
- Increase productivity 
- Write more readable code
- Avoid running into similar problems, errors and obscurities as other users of the python interface of *PowerFactory* before you
- Having a standard way of doing things in your organization (e.g. a standard format for simulation result export) 
- Steep learning curve for *PowerFactory* beginners (helpful tutorials)


## Contact
This package is under active development and mainly maintained by *Fraunhofer IEE*. You are welcome to contribute, open issues or get in touch (simon.eberlein@iee.fraunhofer.de). 
