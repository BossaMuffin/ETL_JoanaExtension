"""
Created on June 18, 2022
@author: BalthMhs
@society: BossaMuffinConnected
"""

from datetime import date, datetime, timedelta
from os import listdir
from os.path import isfile, join, abspath


class ModelCheckDate:
    """
    Classdocs
    """

    def isWeekPresentInFolder(self, p_date, p_folder, p_ext):
        e_result_to_return = {'bool': False,
                              'date': ''}
        e_last_sunday = str(self._getDateOfLastSunday(str(p_date)))
        e_files = self._listFilesFromFolder(p_folder, p_ext)
        e_dates_list = self._getDatesFromFilesList(e_files['list'])
        if e_last_sunday in e_dates_list:
            e_result_to_return['bool'] = True
            e_result_to_return['date'] = e_last_sunday
        return e_result_to_return

    def _getDateFromFilePath(self, p_file_path):
        e_datetime_to_return = p_file_path.split('_', -1)
        e_datetime_to_return = e_datetime_to_return[-1]
        e_datetime_to_return = e_datetime_to_return.split('.', 1)
        e_datetime_to_return = e_datetime_to_return[0]
        try:
            e_date = date.fromisoformat(e_datetime_to_return)
            return e_datetime_to_return
        except:
            return False

    def _getDateOfLastSunday(self, p_date: _getDateFromFilePath):
        p_date_iso = date.fromisoformat(p_date)
        e_last_sunday = p_date_iso
        e_date_day = p_date_iso.weekday()
        print(e_date_day)
        if e_date_day != 6:
            e_last_sunday = p_date_iso - timedelta(days=e_date_day + 1)
        return e_last_sunday

    def _isFileAndExtMask(self, p_folder_path: str, p_file: str, p_ext: str = "json"):
        return isfile(join(p_folder_path, p_file)) and join(p_folder_path, p_file).split(".", -1)[1] == p_ext

    def _listFilesFromFolder(self, p_folder_path: str, p_ext: str = "json"):
        e_abs_path = abspath(".")
        e_result_to_return = {
            'list': [],
            'text': '',
            'bool': False,
        }
        try:
            e_result_to_return['list'] = [l_file for l_file in listdir(p_folder_path) if
                                          self._isFileAndExtMask(p_folder_path, l_file, p_ext)]
            # e_result_to_return['list'] = [self._getDateFromFilePath(l_file) for l_file in listdir(p_folder_path) if isfile(join(p_folder_path, l_file))]
            # e_result_to_return['list'] = [self.test(l_file) for l_file in listdir(p_folder_path) if isfile(join(p_folder_path, l_file))]
            e_result_to_return['bool'] = True
            e_result_to_return['text'] += "\n"
            e_result_to_return[
                'text'] += f">> Les fichiers '.{p_ext}' ont été correctment listés depuis le dossier '{p_folder_path}'"
            e_result_to_return['text'] += "\n"
            e_result_to_return['text'] += f">> dans : '{e_abs_path}'"
            print(f">> Files '.{p_ext}' correctly listed from '{e_abs_path}/{p_folder_path}'")
        except:
            print(">> Folder doesn't exist")
            e_result_to_return['text'] += "\n"
            e_result_to_return['text'] += f">> Erreur : le dossier '{p_folder_path}' n'existe plus !"
            e_result_to_return['text'] += "\n"
            e_result_to_return['text'] += f">> Merci de le recréer à la racine du programme :"
            e_result_to_return['text'] += "\n"
            e_result_to_return['text'] += f">> '{e_abs_path}'"
            print(f">> Error : 'scrapped' folder can't be find in '{e_abs_path}/{p_folder_path}'")
        finally:
            return e_result_to_return

    def _getDatesFromFilesList(self, p_files_list):
        return [self._getDateFromFilePath(l_file) for l_file in p_files_list]
