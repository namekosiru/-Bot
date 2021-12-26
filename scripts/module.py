import sys, os
from github import Github
from pytz import timezone
from docx import Document
import sqlite3
import requests
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
from collections import defaultdict
import datetime

import settings

def make_word_count(file_name):
    document = Document(file_name)
    total_chars = 0
    for i in document.paragraphs:
        total_chars += len(i.text)
    return total_chars

def make_git_date(token, repo_name):
    g = Github(token)
    repo = g.get_repo(repo_name)
    commit_obj = repo.get_commits()[0].commit

    author_name = commit_obj.author.name
    author_date_gmt = commit_obj.author.date
    author_date_jp = author_date_gmt.astimezone(timezone('Asia/Tokyo'))


    committer_name = commit_obj.committer.name
    committer_date_gmt = commit_obj.committer.date
    committer_date_jp = committer_date_gmt.astimezone(timezone('Asia/Tokyo'))


    message = commit_obj.message

    return (committer_name, committer_date_jp, message)

def data_processing(dbname):
    users_data = defaultdict(lambda: defaultdict(dict))
    #データの抜き出し
    conn = sqlite3.connect(dbname)
    df = pd.read_sql('SELECT * FROM users', conn)
    conn.close()

    #データの加工
    users_name = df['committer_name'].unique()
    users_name_dic = defaultdict(lambda: defaultdict(dict))
    for user_name in users_name:
        user_df = df.query(f'committer_name == "{user_name}"')
        count_list = user_df['count'].values
        date_list = pd.to_datetime(user_df['committer_time'].values)
        users_name_dic[user_name] = {'date': date_list, 'count': count_list}

    return users_name_dic

def data_plot(users_dict):
    figure = plt.figure(figsize=(12,8))
    axes = figure.add_subplot(111)

    for user, item in users_dict.items():
    #描画
        if user == "namekosiru":
            axes.plot(item['date'], item['count'], label=user, linestyle="--", marker="s", alpha=0.9, ms=4)
        elif user == "KIKUMIYA":
            axes.plot(item['date'], item['count'], label=user, linestyle=":", marker="^", alpha=0.9, ms=4)
        elif user == "niromas":
            axes.plot(item['date'], item['count'], label=user, linestyle="-.", marker="*", alpha=0.9, ms=4)
        else:
            axes.plot(item['date'], item['count'], label=user)
    new_xticks = date2num([
            datetime.datetime(2021, 9, 15),
            datetime.datetime(2021, 10, 1),
            datetime.datetime(2021, 10, 15),
            datetime.datetime(2021, 11, 1),
            datetime.datetime(2021, 11, 15),
            datetime.datetime(2021, 12, 1),
            datetime.datetime(2021, 12, 15),
            datetime.datetime(2022, 1, 1),
            datetime.datetime(2022, 1, 15),
            datetime.datetime(2022, 1, 31)])

    #各軸の詳細設定
    axes.set_title("progress")
    axes.set_xlabel("date")
    axes.set_ylabel("chars")

    #x軸の設定
    xaxis = axes.xaxis
    xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
    xaxis.set_major_locator(ticker.FixedLocator(new_xticks))
    axes.set_xlim(datetime.datetime(2021,9,1), datetime.datetime(2022,1,31)) 
    axes.tick_params(axis='x', rotation=70)

    #y軸
    axes.set_ylim(0, 25000)

    #表示形式
    axes.grid(True)
    axes.legend()

    dt_now = datetime.datetime.now()
    base_path = os.path.dirname(os.path.abspath(__file__))
    figure.savefig(base_path + "/../outputs/"+dt_now.strftime('%Y%m%d_%H')+".jpg")

def send2slack(img_path, slack_token, slack_channel):
    url = "https://slack.com/api/files.upload"

    files = {'file': open(img_path, 'rb')}
    param = {
        'token': slack_token,
        'channels': slack_channel,
        "filename":"plot.jpg",
        "initial_comment":"卒論が更新されたよ！",
    }

    requests.post(url, data=param, files=files)

if __name__ == "__main__":
    token = settings.GAT
    repo_name = settings.REPO_NAME
    file_name = settings.FILE_NAME

    # count = make_word_count(file_name)
    obj = data_processing('commit.db')
    data_plot(obj)