class QueryObject:
    def __init__(self, data: dict):
        self.data = data

    def str(self):
        string = ''
        # Loop through data to create a string to parse into a http request
        for key, value in self.data.items():
            string += '&{0}={1}'.format(key, value)
        return string
