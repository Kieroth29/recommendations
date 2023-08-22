class PublicationAlreadyExists(Exception):
    def __init__(self, resource: str, message="Publication already exists"):
        self.message: str = message
        self.resource: str = resource
        super().__init__(self.message)


class RecommendationAlreadyExists(Exception):
    def __init__(self, resource: str, message="Recommendation already exists"):
        self.message: str = message
        self.resource: str = resource
        super().__init__(self.message)
