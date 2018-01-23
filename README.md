# CashFlows

This repo aims to provide utility functions for cashflow analysis using **python 3.6**. 

## CashFlow analysis in action

Check out the file **examples.ipynb** in order to see usage examples. 

## Usage

1. Download this repo with `git clone https://github.com/rhdzmota/cashflows.git`.
1. Create a virtual-environment and install requirements.
    * `virtualenv --python=python3 venv`
    * `source venv/bin/activate`
    * `pip install -r requirements.txt`
1. Run the tests to guarantee usability (see **Tests** section).
1. Install locally. Go to the base directory and run:
    `pip install -e .`.

## Tests

There are two ways of running tests.
Make sure to have **nose** installed.

#### Nose installation 

There are two ways of installing nose:

* Install the linux package: `sudo apt install python3-nose`
* Install via pip: `pip install nose`
In the base directory run the following:

#### Run the tests

Go to the base directory and run the following: 

* Using the linux package: `nosetests3`
* Using python: `python setup.py test`


## Contributions and authors
Contact the main developer for contributions.

* **Main developer**: Rodrigo Hernández Mota (rohdzmota@gmail.com)
* **Developer**: Jose Luis Vazquez (--)

## License

See the LICENSE.md file. 
