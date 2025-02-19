import os
from typing import Annotated
from fastapi import FastAPI, UploadFile, Response, HTTPException, Form, File
from io import BytesIO
import uvicorn
from src.algorithms.plane_rotation.plane_rotation import plane_rotation
from src.algorithms.k_means_monochrome.k_means_monochrome import k_means_monochrome
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()


@app.post('/image')
async def create_upload_file(image: Annotated[UploadFile, File()], cvd_type: Annotated[str, Form()]):
    image_path = image.file

    try:
        if cvd_type == 'Achromatopsia':
            img = k_means_monochrome(image_path, 15)
        else:
            img = plane_rotation(image_path, cvd_type.lower())

        buffer = BytesIO()
        img.save(buffer, format='JPEG')
        buffer.seek(0)

        return Response(content=buffer.read(), media_type='image/jpeg')
    except Exception as e:
        print(f'Error: {e}')

    raise HTTPException(status_code=500, detail='Internal server error')


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=int(os.getenv('PORT') or 8000))
