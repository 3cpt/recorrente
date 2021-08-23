import argparse
import datetime
import json
import csv
from pathlib import Path
from github import Github

parser = argparse.ArgumentParser()
parser.add_argument("token", help="github token")
parser.add_argument("user", help="github username")
args = parser.parse_args()

github = Github(args.token)

for repo in github.get_user(args.user).get_repos():
    repo_pulls = repo.get_pulls(state='all')
    repo_issues = repo.get_issues(state='all')
    repo_contributors = repo.get_contributors(anon='true')

    repo_data = {
        "date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "full_name": repo.full_name,
        "subscribers_count": repo.subscribers_count,
        "stargazers_count": repo.stargazers_count,
        "forks_count": repo.forks_count,
        "size": repo.size,
        "contributors": repo_contributors.totalCount,
        "views": 0,
        "unique_views":0,
        "clones":0,
        "unique_clones":0,
        "open_issues": 0,
        "closed_issues": 0,
        "open_pr": 0,
        "merged_pr": 0,
        "closed_pr": 0
    }


    repo_views = repo.get_views_traffic()

    if repo_views['views']:
        repo_data["views"] = repo_views['views'][-1].count
        repo_data["unique_views"] = repo_views['views'][-1].uniques


    repo_clones = repo.get_clones_traffic()

    if repo_clones['clones']:
        repo_data["clones"] = repo_clones['clones'][-1].count
        repo_data["unique_clones"] = repo_clones['clones'][-1].uniques

    issues_open = repo.get_issues(state='open')
    repo_data['open_issues'] = sum(map(lambda x : x.pull_request is None, issues_open))

    issues_closed = repo.get_issues(state='closed')
    repo_data['closed_issues'] = sum(map(lambda x : x.pull_request is None, issues_closed))

    repo_data['open_pr'] = repo.get_pulls(state='open').totalCount
    pull_request_closed =repo.get_pulls(state='closed')
    repo_data['merged_pr'] = sum(map(lambda x : x.merged , pull_request_closed))
    repo_data['closed_pr'] = repo.get_pulls(state='closed').totalCount - repo_data['merged_pr']

    path = 'repo-data.csv'
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
