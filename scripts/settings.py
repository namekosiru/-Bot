import os
from os.path import join, dirname
from dotenv import load_dotenv
import dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

GAT = os.environ.get('ACCESS_TOKEN')
REPO_NAME = os.environ.get('REPO_NAME')

FILE_NAME = os.environ.get('FILE_NAME')

SLACK_TOKEN = os.environ.get('SLACK_TOKEN')
SLACK_CHANNEL = os.environ.get('SLACK_CHANNEL')
