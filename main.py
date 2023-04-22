import os

from data_base import create_database, save_data_to_database
from config import config
from utils import get_id_employers
from classes import *


def main():
    hh = Employers('Сбер')

    params = config()
    data = hh.get_request

    create_database('hh_parser', params)
    save_data_to_database(data, 'hh_parser', params)


if __name__ == '__main__':
    main()
