import requests
from config_interpreter import host, protocol, api_key

if __name__ == '__main__':
    url = f'{protocol}://{host}/api/v1/unit/object?hierarchy=1&id=1&api_key={api_key}'

    response = requests.request("GET", url)

    print(response.text)
