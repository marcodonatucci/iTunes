from dataclasses import dataclass


@dataclass
class Album:
    AlbumId: int
    Title: str
    ArtistId: int
    durata_totale: float

    def __hash__(self):
        return hash(self.AlbumId)
