import requests
import datetime


def get_date_week_ago():
    date_now = datetime.date.today()
    days_week = 7
    date_week_ago = date_now - datetime.timedelta(days=days_week)
    return date_week_ago.isoformat()


def get_trending_repositories(
        date_ago,
        top_size,
        url_api_github='https://api.github.com/search/repositories',
        sort='stars',
        order='desk'
):
    search_params = {
        'q': 'created:>{}'.format(date_ago),
        'sort': sort,
        'order': order
    }
    try:
        response = requests.get(url_api_github, params=search_params)
        if response.ok:
            repositories = response.json()
            return repositories['items'][:top_size]
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        return None


def get_issues_amount(repo_full_name):
    reposetory_issues = 'https://api.github.com/repos/{}/issues'.format(
        repo_full_name
    )
    response = requests.get(reposetory_issues)
    if response.ok:
        return len(response.json())


def print_trend_repository(trend_repository, issues_amount):
    print('{full_name}:'.format(full_name=trend_repository['full_name']))
    print('\t\turl_repository: {url_repository}'.format(
        url_repository=trend_repository['url']
    ))
    print('\t\tissues amount: {issues_amount}'.format(
        issues_amount=issues_amount
    ))


if __name__ == '__main__':
    date_week_ago = get_date_week_ago()
    top_size = 20
    trending_repositories = get_trending_repositories(date_week_ago, top_size)
    if trending_repositories:
        print('New popular projects on github for the week:')
        for trend_repository in trending_repositories:
            issues_amount = get_issues_amount(trend_repository['full_name'])
            if issues_amount is None:
                issues_amount = 'no data'
            print_trend_repository(trend_repository, issues_amount)
    else:
        print('Can not load data.')
