import csv
import git
import os
import sys
import shutil
import stat
import logging

# Uso: python3 scripts/clone_projects.py /path/to/directory/ /path/to/file.csv
# Exemplo: python3 scripts/clone_projects.py ~/pamunb-workspace/PyMiner/dataset/ projects.csv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

cwd = sys.argv[1]
clear = []
count = 1

def remove_directory(path):
    """
    Remove recursivamente o diretório 'path', ajustando permissões quando necessário.
    Trata links simbólicos de forma apropriada para evitar erros.
    """
    def onerror(func, path, exc_info):
        try:
            # Se for um link simbólico, remova-o diretamente
            if os.path.islink(path):
                os.unlink(path)
            else:
                # Tenta definir permissões amplas e repetir a operação
                os.chmod(path, 0o777)
                func(path)
        except Exception as e:
            logger.error(f"Falha ao remover {path}: {e}")
    try:
        shutil.rmtree(path, onerror=onerror)
    except Exception as e:
        logger.error(f"Erro ao remover diretório {path}: {e}")

with open(sys.argv[2], newline='', encoding='latin-1') as f:
    projects = csv.reader(f, delimiter=',')
    for project in projects:
        # Pula o cabeçalho
        if project[1] == "name":
            continue

        logger.info(f"Processando projeto #{count}")
        parts = project[1].split('/')
        if len(parts) < 2:
            logger.error(f"Formato inválido para o projeto: {project[1]}")
            continue

        owner = parts[0].strip()
        repoName = parts[1].strip()
        # Nome da pasta: owner_repoName
        folder_name = owner + "_" + repoName
        # Gera o caminho absoluto onde o repositório será clonado
        path = os.path.abspath(os.path.join(cwd, folder_name))
        url = "git@github.com:" + project[1].strip() + ".git"
        logger.info(f"Caminho: {path} | URL: {url}")

        try:
            # Se o diretório já existir, removê-lo usando nossa função
            if os.path.isdir(path):
                logger.info(f"Diretório {folder_name} já existe. Removendo...")
                remove_directory(path)
                logger.info(f"Diretório existente removido: {folder_name}")

            logger.info("Clonando: " + folder_name)
            # Clona o repositório no diretório cwd com o nome folder_name
            git.Git(cwd).clone(url.strip(), folder_name)
            count += 1
        except UnicodeDecodeError as e:
            logger.error(f"Erro de decode no projeto: {project[1]}")
            logger.error(e)
            clear.append(folder_name)
            if os.path.isdir(path):
                remove_directory(path)
        except Exception as e:
            logger.error(f"Erro clonando o projeto: {project[1]}")
            logger.error(e)
            clear.append(folder_name)
            if os.path.isdir(path):
                remove_directory(path)

    logger.info("Projetos com erro: " + str(clear))
