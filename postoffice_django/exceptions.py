class UrlSettingNotDefined(Exception):
    def __init__(self):
        self.message = "POST_OFFICE_URL is not defined on settings"


class ConsumersSettingNotDefined(Exception):
    def __init__(self):
        self.message = "POST_OFFICE_CONSUMERS is not defined on settings"


class OriginHostSettingNotDefined(Exception):
    def __init__(self):
        self.message = 'ORIGIN_HOST is not defined on settings'
