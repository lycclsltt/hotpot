from decouple import config
import logger.logger as log
from engine.app_factory import AppFactory
import app_init

app_init.app_init()

#创建应用
app = AppFactory.createApp(__name__)

if __name__ == '__main__':
    log.info('app start, version:' + config('VERSION'))

    accessLogTag = False
    if config('ACCESS_LOG') == 'true':
        accessLogTag = True

    debugTag = False
    autoReloadTag = False
    if config('DEBUG') == 'true':
        debugTag = True
        autoReloadTag = True

    app.run(
        host='0.0.0.0',
        port=int(config('PORT')),
        debug=debugTag,
        access_log=accessLogTag,
        workers=int(config('WORKER_NUM')),
    )
