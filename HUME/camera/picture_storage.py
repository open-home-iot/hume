import os

from datetime import datetime


def get_picture_directory():
    user = os.getenv('DJANGO_STATIC_DIR', '~/')
    if user == '~/':
        raise EnvironmentError('You do not seem to have installed the project correctly, environment variable missing.')

    alarm_pic_path = os.path.expanduser(user) + '/alarm_pictures/'

    current_month_dir = datetime.now().strftime('%Y_%m') + '/'

    final_path = alarm_pic_path + current_month_dir

    if not os.path.exists(final_path):
        os.makedirs(final_path)

    return final_path
