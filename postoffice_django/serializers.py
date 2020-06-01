class MessagesSerializer:
    fields = ['id', 'topic', 'payload', 'attributes', 'bulk']

    def serialize(self, messages):
        return [self._serialize_fields(message) for message in messages]

    def _serialize_fields(self, message):
        return {field: getattr(message, field, None) for field in self.fields}
