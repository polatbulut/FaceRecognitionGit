import cv2
from recognitionclass import SimpleFacerec
from PIL import Image
import io
import pymssql
import datetime
import argparse


# BLACKLISTED IMAGEDATA
black_data = ""


class Main:
    def __init__(self, flag):
        self.faceRec = SimpleFacerec()

        server = ''
        database = ''
        username = ''
        password = ''

        self.meyer_database = pymssql.connect(server=server, database=database, user=username, password=password)
        self.meyer_cursor = self.meyer_database.cursor()

        meyer_query_complete = f"SELECT ###, ### FROM ### WHERE ### NOT LIKE {black_data} ORDER BY ###"
        meyer_query = "SELECT sf.###, sf.### FROM ### sf WHERE sf.### IN (SELECT s.ID FROM ### s WHERE (s.### = # OR s.### = #))"
        if flag:
            self.meyer_cursor.execute(meyer_query_complete)
        else:
            self.meyer_cursor.execute(meyer_query)

        self.meyer_blob_data_list = self.meyer_cursor.fetchall()

        self.meyer_dict = {}
        for sicilid, blob_data in self.meyer_blob_data_list:
            blob_stream = io.BytesIO(blob_data)
            image = Image.open(blob_stream)
            self.meyer_dict[sicilid] = image

        self.faceRec.load_encoding_images(self.meyer_dict)

    def commit_to_database(self, input_name, input_time, ship_id, device_id):
        query = f"UPDATE ### SET Datetime = '{input_time}', LocationID = '{ship_id}', DeviceID = '{device_id}' WHERE SicilID = {input_name}"
        print("\n" + query)

        self.meyer_cursor.execute(query)
        self.meyer_database.commit()

    def process(self, camera_id, tolerance, location, device):

        if camera_id.isdigit():
            camera_id = int(camera_id)

        camera = cv2.VideoCapture(camera_id)

        known_names = []
        last_execution_time = datetime.datetime.now()

        while True:
            ret, frame = camera.read()
            face_location, face_name = self.faceRec.detect_known_faces(frame, tolerance)

            for face_loc, name in zip(face_location, face_name):
                y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
                current_time = datetime.datetime.now()
                elapsed_time = (current_time - last_execution_time).total_seconds()

                if name != "Unknown":
                    if name not in known_names:
                        known_names.append(name)

                        current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

                        self.commit_to_database(name, current_datetime, location, device)

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


def passer():
    parser = argparse.ArgumentParser(description="Face recognition application")
    parser.add_argument("--test", type=int, default=1, help="Test flag (0 or 1)")
    parser.add_argument("--c1", type=str, default="0", help="Camera 1 ID")
    parser.add_argument("--t", type=float, default=0.48, help="Tolerance")
    parser.add_argument("--location", default="1", help="Location")
    parser.add_argument("--device", default="1", help="Device")

    args = parser.parse_args()

    if args.test == 1:
        app = Main(False)
    else:
        app = Main(True)

    app.process(args.c1, args.t, args.location, args.device)


if __name__ == "__main__":
    passer()
