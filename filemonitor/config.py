class config:
    host = 'localhost'
    port = 8088
    debug = True
    log_path = "log_filemonitor.txt"
    log_format = "%(levelname)s %(name)s %(message)s"

class configdb:
    db_path = ''
    db_name = 'filemonitor.db'
    table_names = {
        'filepath': 'filepath',
        'webhook': 'webhook',
        'filepath_webhook': 'filepath_webhook'
    }

