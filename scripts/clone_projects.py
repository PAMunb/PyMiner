import csv
import git
import os
import stat
import sys

# python3 runner.py /path/to/directory/ /path/to/file.csv

# git config --global core.longpaths true

cwd = sys.argv[1]
clear = []
count = 1
with open(sys.argv[2], newline='', encoding='latin-1') as f:
    projects = csv.reader(f, delimiter=',')
    for project in projects:
        if project[1] == "name":
            continue
        print(count)
        projectName = project[1].split('/')
        path = cwd + projectName[1].strip()
        url = "https://github.com/" + project[1] + ".git"
        print(path, url)
        try:
            if os.path.isdir(path):
                if not os.access(path, os.W_OK):
                    os.chmod(path, stat.S_IWUSR)
                    os.system("rmdir /s /q " + path)
                    print("cloning: " + projectName[1].strip())
                    git.Git(cwd).clone(url.strip())
                else:
                    os.system("rmdir /s /q " + path)
                    print("cloning: " + projectName[1].strip())
                    git.Git(cwd).clone(url.strip())
            else:
                print("cloning: " + projectName[1].strip())
                git.Git(cwd).clone(url.strip())
            count = count + 1
        except UnicodeDecodeError as e:
            print(f"Error decoding Unicode in project: {project[1]}")
            print(e)
            clear.append(projectName[1].strip())
            if os.path.isdir(path):
                os.chmod(path, stat.S_IWUSR)
                os.system("rmdir /s /q " + path)
        except Exception as e:
            print(f"Error cloning project: {project[1]}")
            print(e)
            clear.append(projectName[1].strip())
            if os.path.isdir(path):
                os.chmod(path, stat.S_IWUSR)
                os.system("rmdir /s /q " + path)

    print(clear)
