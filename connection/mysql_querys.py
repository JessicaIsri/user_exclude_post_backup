import os
import pathlib
import time
from datetime import date

from connection.mysql_connection import blacklist_cursor, blacklist_connection, persistent_data_cursor, \
    persistent_data_connection, persistent_data, blacklist, base_dir
from os import system

cwd = pathlib.Path(__file__).parent.parent
base_dir = base_dir
backup_dir = os.path.join('D:', 'backupd_mysl', f'{persistent_data.get("database")}_{date.today()}.sql')
bl_backup_dir = os.path.join('D:', 'backupd_mysl', f'{blacklist.get("database")}.sql')


query_backup = f'mysqldump -u {persistent_data.get("user")} {persistent_data.get("database")} > {backup_dir}'


bl_query_backup = f'mysqldump -u {blacklist.get("user")} {blacklist.get("database")} > {bl_backup_dir}'
bl_query_restore = f'mysql -u {blacklist.get("user")} {blacklist.get("database")} < {bl_backup_dir}'


def list_backups():
    backups = []
    files_in_dir = os.listdir(base_dir)
    for file in files_in_dir:
        data_file = {'name': file, 'saved_at': time.ctime(os.path.getmtime(os.path.join(base_dir, file)))}
        backups.append(data_file)
    return {'backups': backups}, 200


def insert_in_blacklist(name, email):
    query_to_search = f"select id from users where name = '{name}' and email = '{email}';"
    persistent_data_cursor.execute(query_to_search)
    result = persistent_data_cursor.fetchall()
    result = [str(x[0]) for x in result]
    if len(result) < 1:
        return 'Nenhum usuário encontrado', 404
    else:
        query_to_delete = f"delete from users where id = {result[0]};"
        persistent_data_cursor.execute(query_to_delete)
        persistent_data_connection.commit()
        query_to_insert = f'insert into black_list (id_exclude) values ({result[0]})'
        blacklist_cursor.execute(query_to_insert)
        blacklist_connection.commit()
        return "Usuário deletado", 200


def get_ids_blacklist():
    query = 'SELECT id_exclude from black_list;'
    blacklist_cursor.execute(query)
    result = blacklist_cursor.fetchall()
    result = [str(x[0]) for x in result]
    ids_to_remove = ','.join(result)
    return ids_to_remove


def remove_ids(ids_to_remove: str):
    query = f'DELETE from users where id in ({ids_to_remove})'
    persistent_data_cursor.execute(query)
    persistent_data_connection.commit()
    return 'Foram excluidos {} registros! Banco pronto para uso !'.format(persistent_data_cursor.rowcount)
    # print()


def backup_database():

    system(query_backup)
    return 'backup realizado', 200


def restore_database(backup_file):
    backups = os.listdir(base_dir)
    if backup_file in backups:
        query_restore = f'mysql -u {persistent_data.get("user")} {persistent_data.get("database")} < {os.path.join(base_dir, backup_file)}'
        system(query_restore)
        print('Aplicando blacklist ...')
        ids_to_remove = get_ids_blacklist()

        return remove_ids(ids_to_remove), 200
    else:
        return 'Backup não encontrado', 404
