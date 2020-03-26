import wtforms


class ValidAccessToken:
    def __init__(self, message=None):
        self.max = max
        if not message:
            message = "That lobby does not exist."
        self.message = message

    def __call__(self, form, field):
        lobbies = getattr(form, "lobbies", {})
        token = field.data
        if token not in lobbies:
            raise wtforms.ValidationError(self.message)


import string

name_characters = string.ascii_letters + string.digits

def has_valid_asciis(word):
    for char in word:
        if char not in name_characters:
            return False
    return True


class ValidAsciiValues:
    def __init__(self, message=None):
        if not message:
            message = (
                "Requested username contains invalid characters "
                "(must be letters or numbers)."
            )
        self.message = message

    def __call__(self, form, field):
        requested_player_id = field.data
        if not has_valid_asciis(requested_player_id):
            raise wtforms.ValidationError(self.message)
