import cv2
from recognitionclass import SimpleFacerec
from PIL import Image
import io
import pymssql
import datetime
import mysql.connector

# BLACKLISTED IMAGEDATA
black_data = "0xFFD8FFE000104A46494600010100000100010000FFDB0084000906070D0D0D0D0E0E0D100F0D0E0D0D0D0D0D0E0F0F0F0E0E0D15121616151D1515181E2820181A251B151321322125292B2E2E2E171F3338332C37282D2E2B010A0A0A0505050E05050E2B1913192B2B2B2B2B2B2B2B2B2B2B2B2B2B2B2B2B2B2B2B2B2B2B2B2B2B2B2B2B2B2B2B2B2B2B2B2B2B2B2B2B2B2B2B2B2B2B2B2B2BFFC000110800E100E103012200021101031101FFC4001B00010100030101010000000000000000000002010306040507FFC4003F10000202000207030807060700000000000001020304110506122131519122526113417181A1B1C1D114233233627292424363B2E1F1245382A2C2D2F0FFC40014010100000000000000000000000000000000FFC40014110100000000000000000000000000000000FFDA000C03010002110311003F00FD6400000000000000001900003206019C801806464060C19006019006000000000000000000000000000000320003200646723C1A5B4A430D1DFDAB24BB30F0E6F9203DC7CEC5E9BC3559ADBDB9776BDFEDE072D8DD2375EFB737979A0B7417A8F201F7B11ACD63FBBAE315CE4DC9FC0F0D9A6B152FDF35F95463EE47CF007B5696C57F9F3EA7A68D61C4C7ED38D8B94A293EA8F9200EC747E9DA6E6A32FAB9BDC949E716FC247D5C8FCE4FB382D61B6B8A84A2AC4B726DB52CBD3E703AC3078345697AF12DC765C26967B2DE79AF067D1C809064C018064C00000000000000000000C8000A4060A4824524068C5DF1AAB9D92E108B79737E6470589BE56CE564DE7293CDF8782F03A6D6FBB66AAEB5FB73DA7E88AF9B5D0E5000000000000000000DB85C44AAB216478C1E7E9E6BA1FA0C24A51525C249497A19F9C9DD680B36F094B7C545C7F4C9AF8203D8D182DA30D0100C980300C98000000000000032019008A482292009149048B480E4B5C9FD6D2B95727D65FD0E78E8B5D2395B4BE75B5D25FD4E74000000000000000001DBEAC2FF000757A6CFE791C41DF6AFD7B383A1738397EA937F103D8D12D1B5A21A035B30CB689604832600C000000001930640C994611480CA29230916901948B48C245A40733AED576689F294E1D526BDCCE4CEE35CB67E88B3E3E5A1B1E9C9E7ECCCE1C000000000000000001FA468B86586A17F0A1EE3F373F46D0B746CC2D128BFDDC62FC251DCFDC07A5A21A36B443406B68866C68960432596C96060C193000000642065019452308A40522D2251B101948B48C22D01C66BB5D277D75FEC46A534BF14A524DFFB51CE1D26BC432BE9973A767A49FF00D8E6C000000000000000001D46A4625ED5D4B7D97156457269E4FDEBA1CB9D06A5473C4CDF2A65ED680ECDA21A36B21A035344336B46B6043219B190C09660A6600C0000C994611480A452251680B45A251680A45A251480E635EA8CEBA2CEECE55BFF0052CD7F2B38F3F4ED2982589A2CA9EEDA5D97DD9ADE9F53F3DC668CC450DF94AA4927F6D26E1FA96E03C6000000000000000075BA8B43CB116BE0F62B8FAB36FF00E273BA3F46DF8996CD5072CBED49EE847D2CFD0B45602385A215279B59B94BBD37BDBFFDC80F4B219B190C0D6C866C64303532596C8604B30659800000328CA308CA02D168845A02D1B1108B405A29128A40523C1A7E1B583C4AE554E5D167F03DE68C757B74DD1EF55647AC5A03F2C010000000000000CB3DCB8BDC80FD3342E1A34E1A9825976232978CA4B379F53DACC571D98C63CA2974465812C965B21810CD6CD8C8606B6432D90C0964B2992C00000CA29128A40523644D68D9102D168845A02D168845A0321ACD65CC1903F35D39A2E784B5C5EFAE4DBAA7CE3C9F8A3E71D46B469CA2F84E88C25270B375ADA51528BC9E5CFCE8E5C0000000001D06A9E8877D8AF9AFAAAA59AFC762E1EA5B99CF9D5685D66A30F4574CAA9AD84D3947269B6DB6F2E3E703B061988C9349A79A6934D7068CB02592CA64B035B2246C66B901AD92CB64302192CA64B00000328A44A3280B45A211680D88B46B89B10168A44A139C62B6A4D462B8B9349750361F2B59348FD1B0D269E56599D75F34DADEFD4BE04E2B59307566BCAEDCB9569CBDBC3DA717A6749CF176BB25BA296CD70EEC7E60780000000000000000775A9DA47CAD1E464FB74EE59F175BE1D38743EFB3F2FD1F8D9E1ED8DB0FB51E29F0945F14CEDB09ACF84B32DA9BAA4FCD34F2CFF32DC07D96433155D0B16D42519479C5A6BD865810C865B35B02190CB64302592CA64B0000008A44A290148B4423C18CD3987A776DEDCBBB5EFEAF8203EB234E2F1F4D0B3B6C51E4B8C9FA12DE7218ED64C4599AAF2AA3F877CFF57C8F8D293936DB6DBDEDB79B7EB03A8C7EB73DF1C3D797F12CDEFD51F99CEE2F196DEF6ADB2537E6CDEE5E85C11A000000000000000000000000001B70F88B2A96D5739425CE2F2FEE7DFC06B6591C95F0562EFC728CFA707EC39B007E8B82D2987C47DDD89CBB8FB335EA67A647E628FAD81D60C4559272F290EECF7BF54B881DA3259F2F07AC187B72527E4A5CA7C33F09703E9669ACD6F4F835C1818660CB30000004596461172949462B8B7B923E16375912CD530CFF001CF87AA27CFD3DA41DD6B827F575B718AE725C5B3E581EAC5690BEEFBCB24D7756E8F4479400000000000000000000000000000000000000000006FC3632DA7EEEC947C13ECF4E0680074183D6596E574335DF86E7EB47DFC3E2216C54E12528BF3AF33F1E47007B345E3A587B1493EC369591F338FCC0EDC1A7E955F7D00385BDE739FE797BC82AC7DA97A5FBC90000000000000000000000000000000000000000000000000018007DDF2F2F0078BCB4BC3A003C0CC00000000000000000000000000000000000000000000000000000005F9497304000000000000000000000000000000000000000000000000000000000000003FFD9"


class Main:
    def __init__(self):
        self.faceRec = SimpleFacerec()
        self.camera_count = count_connected_cameras()

        l_server = 'localhost'
        l_database = 'personal_data'
        l_username = 'root'
        l_password = 'rootroot'
        self.local_database = mysql.connector.connect(host=l_server, database=l_database, user=l_username, password=l_password)
        self.local_cursor = self.local_database.cursor()

        server = '192.168.20.236'
        database = 'BESIKTAS14120_Meyer'
        username = 'stajyer'
        password = 's1213145!'
        self.meyer_database = pymssql.connect(server=server, database=database, user=username, password=password)
        self.meyer_cursor = self.meyer_database.cursor()
        # meyer_query = f"SELECT sicilid, fotoimage FROM SicilFoto WHERE fotoimage NOT LIKE {black_data} ORDER BY sicilid"
        meyer_query = "SELECT sf.sicilid, sf.fotoimage FROM SicilFoto sf WHERE sf.sicilid IN (SELECT s.ID FROM Sicil s WHERE (s.Bolum = 6 OR s.Bolum = 8 OR s.Bolum = 9 OR s.Bolum = 11 OR s.Bolum = 14 OR s.Bolum = 13  OR s.Bolum = 14 OR s.Bolum = 42) AND CikisTarih IS NULL)"
        self.meyer_cursor.execute(meyer_query)
        self.meyer_blob_data_list = self.meyer_cursor.fetchall()
        self.local_cursor.execute("SELECT sicilid, fotoimage FROM sicilfoto WHERE sicilid = 0")
        stajyer = self.local_cursor.fetchall()
        self.meyer_blob_data_list.append(stajyer[0])
        self.meyer_dict = {}
        for sicilid, blob_data in self.meyer_blob_data_list:
            blob_stream = io.BytesIO(blob_data)
            image = Image.open(blob_stream)
            self.meyer_dict[sicilid] = image

        self.load_images()

    def load_images(self):
        self.faceRec.load_encoding_images(self.meyer_dict)
        self.process(0)

    def commit_to_database(self, input_name, input_time, ship_id, device_id):
        query = f"UPDATE bsy_SicilYuzOkutmaLog SET Datetime = '{input_time}', MerdivenID = '{ship_id}', DeviceID = '{device_id}' WHERE SicilID = {input_name}"
        print("\n" + query)
        self.meyer_cursor.execute(query)
        self.meyer_database.commit()

    def process(self, camera_id):
        ship_id = input("Ship ID: ")
        device_id = input("Device ID: ")
        camera = cv2.VideoCapture(camera_id)
        known_names = []
        last_execution_time = datetime.datetime.now()
        while True:
            ret, frame = camera.read()
            face_location, face_name = self.faceRec.detect_known_faces(frame)

            for face_loc, name in zip(face_location, face_name):
                y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
                current_time = datetime.datetime.now()
                elapsed_time = (current_time - last_execution_time).total_seconds()
                if name != "Unknown":
                    if name not in known_names:
                        known_names.append(name)
                        current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                        self.commit_to_database(name, current_datetime, ship_id, device_id)
                        cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)
                if elapsed_time >= 3:
                    if name in known_names:
                        known_names.remove(name)
                    last_execution_time = datetime.datetime.now()

            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1)
            if key == 27:
                break
        camera.release()
        cv2.destroyAllWindows()


def count_connected_cameras():
    index = 0
    num_connected_cameras = 0
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.isOpened():
            break
        num_connected_cameras += 1
        cap.release()
        index += 1
    return num_connected_cameras


if __name__ == "__main__":
    app = Main()
