class UrlSettingNotDefined(Exception):
    def __init__(self):
        self.message = 'POSTOFFICE_URL is not defined on settings'


class OriginHostSettingNotDefined(Exception):
    def __init__(self):
        self.message = 'ORIGIN_HOST is not defined on settings'
