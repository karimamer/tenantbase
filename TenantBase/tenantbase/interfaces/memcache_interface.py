from pymemcache.client.base import Client

HOST = "localhost"
PORT = 11211
CLIENT = Client((HOST, PORT))


def set_memcahce(key, value):
    CLIENT.set(key, value)
    return None


def get_from_memcahce(key):
    result = CLIENT.get(key)
    return result


def delete_from_memcahce(key):
    CLIENT.delete(key)
    return None
