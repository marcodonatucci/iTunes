from dataclasses import dataclass
from model.album import Album


@dataclass
class Connessione:
    album1: Album
    album2: Album
