from database.DB_connect import DBConnect
from model.album import Album
from model.connessione import Connessione


class DAO:

    @staticmethod
    def getAlbum(durata):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT a.AlbumId , a.Title , a.ArtistId , SUM(t.Milliseconds) / 60000 as durata_totale
FROM album a, track t 
WHERE a.AlbumId = t.AlbumId 
GROUP BY t.AlbumId 
HAVING (SUM(t.Milliseconds) / 60000) > %s"""
            cursor.execute(query, (durata,))
            for row in cursor:
                result.append(Album(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getConnessioni(durata, idMap):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT distinct a1.AlbumId as album1, a2.AlbumId as album2
FROM (SELECT a.AlbumId , a.Title , a.ArtistId , SUM(t.Milliseconds) as durata_totale
FROM album a, track t 
WHERE a.AlbumId = t.AlbumId 
GROUP BY t.AlbumId 
HAVING (SUM(t.Milliseconds) / 60000) > %s)as a1, (SELECT a.AlbumId , a.Title , a.ArtistId , SUM(t.Milliseconds) as durata_totale
FROM album a, track t 
WHERE a.AlbumId = t.AlbumId 
GROUP BY t.AlbumId 
HAVING (SUM(t.Milliseconds) / 60000) > %s)as a2, track t1, track t2, playlisttrack p1, playlisttrack p2 
WHERE a1.AlbumId = t1.AlbumId and a2.AlbumId = t2.AlbumId and a1.AlbumId < a2.AlbumId and p1.PlaylistId = p2.PlaylistId and t1.TrackId = p1.TrackId and t2.TrackId = p2.TrackId"""
            cursor.execute(query, (durata, durata))
            for row in cursor:
                result.append(Connessione(idMap[row['album1']], idMap[row['album2']]))
            cursor.close()
            cnx.close()
        return result
