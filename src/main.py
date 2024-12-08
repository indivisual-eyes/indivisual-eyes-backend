from typing import Annotated
from fastapi import FastAPI, UploadFile, Response, HTTPException, Form, File
from io import BytesIO
import uvicorn

from src.algorithms.simulate_cvd.simulate_cvd import simulate_cvd
from src.algorithms.k_means_monochrome.k_means_monochrome import k_means_monochrome

app = FastAPI()


@app.post('/image')
async def create_upload_file(image: Annotated[UploadFile, File()], cvd_type: Annotated[str, Form()]):
    image_path = image.file

    try:
        if cvd_type == 'Achromatopsia':
            img = k_means_monochrome(image_path, 6)
        else:
            img = simulate_cvd(image_path, cvd_type.lower(), 100)

        buffer = BytesIO()
        img.save(buffer, format='JPEG')
        buffer.seek(0)

        return Response(content=buffer.read(), media_type='image/jpeg')
    except Exception as e:
        print(f'Error: {e}')

    raise HTTPException(status_code=500, detail='Internal server error')


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
