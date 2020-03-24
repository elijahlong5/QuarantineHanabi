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
