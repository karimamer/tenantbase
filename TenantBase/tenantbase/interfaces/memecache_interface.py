from pymemcache.client.base import Client

HOST = "localhost"
PORT = 11211
CLIENT = Client((HOST, PORT))


def set_memecahce(key, value):
    CLIENT.set(key, value)
    return None


def get_from_memcahce(k):
    result = CLIENT.get(k)
    return result


def delete_from_memcahce(k):
    CLIENT.delete(k)
    return None
