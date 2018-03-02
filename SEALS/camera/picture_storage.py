from os import path, getenv


def get_picture_directory():
    user = getenv('DJANGO_STATIC_DIR', '~/')
    if user == '~/':
        raise EnvironmentError

    p = path.expanduser(user)
    return p + '/alarm_pictures/'
