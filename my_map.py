class MyMap:

    def __init__(self):
        self._keys = []
        self._values = []

    def put(self, key, value):
        if key in self._keys:
            self._values[self._keys.index(key)] = value
        else:
            self._keys.append(key)
            self._values.append(value)

    def get(self, key):
        if key in self._keys:
            return self._values[self._keys.index(key)]
        return None

    def remove(self, key):
        if key in self._keys:
            idx = self._keys.index(key)
            self._keys.pop(idx)
            self._values.pop(idx)

    def keys(self):
        return self._keys

    def values(self):
        return self._values
