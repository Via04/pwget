import argparse
from tqdm import tqdm
import requests


class PWget:
    url = None
    path = None

    def __init__(self, url: str, path=None):
        self.url = url
        self.path = path

    def download_file(self):
        down_stream = requests.get(self.url, stream=True)
        with open(self.path, 'wb') as out:
            total = int(down_stream.headers.get('content-length'))
            for chunk in tqdm(down_stream.iter_content(chunk_size=1024), total=(total/1024)+1):
                if chunk:
                    out.write(chunk)
                    out.flush()

    def print_file(self):
        req = requests.get(self.url)
        print(req.content)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Download files by url, if no arguments passed start interactive mode')
    parser.add_argument('-u', '--url', type=str, required=False, help='url for download')
    parser.add_argument('-p', '--path', type=str, required=False,
                        help='Path for file download, if not specified print in console')
    args = parser.parse_args()
    if args.url == '' or args.url is None:
        user_input = None
        while user_input != 'q':
            print('Use this program to download files. Interactive mode - select option:\n'
                  + 'p: print file in url to console\n'
                  + 'd: download file in url\n'
                  + 'q: exit program\n')
            user_input = input('Enter selected option: ')
            if user_input == 'p':
                url = input('Enter url: ')
                pwget = PWget(url)
                pwget.print_file()
            if user_input == 'd':
                url = input('Enter url: ')
                path = input('Enter download path (with file name): ')
                pwget = PWget(url, path)
                pwget.download_file()
    elif args.path == '' or args.path is None:
        url = args.url
        pwget = PWget(url)
        pwget.print_file()
    else:
        url = args.url
        path = args.path
        pwget = PWget(url, path)
        pwget.download_file()