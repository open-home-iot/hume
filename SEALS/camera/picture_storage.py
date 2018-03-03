from os import path, getenv


def get_picture_directory():
    user = getenv('DJANGO_STATIC_DIR', '~/')
    if user == '~/':
        raise EnvironmentError('You do not seem to have installed the project correctly, environment variable missing.')

    p = path.expanduser(user)
    return p + '/alarm_pictures/'
