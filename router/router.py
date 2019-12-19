from controller.example import Hello, GetParam, Page, ReadConfig, OrmSelect

routers = {
    '/hello': Hello,
    '/get_param': GetParam,
    '/page': Page,
    '/read_config': ReadConfig,
    '/orm/select': OrmSelect,
}
