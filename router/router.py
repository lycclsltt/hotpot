from controller.example import Hello, GetParam, Page, ReadConfig, OrmSelect, Status, Json

routers = {
    '/hello': Hello,
    '/get_param': GetParam,
    '/page': Page,
    '/read_config': ReadConfig,
    '/orm/select': OrmSelect,
    '/status': Status,
    '/return.json': Json,
}
