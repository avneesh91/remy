import datetime

class RecommendationDTO:

    def __init__(self, **kwargs):
        self._revision_topic_dict = {}
        self._revision_topic_recommendation_list_dict = {}

    def add_topic_data(self, topic_name, topic_dto_list):
        self._revision_topic_dict[topic_name] = topic_dto_list

    def update_revision_date_confirmation(self, sheet):
        revision_timestamp = datetime.datetime.utcnow()

        for values in self._revision_topic_recommendation_list_dict.values():
            for topic_dto in values:
                topic_dto.update_revised_on(revision_timestamp, sheet)

    def get_recommendation_list_for_printing(self, topic_name, ):
        self._revision_topic_dict
