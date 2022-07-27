import os
from dotenv import load_dotenv

load_dotenv()

BASE_PATH = 'wines.xlsx'
SETTING_PATH = os.getenv('SETTING_PATH', BASE_PATH)