basic organization tools repo for myself

currently just has a trello/style task tracking system with columns/cards.

## requirements: 
- postgres installation on the host machine or elsewhere,
- database provisioned within postgres
- config file `config.json` of the format:
  ```json
    {"DB_USER": "<Postgres username>", "DB_NAME": "<Postgres database name>"}
  ```
- python 3.6+ (relies on dict ordering and other features in 3.6)
- python package requirements in requirements.txt installed via `pip install -r requirements.txt`
