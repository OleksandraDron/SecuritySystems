import json

# Функція для завантаження даних з JSON-файлу
def load_data():
    try:
        with open('filesystem.json') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {
            'current_directory': '/',
            'users': {
                'root': {
                    'password': 'root',
                    'permissions': {'read': True, 'edit': True}
                }
            },
            'files': {},
            'directories': {}
        }
    return data


# Функція для збереження даних у JSON-файлі
def save_data(data):
    with open('../../Desktop/filesystem.json', 'w') as file:
        json.dump(data, file, indent=4)


# Функція для входу в систему або реєстрації нового користувача
def login(data):
    username = input('Username: ')
    password = input('Password: ')

    if username in data['users']:
        if data['users'][username]['password'] == password:
            data['current_user'] = username
            print(f'Logged in as {username}')
        else:
            print('Invalid password')
    else:
        register = input('User not found. Register as a new user? (y/n): ')
        if register.lower() == 'y':
            data['users'][username] = {
                'password': password,
                'permissions': {'read': False, 'edit': False}
            }
            data['current_user'] = username
            print(f'New user registered: {username}')
        else:
            print('User not registered')


# Функція для перевірки пароля користувача
def check_password(data, username, password):
    if username in data['users']:
        if data['users'][username]['password'] == password:
            return True
    return False


# Функція для отримання поточного шляху
def pwd(data):
    print(f'Current directory: {data["current_directory"]}')


# Функція для виведення списку файлів та папок поточного каталогу
def ls(data):
    current_directory = data['current_directory']
    print(f'Contents of {current_directory}:')

    for name, info in data['directories'].items():
        if info['parent'] == current_directory:
            print(f'Directory: {name}/')

    for name, info in data['files'].items():
        if info['parent'] == current_directory:
            print(f'File: {name}')


# Функція для створення нової папки
def mkdir(data):
    directory_name = input('Enter directory name: ')
    current_directory = data['current_directory']

    if directory_name in data['directories']:
        print('Directory already exists')
    else:
        permissions = {
            'owner': data['current_user'],
            'read': True,
            'edit': True
        }
        data['directories'][directory_name] = {
            'parent': current_directory,
            'permissions': permissions
        }
        print(f'Created directory: {directory_name}')


# Функція для створення нового файлу
def create_file(data):
    file_name = input('Enter file name: ')
    current_directory = data['current_directory']

    if file_name in data['files']:
        print('File already exists')
    else:
        permissions = {
            'owner': data['current_user'],
            'read': True,
            'edit': True
        }
        file_content = input('Enter file content: ')
        data['files'][file_name] = {
            'parent': current_directory,
            'permissions': permissions,
            'content': file_content
        }
        print(f'Created file: {file_name}')


# Функція для редагування файлу
def edit_file(data):
    file_name = input('Enter file name: ')
    current_directory = data['current_directory']

    if file_name in data['files'] and current_directory == data['files'][file_name]['parent']:
        username = data['current_user']
        file_permissions = data['files'][file_name]['permissions']

        if username == file_permissions['owner'] or username == 'root' or file_permissions['edit']:
            new_content = input('Enter new content: ')
            data['files'][file_name]['content'] = new_content
            print(f'File {file_name} updated')
        else:
            print('You do not have permission to edit this file')
    else:
        print('File not found')


# Функція для зміни поточного каталогу
def cd(data):
    directory_name = input('Enter directory name: ')
    current_directory = data['current_directory']

    if directory_name in data['directories']:
        if directory_name == '..':
            if current_directory == '/':
                print('Already at the root directory')
            else:
                data['current_directory'] = '/'.join(current_directory.split('/')[:-2]) + '/'
                print(f'Current directory changed to {data["current_directory"]}')
        else:
            data['current_directory'] = current_directory + directory_name + '/'
            print(f'Current directory changed to {data["current_directory"]}')
    else:
        print('Directory not found')


# Функція для зміни прав доступу до файлу
def change_permissions(data):
    file_name = input('Enter file name: ')
    current_directory = data['current_directory']

    if file_name in data['files'] and current_directory == data['files'][file_name]['parent']:
        username = data['current_user']
        file_permissions = data['files'][file_name]['permissions']

        if username == file_permissions['owner'] or username == 'root':
            read_permission = input('Read permission (y/n): ')
            edit_permission = input('Edit permission (y/n): ')

            if read_permission.lower() == 'y':
                file_permissions['read'] = True
            else:
                file_permissions['read'] = False

            if edit_permission.lower() == 'y':
                file_permissions['edit'] = True
            else:
                file_permissions['edit'] = False

            print(f'Permissions for file {file_name} changed')
        else:
            print('You do not have permission to change permissions for this file')
    else:
        print('File not found')


# Функція для видалення папки або файлу
def rm(data):
    name = input('Enter name (file/directory) to delete: ')
    current_directory = data['current_directory']

    if name in data['directories'] and current_directory == data['directories'][name]['parent']:
        del data['directories'][name]
        print(f'Directory {name} deleted')
    elif name in data['files'] and current_directory == data['files'][name]['parent']:
        del data['files'][name]
        print(f'File {name} deleted')
    else:
        print('Item not found')

# Функція для читання вмісту файла
def read(data):
    file_name = input('Enter file name: ')
    current_directory = data['current_directory']

    if file_name in data['files'] and current_directory == data['files'][file_name]['parent']:
        file_content = data['files'][file_name]['content']
        print(f'Content of file {file_name}:')
        print(file_content)
    else:
        print('File not found')


# Функція для видалення облікового запису користувача
def delete_user(data):
    username = data['current_user']
    password = input('Enter password to confirm account deletion: ')

    if check_password(data, username, password):
        del data['users'][username]
        data['current_user'] = None
        data['current_directory'] = '/'
        print(f'User {username} deleted')
    else:
        print('Invalid password')


# Функція для виходу з облікового запису користувача
def logout(data):
    data['current_user'] = None
    data['current_directory'] = '/'
    print('Logged out')


# Функція для виходу з програми
def exit_program(data):
    save_data(data)
    print('Exiting the program')
    exit()


# Основна функція для обробки команд
def main():
    data = load_data()
    commands = {
        'login': login,
        'pwd': pwd,
        'ls': ls,
        'mkdir': mkdir,
        'create': create_file,
        'edit': edit_file,
        'cd': cd,
        'change_perm': change_permissions,
        'rm': rm,
        'read': read,
        'delete_user': delete_user,
        'logout': logout,
        'exit': exit_program
    }

    while True:
        current_directory = data['current_directory']
        command = input(f'{current_directory}>')

        if command in commands:
            commands[command](data)
        else:
            print('Invalid command')


# Запуск головної функції
if __name__ == '__main__':
    main()
