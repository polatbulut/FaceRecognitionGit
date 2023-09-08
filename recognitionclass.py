import face_recognition
import cv2
import numpy as np
import os
import glob


class SimpleFacerec:

    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.frame_resizing = 0.25

    def load_encoding_images(self, image_dict):
        count = 0
        for idx, image in image_dict.items():
            rgb_img = image.convert("RGB")
            np_img = np.array(rgb_img)

            img_encodings = face_recognition.face_encodings(np_img)

            if len(img_encodings) > 0:
                img_encoding = img_encodings[0]

                self.known_face_encodings.append(img_encoding)
                self.known_face_names.append(str(idx))
            else:
                count += 1
                print(f"No face found in image {idx}")

        print(f"{len(image_dict) - count} Encoding images loaded")

    def detect_known_faces(self, frame):
        small_frame = cv2.resize(frame, (0, 0), fx=self.frame_resizing, fy=self.frame_resizing)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"
            """
            # # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = self.known_face_names[first_match_index]
                face_names.append(name)
            """
            # Use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]
            face_names.append(name)

        face_locations = np.array(face_locations)
        face_locations = face_locations / self.frame_resizing
        return face_locations.astype(int), face_names
