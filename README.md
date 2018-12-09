# Botchevik
Discord bot tailored for the Git Gud Discord server.

## Requirement
- Python 3.5.3+

## Installation

1. Rename `secrets_example.py` to `secrets.py`
2. Set the `TOKEN` variable with the token of your Discord bot
3. Install the requirement :
````bash
pip install -r requirements.txt
````
4. Populate the database (Example on debian) :
````bash
sqlite3 botchevik.db < database.sql
````
5. (Linux) Maybe you will have to install the opus module :
````bash
apt-get install libopus0
````
6. Launch the main script :
````bash
python main.py
```` 

## Licence

GNU General Public License v3.0