class UrlSettingNotDefined(Exception):
    def __init__(self):
        self.message = 'POSTOFFICE_URL is not defined on settings'


class OriginHostSettingNotDefined(Exception):
    def __init__(self):
        self.message = 'ORIGIN_HOST is not defined on settings'


class BadTopicCreation(Exception):
    def __init__(self, topic_name):
        self.message = (
            f'Can not create topic. Topic no created: { topic_name }')


class BadPublisherCreation(Exception):
    def __init__(self, publisher):
        self.message = (
            f'Can not create publisher. Publisher not created: { publisher }')
