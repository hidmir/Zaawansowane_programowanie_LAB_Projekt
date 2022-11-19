import io
from fastapi import FastAPI, HTTPException, File, UploadFile, Depends
from fastapi.responses import Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from PIL import Image
import PIL.ImageOps
import math
import secrets
import datetime

app = FastAPI()

security = HTTPBasic()


def is_prime(number):
    if number < 0:
        raise HTTPException(status_code=422, detail="Number should be integer greater than 0.")
    if number == 0 or number == 1:
        return False
    for i in range(2, int(math.sqrt(number)) + 1):
        if (number % i) == 0:
            return False
    return True


def invert_colors(image):
    inverted_image = PIL.ImageOps.invert(image)
    buffer = io.BytesIO()
    inverted_image.save(buffer, 'jpeg')
    image_response = buffer.getvalue()

    return Response(content=image_response, media_type="image/jpeg")


def validate_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    user_name = credentials.username.encode("utf-8")
    password = credentials.password.encode("utf-8")

    stored_username = b'admin'
    stored_password = b'admin'

    is_username_valid = secrets.compare_digest(user_name, stored_username)
    is_password_valid = secrets.compare_digest(password, stored_password)

    if is_username_valid and is_password_valid:
        return {"auth message": "authentication successful"}

    raise HTTPException(status_code=401, detail="Invalid credentials")


@app.get("/prime/{number}")
async def is_prime_request(number: int):
    return f"Is {number} prime? -> {is_prime(number)}"


@app.post("/picture/invert")
async def invert_colors_request(file: UploadFile = File(...)):
    content = await file.read()
    image = Image.open(io.BytesIO(content))
    return invert_colors(image)


@app.get("/time")
async def get_time_request(credentials: HTTPBasicCredentials = Depends(validate_credentials)):
    return datetime.datetime.now().time()
