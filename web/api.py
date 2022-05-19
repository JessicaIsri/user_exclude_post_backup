from flask import Flask, request
from connection.mysql_querys import insert_in_blacklist as isb
from connection.mysql_querys import backup_database, list_backups, restore_database

app = Flask(__name__)


@app.route("/new_blacklist", methods=['POST'])
def insert_in_blacklist():
    json = request.json
    name = json.get('name')
    email = json.get('email')
    if name is not None and email is not None:
        return isb(name, email)
    else:
        return "Nome ou email não encontrado", 404


@app.route("/backup", methods=['POST'])
def backup_databases():
    return backup_database()


@app.route("/list_backups")
def list_backup():
    return list_backups()


@app.route("/restore", methods=['POST'])
def restore_databases():
    json = request.json
    if json.get('backup_file') is not None:
        return restore_database(json.get('backup_file'))
    else:
        return 'Arquivo do backup ausente', 400


if __name__ == "__main__":
    app.run()