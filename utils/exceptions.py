class PublicationAlreadyExists(Exception):
    def __init__(self, message="Publication already exists"):
        self.message = message
        super().__init__(self.message)


class RecommendationAlreadyExists(Exception):
    def __init__(self, message="Recommendation already exists"):
        self.message = message
        super().__init__(self.message)
