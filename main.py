import argparse
from datetime import datetime, timedelta
import json
import csv
from pathlib import Path
from github import Github

parser = argparse.ArgumentParser()
parser.add_argument("token", help="github token")
parser.add_argument('--fork', dest='fork', action='store_true', help='include forks')
parser.add_argument('--path', help='file path', default='repo-data.csv')
parser.set_defaults(fork=False)
args = parser.parse_args()

github = Github(args.token)
yesterday_date = datetime.now() + timedelta(days=-1)
user = github.get_user()

for repo in github.get_user(user.login).get_repos():
    if repo.fork and not args.fork:
        continue
    repo_pulls = repo.get_pulls(state='all')
    repo_issues = repo.get_issues(state='all')
    repo_contributors = repo.get_contributors(anon='true')

    repo_data = {
        "date": yesterday_date.strftime("%Y-%m-%d"),
        "full_name": repo.full_name,
        "subscribers_count": repo.subscribers_count,
        "stargazers_count": repo.stargazers_count,
        "forks_count": repo.forks_count,
        "size": repo.size,
        "contributors": repo_contributors.totalCount,
        "views": 0,
        "unique_views": 0,
        "clones": 0,
        "unique_clones": 0,
        "open_issues": 0,
        "closed_issues": 0,
        "open_pr": 0,
        "merged_pr": 0,
        "closed_pr": 0
    }

    repo_views = repo.get_views_traffic()

    if repo_views['views']:
        last_view_count = repo_views['views'][-1]
        if last_view_count:
            if last_view_count.timestamp.strftime("%Y-%m-%d") == yesterday_date.strftime("%Y-%m-%d"):
                repo_data["views"] = last_view_count.count
                repo_data["unique_views"] = last_view_count.uniques
            elif len(repo_views['views']) >= 2:
                last_view_count = repo_views['views'][-2]
                if last_view_count.timestamp.strftime("%Y-%m-%d") == yesterday_date.strftime("%Y-%m-%d"):
                    repo_data["views"] = last_view_count.count
                    repo_data["unique_views"] = last_view_count.uniques


    repo_clones = repo.get_clones_traffic()

    if repo_clones['clones']:
        last_clone_count = repo_clones['clones'][-1]
        if last_clone_count:
            if last_clone_count.timestamp.strftime("%Y-%m-%d") == yesterday_date.strftime("%Y-%m-%d"):
                repo_data["clones"] = last_clone_count.count
                repo_data["unique_clones"] = last_clone_count.uniques
            elif len(repo_clones['clones']) >= 2:
                last_clone_count = repo_clones['clones'][-2]
                if last_clone_count.timestamp.strftime("%Y-%m-%d") == yesterday_date.strftime("%Y-%m-%d"):
                    repo_data["clones"] = last_clone_count.count
                    repo_data["unique_clones"] = last_clone_count.uniques

    issues_open = repo.get_issues(state='open')
    repo_data['open_issues'] = sum(map(lambda x: x.pull_request is None, issues_open))

    issues_closed = repo.get_issues(state='closed')
    repo_data['closed_issues'] = sum(map(lambda x: x.pull_request is None, issues_closed))

    repo_data['open_pr'] = repo.get_pulls(state='open').totalCount
    pull_request_closed = repo.get_pulls(state='closed')
    repo_data['merged_pr'] = sum(map(lambda x: x.merged, pull_request_closed))
    repo_data['closed_pr'] = repo.get_pulls(state='closed').totalCount - repo_data['merged_pr']

    path = args.path
    fieldnames = ['date', 'full_name', 'subscribers_count', 'stargazers_count', 'forks_count', 'size', 'contributors', 'views', 'unique_views', 'clones', 'unique_clones', 'open_issues', 'closed_issues', 'open_pr', 'merged_pr', 'closed_pr']
    my_file = Path(path)

    if not my_file.is_file():
        with open(path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(repo_data)

    with open(path, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(repo_data)

    print(json.dumps(repo_data))
