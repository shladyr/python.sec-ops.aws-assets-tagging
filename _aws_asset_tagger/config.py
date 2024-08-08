import os

TAG_SCHEMA = {'Environment': 'Production', 'Compliance': 'SOC-2'}
METADATA_TABLE_NAME = os.getenv('METADATA_TABLE_NAME')
HISTORY_TABLE_NAME = os.getenv('HISTORY_TABLE_NAME')
ACTIONS_TABLE_NAME = os.getenv('ACTIONS_TABLE_NAME')
