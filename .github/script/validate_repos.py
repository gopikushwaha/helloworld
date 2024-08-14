import os
import requests

def get_repositories(org, token):
    headers = {'Authorization': f'token {token}'}
    repos = []
    page = 1
    while True:
        response = requests.get(f'https://api.github.com/orgs/{org}/repos?page={page}&per_page=100', headers=headers)
        response.raise_for_status()
        repos_page = response.json()
        if not repos_page:
            break
        repos.extend(repos_page)
        page += 1
    return repos

def validate_repo_name(name):
    pattern = r'^[a-z0-9]+(-[a-z0-9]+)*$'  # Example pattern: lower-case letters, numbers, hyphens
    return re.match(pattern, name) is not None

def main():
    org = os.getenv('ORGANIZATION')
    token = os.getenv('GITHUB_TOKEN')
    
    repos = get_repositories(org, token)
    
    invalid_repos = [repo['name'] for repo in repos if not validate_repo_name(repo['name'])]
    
    if invalid_repos:
        print(f"Invalid repository names: {', '.join(invalid_repos)}")
        exit(1)
    else:
        print("All repository names are valid.")

if __name__ == '__main__':
    import re
    main()
