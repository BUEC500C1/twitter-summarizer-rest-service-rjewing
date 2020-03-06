import os
import subprocess
import configparser
from requests import get

basedir = os.path.abspath(os.path.dirname(__file__))

def load_config(key, section='auth'):
    if os.path.exists('./keys'):
        config_parser = configparser.ConfigParser()
        config_parser.read("./keys")
        return config_parser.get(section, key).strip()
    return None


class Config():
    TWITTER_API_KEY = load_config('consumer_key') or os.getenv('EC500_TWITTER_API_KEY')
    TWITTER_SECRET_KEY = load_config('consumer_secret') or os.getenv('EC500_TWITTER_SECRET_KEY')
    TWITTER_ACCESS_TOKEN = load_config('access_token') or os.getenv('EC500_TWITTER_ACCESS_TOKEN')
    TWITTER_ACCESS_SECRET = load_config('access_secret') or os.getenv('EC500_TWITTER_ACCESS_SECRET')

    SECRET_KEY = os.getenv('EC500_SECRET_KEY', 'dev_key')

    # Set Host and Port
    API_IP = '0.0.0.0'
    API_PORT = 80
    API_PUBLIC_IP = get('https://api.ipify.org').text
    API_HOSTNAME = subprocess.check_output("/usr/bin/dig -x {API_PUBLIC_IP} +short", shell=True)[0:-2].decode("ascii")

    GMAIL_EMAIL = os.getenv('EC500_GMAIL_EMAIL')
    GMAIL_PASSWORD = os.getenv('EC500_GMAIL_PASSWORD')

    NUM_WORKERS = 2
