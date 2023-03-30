class ImgResponse:

    def __init__(self, *, created: int, data: list[dict]):
        self.created: int = created
        self.data: list[dict] = data

    @property
    def url(self) -> str | None:
        return self.data[0].get('url')

    @classmethod
    def from_json(cls, json: dict[str]):
        return cls(**json)

    def to_json(self) -> dict:
        return vars(self)

    def __repr__(self) -> str:
        return f'ImgResponse(data={self.data}, create={self.created})'
