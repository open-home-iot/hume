import os
import sys


if len(sys.argv) < 2:
    print('ERROR')
    print('You need to supply at least one argument of where the environment variable should be saved.')
    exit(1)

user_path = os.path.expanduser('~/')

save_location = sys.argv[1]
if os.path.isfile(user_path + save_location):
    print('Saving into: ' + save_location)
else:
    print('ERROR')
    print('The supplied save location does not exist.')
    exit(1)


def find(name, path):
    exclude = {'.virtualenvs', 'frontend'}

    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in exclude]
        if name in dirs:
            return os.path.join(root, name)

    raise FileNotFoundError('Could not find static directory, have you cloned the HOME-interface repository?')


# find hint
hint_path = find('HOME-interface', user_path)

# find static dir
static_dir = find('static', hint_path)

# prune user path
static_path = '~/' + static_dir[len(user_path):]

# insert into
with open(user_path + save_location, 'a') as file:
    lines = ['\n\n', '# HOME env vars\n', 'export DJANGO_STATIC_DIR=' + static_path + '\n']
    file.writelines(lines)
