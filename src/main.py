from fastapi import FastAPI, UploadFile, Response, HTTPException
import numpy as np
from PIL import Image
from io import BytesIO
import uvicorn

app = FastAPI()

CVD_MATRICES = {
    "normal": np.array([
        [1.000, 0.000, 0.000],
        [0.000, 1.000, 0.000],
        [0.000, 0.000, 1.000]
    ]),
    "protanopia": np.array([
        [0.567, 0.433, 0.000],
        [0.558, 0.442, 0.000],
        [0.000, 0.242, 0.758]
    ]),
    "deuteranopia": np.array([
        [0.625, 0.375, 0.000],
        [0.700, 0.300, 0.000],
        [0.000, 0.300, 0.700]
    ]),
    "tritanopia": np.array([
        [0.950, 0.050, 0.000],
        [0.000, 0.433, 0.567],
        [0.000, 0.475, 0.525]
    ])
}


def simulate_cvd(image_path, cvd_type, severity):
    if cvd_type not in CVD_MATRICES:
        raise ValueError(f"Invalid CVD type. Choose from {list(CVD_MATRICES.keys())}.")

    if not (0 <= severity <= 100):
        raise ValueError("Severity must be between 0 and 100.")

    img = Image.open(image_path).convert("RGB")
    img_array = np.array(img, dtype=np.float32) / 255.0

    transformation_matrix = CVD_MATRICES[cvd_type]

    severity_factor = severity / 100.0
    transformed_array = np.dot(img_array, transformation_matrix.T)
    result_array = (1 - severity_factor) * img_array + severity_factor * transformed_array

    result_array = np.clip(result_array, 0, 1) * 255.0
    result_image = Image.fromarray(result_array.astype(np.uint8))

    return result_image


@app.post("/image")
async def create_upload_file(image: UploadFile):
    image_path = image.file
    cvd_type = "protanopia"  # Choose from "normal", "protanopia", "deuteranopia", "tritanopia"
    severity = 100

    try:
        img = simulate_cvd(image_path, cvd_type, severity)

        buffer = BytesIO()
        img.save(buffer, format="JPEG")
        buffer.seek(0)

        return Response(content=buffer.read(), media_type="image/jpeg")
    except Exception as e:
        print(f"Error: {e}")

    raise HTTPException(status_code=500, detail="Internal server error")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
