class config:
    host = 'localhost'
    port = 8088
    debug = True
    web_hook_url_path = '.\\db\\webhook_url.txt'
    file_tracking_path = '.\\db\\file_tracking.txt'

class configdb:
    db_path = ''
    db_names = 'filemonitor.db'
    table_names = {
        'filepath': 'filepath',
        'webhook': 'webhook',
        'filepath_webhook': 'filepath_webhook'
    }


