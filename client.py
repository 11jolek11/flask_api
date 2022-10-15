import requests
from os import path


def send_file():
    pass


def download_file_list(host: str) -> int:
    req = requests.get(host + '/files')
    code = req.status_code
    if code != 200:
        print('Server error: ' + code)
        return int(code)
    else:
        files = req.json()['files']
        for file in files:
            print(file)
        return int(code)


def get_line(host: str, line: int):
    pass


if __name__ == "__main__":
    download_file_list('http://localhost:5000')
