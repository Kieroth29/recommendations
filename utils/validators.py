def publication_creation_payload_is_valid(data) -> bool:
    fields = [
        {"name": "class_topic", "type": str},
        {"name": "title", "type": str},
        {"name": "venue", "type": str},
        {"name": "url", "type": str},
        {"name": "authors", "type": list},
        {"name": "num_citations", "type": int},
        {"name": "pub_year", "type": int}
    ]

    for field in fields:
        if field["name"] not in data:
            return False

        if not isinstance(data[field["name"]], field["type"]):
            return False

    return True


def recommendation_creation_payload_is_valid(data) -> bool:
    fields = [
        {"name": "class_topic", "type": str},
        {"name": "title", "type": str},
        {"name": "venue", "type": str},
        {"name": "url", "type": str},
        {"name": "authors", "type": list},
        {"name": "pub_year", "type": int}
    ]

    for field in fields:
        if field["name"] not in data:
            return False

        if not isinstance(data[field["name"]], field["type"]):
            return False

    return True

