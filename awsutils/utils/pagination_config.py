class PaginationConfig:
    def __init__(self, 
        max_items = 10,
        page_size = 1,
        starting_token = None
    ) -> None:
        self.max_items = max_items
        self.page_size = page_size
        self.starting_token = starting_token

    def get_dict(self):
        return {
            'MaxItems': self.max_items,
            'PageSize': self.page_size,
            'StartingToken': self.starting_token
        }