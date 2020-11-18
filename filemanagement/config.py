class config:
    host = 'localhost'
    port = 8080
    debug = True
    log_path = "./log.txt"
    log_format = "%(levelname)s %(name)s %(message)s"

class configdb:
    db_name = 'filemanagement.db'
    db_path = ''
    table_names = {
        'fileinfo': 'fileinfo'
    }


