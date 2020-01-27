class UrlSettingNotDefined(Exception):
    def __init__(self):
        self.message = "POST_OFFICE_URL is not defined on settings"


class ConsumersSettingNotDefined(Exception):
    def __init__(self):
        self.message = "POST_OFFICE_CONSUMERS is not defined on settings"
