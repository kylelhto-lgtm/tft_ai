from ultralytics import YOLO
from pathlib import Path
import shutil
import torch


def main():
    # =========================
    # CONFIG
    # =========================
    DATA_PATH = "yolo_dataset/data.yaml"
    BASE_MODEL = "yolo26n.pt"   # or yolov8n.pt / yolov11n.pt etc.

    EPOCHS = 100
    IMG_SIZE = 640
    BATCH = 16
    device = 0 if torch.cuda.is_available() else "cpu"  # "cpu" if no GPU

    RUN_NAME = "tft_champion_detector"

    SAVE_DIR = Path("trained_models")
    SAVE_DIR.mkdir(exist_ok=True, parents=True)

    # =========================
    # LOAD MODEL
    # =========================
    model = YOLO(BASE_MODEL)

    # =========================
    # TRAIN
    # =========================
    results = model.train(
        data=DATA_PATH,
        epochs=EPOCHS,
        imgsz=IMG_SIZE,
        batch=BATCH,
        device = 0 if torch.cuda.is_available() else "cpu",
        project="runs/train",
        name=RUN_NAME,
        patience=20,
        save=True,
        val=True,
        workers=4
    )

    # =========================
    # PATHS TO TRAINED WEIGHTS
    # =========================
    run_dir = Path("runs/train") / RUN_NAME
    best_model = run_dir / "weights" / "best.pt"
    last_model = run_dir / "weights" / "last.pt"

    print("\nTraining complete!")
    print(f"Best model: {best_model}")
    print(f"Last model: {last_model}")

    # =========================
    # COPY MODELS TO SAFE FOLDER
    # =========================
    saved_best = SAVE_DIR / "tft_best.pt"
    saved_last = SAVE_DIR / "tft_last.pt"

    shutil.copy(best_model, saved_best)
    shutil.copy(last_model, saved_last)

    print("\nModels saved to:")
    print(saved_best)
    print(saved_last)

    # =========================
    # OPTIONAL: EXPORT FOR DEPLOYMENT
    # =========================
    export_dir = SAVE_DIR / "exported"
    export_dir.mkdir(exist_ok=True)

    model.export(format="onnx", project=str(export_dir))
    model.export(format="torchscript", project=str(export_dir))

    print("\nExport complete (ONNX + TorchScript).")


if __name__ == "__main__":
    main()