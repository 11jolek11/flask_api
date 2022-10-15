import requests
from os import path


def send_file(host, path_to_file:str):
    url = host + '/upload'
    if path.exists(path_to_file):
        print(path_to_file)
        payload={}
        files=[
            ('file',(path.basename(path_to_file),open(path_to_file,'rb'),'text/plain'))
        ]
        headers = {}
        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        print(response.json()['message'])
    else:
        print("File not found")


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


def get_line(host: str,file:str, line: int):
    payload = {'line': str(line)}
    req = requests.get(host + '/files/' + file, params=payload)
    print(req.url)
    code = req.status_code
    if code != 200:
        print('Server error: ' + code)
        return int(code)
    else:
        resp = req.json()['content']
        print(resp)
        return int(code)


if __name__ == "__main__":
    download_file_list('http://localhost:5000')
    #get_line('http://localhost:5000', 'text.txt', 1)
    send_file('http://localhost:5000', './test.txt')
    download_file_list('http://localhost:5000')






