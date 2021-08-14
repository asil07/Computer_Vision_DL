from imutils import face_utils
from imutils.video import VideoStream
import dlib
import cv2

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

vs = VideoStream(0).start()

while True:

    frame = vs.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 1)
    for (i, rect) in enumerate(rects):

        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
        (x, y, w, h) = face_utils.rect_to_bb(rect)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 200, 0), 2)

        cv2.putText(frame, "Face #{}".format(i + 1), (x - 10, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Nuqtalar
        for (x, y) in shape:

            cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
    cv2.imshow("Natija", frame)

    if cv2.waitKey(10) & 0xFF == ord("q"):
        break
vs.stop()
cv2.destroyAllWindows()