# CashFlows

This repo aims to provide utility functions for cashflow analysis using **python 3.6**. 

## CashFlow analysis in action

Check out the file **examples.ipynb** in order to see usage examples. 

## Usage

1. Download this repo with `git clone`.
2. Run the tests to guarantee usability.
3. Install locally. Go to the base directory and run:
    `pip install -e .`.

## Tests

There are two ways of running tests.
Make sure to have **nose** installed.

#### Linux package 
In the base directory run the following:

```bash
sudo apt install python3-nose
nosetests3
```

#### Python package
Use the virtualenv with the required packages.

```bash
virtualenv venv
source venv/bin/activate
pip install -r requirements
python setup.py test
```

Or via pip.

```bash
pip install nose
python setup.py test
```

## Contribute
Contact the main developer.

* **Main developer**: Rodrigo Hernández Mota (rohdzmota@gmail.com)

## License

See the LICENSE.md file. 

