# HOME

## Installation

Install python 3.6, other versions might work but are not tested. Python 2 will not work.

Install a virtual environment handler, I recommend [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/). Virtualenvwrapper is also used for start scripts, so using the base virtual env handling will result in you having to start things manually. The created virtual env should be named seals for start scripts to work.

```mkvirtualenv seals```

Install requirements from requirements.txt.

```pip install -r requirements.txt```

Set environment variables. This install script will insert environment variables into the file you supply. For different systems, different scripts are run on terminal startup, bash_profile for macOS and bashrc for others. You need to supply the file that you know will be sourced.

```python install.py <bashrc/bash_profile>```
