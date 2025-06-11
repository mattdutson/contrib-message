# contrib-message

Write a message in the GitHub contribution graph

## Setup

Create a Python virtual environment:
```
python -m venv venv
```
Then activate the environment:
```
source venv/bin/activate
```
Install dependencies:
```
pip install -r requirements.txt
```

## Usage

To see script options:
```
./contrib_message.py --help
```

Example usage:
```
./contrib_message.py '<HI MOM' '<HAPPY' ' BDAY'
```

Use `-d` to see the rendered text without creating commits.

Commits are added to the repository for the working directory.

## Font License

The BPdotsUnicaseSquare font is subject to a [CC BY-ND 3.0 license](https://creativecommons.org/licenses/by-nd/3.0/).
