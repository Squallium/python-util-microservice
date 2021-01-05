import hashlib
import logging
import os
import shutil
import sys
from pathlib import Path

from git import Repo


class LazyFrontend:
    FULL_LOG_INFO = False
    WRITE_MODE = False

    WINDOWS_LINE_ENDING = b'\r\n'
    UNIX_LINE_ENDING = b'\n'

    IGNORED_FOLDERS = ['node_modules', '.idea']
    IGNORED_FILES = ['.DS_Store']
    IGNORED_EXTENSIONS = []

    FRONTEND_PROJECT_PATH = '/Users/borja.refoyo/Personal/frontend-macroservice'
    INTRANET_PROJECT_TEMP_PATH = '/Users/borja.refoyo/Personal/temp/genera-intranet'
    FRONTEND_PROJECT_TEMP_PATH = os.path.join(INTRANET_PROJECT_TEMP_PATH, 'metronic')
    NEW_VERSION_PROJECT_PATH = '/Users/borja.refoyo/Personal/temporal/metronic_v7.1.8/theme/angular/demo1'

    BEGIN_COMMIT = '94b05261f889ce8eec62db59d134e2c3bb20ea6a'
    END_COMMIT = '5e9a533b88731942f956a3a8c11e7fafe4706cca'

    def __init__(self, params) -> None:
        # atributos de la clase
        self.files_new_version = {}
        self.files_prev_version = {}
        self.modified_files = []

    def run_job(self):
        pass
        self.fix_crlf_to_lf()
        # self.update_version()
        # self.copy_modified_files()

    def calculate_modified_files(self):
        logging.warning('')
        logging.warning('=================================================================')
        logging.info('FICHEROS MODIFICADOS DESDE LA ULTIMA ACTUALIZACIÓN')
        logging.warning('=================================================================')
        logging.warning('')

        logging.info(Repo(self.INTRANET_PROJECT_TEMP_PATH).active_branch.name)
        commits = self.__commits_between_two_commits(self.BEGIN_COMMIT, self.END_COMMIT)
        for commit in commits:
            if not commit.message.startswith('[IGNORE]'):
                for file in commit.stats.files:
                    if file.startswith('metronic/'):
                        self.modified_files.append(file.replace('metronic/', ''))
        self.modified_files = list(dict.fromkeys(self.modified_files))
        logging.info(self.modified_files)

    def copy_modified_files(self):
        self.calculate_modified_files()

        for mod_file in self.modified_files:

            src = os.path.join(self.FRONTEND_PROJECT_TEMP_PATH, mod_file)
            dst = os.path.join(self.FRONTEND_PROJECT_PATH, mod_file)
            logging.info(f'src ----> {src}')
            logging.info(f'dst ----> {dst}')
            if self.WRITE_MODE:
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copyfile(src, dst)

    def fix_crlf_to_lf(self):
        files = self.__list_folder_files(self.NEW_VERSION_PROJECT_PATH)
        for file in files:
            if file.lower().endswith(('.ts', '.html', '.scss', '.svg', '.css', '.js', '.txt', '.htaccess', '.json',
                                      'browserslist', '.md')):
                self.file_from_crlf_to_lf(file)

    def file_from_crlf_to_lf(self, file_path):
        with open(file_path, 'rb') as open_file:
            content = open_file.read()

        content = content.replace(self.WINDOWS_LINE_ENDING, self.UNIX_LINE_ENDING)

        with open(file_path, 'wb') as open_file:
            open_file.write(content)

    def update_version(self):
        self.calculate_modified_files()

        self.__extract_version_files(self.FRONTEND_PROJECT_PATH, self.FRONTEND_PROJECT_PATH, self.files_prev_version)
        if self.FULL_LOG_INFO:
            logging.warning('')
            logging.warning('=================================================================')
            logging.warning('FICHEROS DE LA ACTUAL VERSION')
            logging.warning('=================================================================')
            logging.warning('')
        # for key in self.files_new_version.keys():
        #     if self.FULL_LOG_INFO:
        #         logging.info(f'{key} -> {self.files_new_version[key]}')

        self.__extract_version_files(self.NEW_VERSION_PROJECT_PATH, self.NEW_VERSION_PROJECT_PATH,
                                     self.files_new_version)
        if self.FULL_LOG_INFO:
            logging.warning('')
            logging.warning('=================================================================')
            logging.warning('FICHEROS DE LA NUEVA VERSION')
            logging.warning('=================================================================')
            logging.warning('')
        # for key in self.files_new_version.keys():
        #     if self.FULL_LOG_INFO:
        #         logging.info(f'{key} -> {self.files_new_version[key]}')

        logging.warning('')
        logging.warning('=================================================================')
        logging.info('FICHEROS EN AMBAS VERSIONES')
        logging.warning('=================================================================')
        logging.warning('')

        # comparamos los dos diccionarios para ver las diferencias
        same_file_same_path = []
        diff_file_same_path = []
        for new_file_id in self.files_new_version.keys():
            basename = self.files_new_version[new_file_id]['basename']
            prev_abs_path = self.files_new_version[new_file_id]['abs_path'][0]
            if new_file_id in self.files_prev_version:
                new_rel_path = self.files_new_version[new_file_id]["rel_path"]
                prev_rel_path = self.files_prev_version[new_file_id]["rel_path"]

                md5_check = self.files_new_version[new_file_id]["md5"] == \
                            self.files_prev_version[new_file_id]["md5"]
                if md5_check:
                    same_file_same_path.append(
                        f'{new_file_id}: [{new_rel_path}] -> [{prev_rel_path}]')
                else:
                    diff_file_same_path.append(
                        f'{new_file_id}: [{new_rel_path}] -> [{prev_rel_path}]')

                    # borramos el original
                    prev_abs_paths = self.files_prev_version[new_file_id]["abs_path"]
                    for prev_file in prev_abs_paths:
                        if self.WRITE_MODE:
                            os.remove(prev_file)

                    # copiamos el nuevo
                    src = self.files_new_version[new_file_id]["abs_path"][0]
                    dst = os.path.join(self.FRONTEND_PROJECT_PATH, new_rel_path, basename)
                    if self.FULL_LOG_INFO:
                        logging.info(f'src ----> {src}')
                        logging.info(f'dst ----> {dst}')
                    if self.WRITE_MODE:
                        os.makedirs(os.path.dirname(dst), exist_ok=True)
                        shutil.copyfile(src, dst)

        # self.__log_compare_report(same_file_same_path, 'IGUALES Y MISMO LUGAR', logging.info)
        self.__log_compare_report(diff_file_same_path, 'DISTINTOS Y MISMO LUGAR', logging.warning)

        logging.warning('')
        logging.warning('=================================================================')
        logging.info('FICHEROS NUEVOS')
        logging.warning('=================================================================')
        logging.warning('')

        for new_file_id in self.files_new_version.keys():
            basename = self.files_new_version[new_file_id]['basename']
            if new_file_id not in self.files_prev_version:
                rel_path = self.files_new_version[new_file_id]["rel_path"]
                logging.warning(f'{new_file_id}: [{rel_path}]')
                src = self.files_new_version[new_file_id]["abs_path"][0]
                dst = os.path.join(self.FRONTEND_PROJECT_PATH, rel_path, basename)
                logging.info(f'src ----> {src}')
                logging.info(f'dst ----> {dst}')
                if self.WRITE_MODE:
                    try:
                        os.makedirs(os.path.dirname(dst))
                    except FileExistsError as fee:
                        pass
                    shutil.copyfile(src, dst)

        logging.warning('')
        logging.warning('=================================================================')
        logging.info('FICHEROS QUE NO ESTÁN YA, SERÁN BORRADOS')
        logging.warning('=================================================================')
        logging.warning('')

        for new_file_id in self.files_prev_version.keys():
            if new_file_id not in self.files_new_version:
                # logging.error(f'{new_file_name}: [{self.files_prev_version[new_file_name]["rel_path"]}]')
                prev_abs_paths = self.files_prev_version[new_file_id]["abs_path"]
                for prev_file in prev_abs_paths:
                    if new_file_id in self.modified_files:
                        logging.warning(f'deleting ---> {prev_file}')
                    else:
                        logging.info(f'deleting ---> {prev_file}')
                    if self.WRITE_MODE:
                        os.remove(prev_file)

    def __extract_version_files(self, project_path_folder, prefix, files_dict, replacers=[], movements={}):
        files = self.__list_folder_files(project_path_folder)
        for file in files:
            basename = os.path.basename(file)
            rel_path = os.path.join(*file.replace(prefix, '').replace('/' + basename, '').split('/'))
            if all(x not in rel_path for x in self.__ignored_folders()):
                if all(not basename.endswith(x) for x in self.IGNORED_EXTENSIONS):
                    if all(x not in basename for x in self.IGNORED_FILES):
                        for rep in replacers:
                            rel_path = os.path.join(*rel_path.replace(rep, '').split('/'))
                        if basename not in files_dict.keys():
                            file_id = os.path.join(rel_path, basename)
                            if movements:
                                movement = self.__find_movement_in_dict(rel_path, movements)
                                if movement:
                                    file_id = os.path.join(movement, basename)
                                else:
                                    logging.error(f'Movimiento no controlado par el fichero: {file}')
                                    sys.exit(1)

                            files_dict[file_id] = {
                                'basename': basename,
                                'abs_path': [file],
                                'rel_path': rel_path,
                                'md5': self.__md5(file)
                            }
                        else:
                            logging.error(f'Duplicate file: {file}')
                            sys.exit(1)
                            # files_dict[basename]['abs_path'].append(file)

    def __commits_between_two_commits(self, begin_commit, end_commit):
        result = []

        repo = Repo(self.INTRANET_PROJECT_PATH, search_parent_directories=True)

        ready = False
        for commit in repo.iter_commits():
            if not ready and commit.hexsha == begin_commit:
                ready = True

            if ready:
                result.append(commit)
                logging.info(commit)

            if commit.hexsha == end_commit:
                break

        return result

    def __list_folder_files(self, folder):
        result = []
        for root, dirs, files in os.walk(folder, topdown=True):
            result += [os.path.join(root, f) for f in files]

        return result

    def __find_movement_in_dict(self, new_rel_path, movements):
        result = None

        if new_rel_path in movements.keys():
            result = movements[new_rel_path]
        else:
            split_path = new_rel_path.split('/')
            for i in range(len(split_path) - 1, 0, -1):
                sub_key = '/'.join(split_path[0:i])
                if sub_key in movements.keys():
                    result = os.path.join(movements[sub_key], os.path.join(*split_path[i:]))
                    break

        return result

    def __md5(self, fname):
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def __log_compare_report(self, logs, title, logger):
        logging.info(title)
        for log in logs:
            logger(log)

    def __ignored_folders(self):
        return self.IGNORED_FOLDERS

    def lol(self, repo):
        commit = repo.commit(sys.argv[1])
        for path in self.list_paths(commit.tree):
            print(path)

    def list_paths(self, root_tree, path=Path(".")):
        for blob in root_tree.blobs:
            yield path / blob.name
        for tree in root_tree.trees:
            yield from self.list_paths(tree, path / tree.name)
