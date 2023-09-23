class RecordFetchDTO:

    def __init__(self, **kwargs):
        self.topic = kwargs.get('topic')
        self.category = kwargs.get('category')
        self.sub_category = kwargs.get('sub_category')
