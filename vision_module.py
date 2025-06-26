from picamera2 import Picamera2
import time
import cv2
import numpy as np

class VisionModuleLive:

    def __init__(self):
        self.picam = Picamera2()
        self.picam.configure(self.picam.create_preview_configuration(main={"format": 'RGB888', "size": (640, 480)}))
        self.picam.start()
        time.sleep(2)
        print("Càmera inicialitzada per vídeo en directe.")

    def grau_torrat_frame(self, frame):
        # Convertir a HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
        H, S, V = cv2.split(hsv)

        # Detectar cinta blava
        mask_blava = (H > 90) & (H < 130) & (S > 100) & (V > 50)
        mask_blava = mask_blava.astype(np.uint8) * 255
        mask_blava = cv2.morphologyEx(mask_blava, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))

        # Invertim la màscara per detectar el pa
        mask_pa_candidates = cv2.bitwise_not(mask_blava)
        contours, _ = cv2.findContours(mask_pa_candidates, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        pa_detectat = False
        grau_torrat = None
        output = frame.copy()

        for contour in contours:
            area = cv2.contourArea(contour)
            if area < 5000:
                continue

            epsilon = 0.05 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            if len(approx) == 4:
                x, y, w, h = cv2.boundingRect(approx)
                aspect_ratio = w / h
                if 0.8 < aspect_ratio < 1.2:  # forma aproximada de quadrat
                    mask_pa = np.zeros_like(V)
                    cv2.drawContours(mask_pa, [approx], -1, 255, thickness=cv2.FILLED)

                    V_pa = V[mask_pa == 255]
                    if len(V_pa) > 0:
                        torrat = 1.0 - (np.mean(V_pa) / 255.0)
                        grau_torrat = torrat
                        pa_detectat = True

                        text = f"Grau de torrat: {torrat:.3f}"
                        cv2.putText(output, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                        cv2.drawContours(output, [approx], -1, (0, 255, 0), 3)
                    break  # només una peça de pa

        if not pa_detectat:
            cv2.putText(output, "No s'ha detectat pa", (30, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        return cv2.cvtColor(output, cv2.COLOR_RGB2BGR)  # per mostrar amb OpenCV

    def run_live_analysis(self):
        print("Prem 'q' per sortir.")
        while True:
            frame = self.picam.capture_array()
            resultat = self.grau_torrat_frame(frame)

            cv2.imshow("Anàlisi en directe", resultat)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()

if __name__ == "__main__":
    visor = VisionModuleLive()
    visor.run_live_analysis()

