import os
from glob import glob
import datetime
from module import data_processing, data_plot, send2slack

dbname = 'commit.db'
SLACK_TOKEN = os.environ.get('SLACK_TOKEN')
SLACK_CHANNEL = os.environ.get('SLACK_CHANNEL')

users_dict = data_processing(dbname)

data_plot(users_dict)

output_file = sorted(glob('outputs/*'))[-1]

send2slack(output_file, SLACK_TOKEN, SLACK_CHANNEL)
