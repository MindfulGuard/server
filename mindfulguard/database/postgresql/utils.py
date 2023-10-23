from uuid import UUID


def serialize_uuid(obj):
    if isinstance(obj, UUID):
        return str(obj)
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')