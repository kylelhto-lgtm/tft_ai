from ultralytics import YOLO


def main():
    # -------------------------
    # CONFIG
    # -------------------------
    MODEL_PATH = "trained_models/one_cost.pt"
    INPUT_PATH = "generated_boards"   # image OR folder

    CONF_THRESH = 0.01

    # output folder
    OUTPUT_PROJECT = "inference_results"
    OUTPUT_NAME = "predictions"

    # -------------------------
    # LOAD MODEL
    # -------------------------
    model = YOLO(MODEL_PATH)

    # -------------------------
    # RUN INFERENCE
    # -------------------------
    results = model.predict(
        source=INPUT_PATH,
        conf=CONF_THRESH,

        # save annotated images
        save=True,

        # DO NOT OPEN WINDOWS
        show=False,

        # output location
        project=OUTPUT_PROJECT,
        name=OUTPUT_NAME,

        # overwrite existing folder
        exist_ok=True,

        # device
        device="cpu"
    )

    # -------------------------
    # PRINT DETECTIONS
    # -------------------------
    for r in results:
        print(f"\nImage: {r.path}")

        if r.boxes is None:
            continue

        for box in r.boxes:
            cls_id = int(box.cls[0])

            label = model.names[cls_id]

            conf = float(box.conf[0])

            xyxy = box.xyxy[0].tolist()

            print(
                f"{label} | "
                f"Conf={conf:.2f} | "
                f"Box={xyxy}"
            )

    print("\nDone.")
    print(f"Saved results to: {OUTPUT_PROJECT}/{OUTPUT_NAME}")


if __name__ == "__main__":
    main()