class ServiceLocater:

    def __init__(self, **kwargs):
        self.misc_mapping = {}

    def add_entity(self, identifier, instance):
        self.misc_mapping[identifier] = instance

