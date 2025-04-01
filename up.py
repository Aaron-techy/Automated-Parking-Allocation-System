def prg():
    import cv2
    import pytesseract
    import os

    # Set the Tesseract path (Modify for your OS)
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    def detect_plate():
        """ Detects number plates and saves the extracted image """
        harcascade = "model/haarcascade_russian_plate_number.xml"

        # Ensure the cascade file exists
        if not os.path.exists(harcascade):
            print("Error: Haarcascade file not found!")
            return None

        plate_cascade = cv2.CascadeClassifier(harcascade)
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("Error: Could not open webcam")
            return None

        cap.set(3, 640)  # Width
        cap.set(4, 480)  # Height

        min_area = 500
        count = 0

        # Ensure output directory exists
        output_dir = "plates"
        os.makedirs(output_dir, exist_ok=True)

        img_roi = None  # Initialize img_roi to prevent errors

        while True:
            success, img = cap.read()
            if not success:
                print("Failed to capture image")
                break

            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            plates = plate_cascade.detectMultiScale(img_gray, 1.1, 4)

            for (x, y, w, h) in plates:
                area = w * h
                if area > min_area:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(img, "Number Plate", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 2)

                    img_roi = img[y:y + h, x:x + w]

                    # Show extracted plate
                    if img_roi is not None:
                        cv2.imshow("ROI", img_roi)

            cv2.imshow("Result", img)

            # Save the detected plate when 's' is pressed
            if cv2.waitKey(1) & 0xFF == ord('s') and img_roi is not None:
                file_path = os.path.join(output_dir, f"scanned_img_{count}.jpg")
                cv2.imwrite(file_path, img_roi)
                print(f"Saved: {file_path}")

                cv2.rectangle(img, (0, 200), (640, 300), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, "Plate Saved", (150, 265), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255), 2)
                cv2.imshow("Result", img)
                cv2.waitKey(500)

                count += 1  # Increment count after saving
                cap.release()
                cv2.destroyAllWindows()
                return file_path  # Return the path of the saved image

        cap.release()
        cv2.destroyAllWindows()
        return None

    def ocr_core(image_path):
        """ Extract text from the saved number plate image """
        img = cv2.imread(image_path)
        if img is None:
            print("Error: Unable to load image for OCR")
            return ""

        # Convert image to grayscale
        def get_grayscale(image):
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Noise removal
        def remove_noise(image):
            return cv2.medianBlur(image, 5)

        # Adaptive Thresholding for better OCR accuracy
        def adaptive_thresholding(image):
            return cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

        # Apply preprocessing
        img = get_grayscale(img)
        img = adaptive_thresholding(img)
        img = remove_noise(img)

        # Resize image to improve OCR accuracy
        img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

        # Perform OCR with config
        custom_config = r'--oem 3 --psm 7'
        text = pytesseract.image_to_string(img, config=custom_config).strip()

        return text

    # Run the detection and OCR
    image_path = detect_plate()
    if image_path:
        print("Extracted Text:")
        extracted_text = ocr_core(image_path)
        print(extracted_text)
        return(extracted_text)
