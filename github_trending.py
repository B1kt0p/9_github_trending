import requests
import datetime


def get_date_week_ago():
    date_now = datetime.date.today()
    days_week = 7
    date_week_ago = date_now - datetime.timedelta(days=days_week)
    return date_week_ago.isoformat()

def downlowd_information_repositories(
        date_ago,
        url_api_github='https://api.github.com/search/repositories',
        sort='stars',
        order='desk'
):
    search_params = {
        'q':"created:>{}".format(date_ago),
        'sort': sort,
        'order': order
    }
    try:
        response = requests.get(url_api_github, params=search_params)
        if response.ok:
            return response.json()
        else:
            return None
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        return None


def get_trending_repositories(repositories, top_size):
    return repositories['items'][:top_size]


def get_open_reposetory_issues(repo_full_name):
    url_api = {'main_url': 'https://api.github.com/repos/', 'add_url': '/issues'}
    reposetory_issues = url_api['main_url'] + repo_full_name + url_api['add_url']
    response = requests.get(reposetory_issues)
    if response.ok:
        return response.json()
    else:
        return None


def count_issues_amount(reposetory_issues):
    return len(reposetory_issues)


def print_trend_repository(trend_repository, issues_amount):
    print('{full_name}:'.format(full_name=trend_repository['full_name']))
    print('\t\turl_repository: {url_repository}'.format(url_repository=trend_repository['url']))
    print('\t\tissues amount: {issues_amount}'.format(issues_amount=issues_amount))


if __name__ == '__main__':
    date_week_ago = get_date_week_ago()
    repositories = downlowd_information_repositories(date_week_ago)
    if repositories:
        print('New popular projects on github for the week:')
        top_size = 20
        trending_repositories = get_trending_repositories(repositories, top_size)
        for trend_repository in trending_repositories:
            reposetory_issues = get_open_reposetory_issues(trend_repository['full_name'])
            if reposetory_issues == None:
                issues_amount = 'no date'
            else:
                issues_amount = count_issues_amount(reposetory_issues)
            print_trend_repository(trend_repository, issues_amount)
    else:
        print('Can not load data.')
