from remy.domain.topic_handler import TopicHandler
from remy.domain.constants import ENTITY_IDENTIFIERS
from remy.domain.storage.local_storage import LocalStorage
from remy.domain.service_locater import ServiceLocater

def get_service_locator() -> ServiceLocater:

    local_storage = LocalStorage()

    service_locater = ServiceLocater()
    service_locater.add_entity(ENTITY_IDENTIFIERS.LOCAL_STORAGE, local_storage)

    topic_handler = TopicHandler(**service_locater.misc_mapping)
    service_locater.add_entity(ENTITY_IDENTIFIERS.TOPIC_HANDLER, topic_handler)

    return service_locater

