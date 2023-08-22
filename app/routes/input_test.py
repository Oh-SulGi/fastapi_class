from fastapi import APIRouter, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import HTMLResponse

import os
import pandas as pd

router = APIRouter()
templates = Jinja2Templates(directory="templates")

STATIC_DIR ='static/'
MEDIA_DIR = 'media/'
MEDIA_DIR_DB = MEDIA_DIR+'DB/'


# 파일 업로드를 처리하는 API
@router.get("/upload_test", response_class=HTMLResponse)
def upload_page(request: Request):
    return templates.TemplateResponse("input_test.html", 
                                      {"request":request})


@router.post("/upload_files", response_class=HTMLResponse)
async def upload_file(request: Request, file: UploadFile = File(...)):
    # 파일을 저장할 디렉토리 체크 후 생성
    upload_dir = MEDIA_DIR_DB
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    # 파일 저장
    file_path = os.path.join(upload_dir, file.filename)
    print(file_path)
    with open(file_path, "wb") as buffer:
        while True:
            data = file.file.read(1024)
            if not data:
                break
            buffer.write(data)

    result = "Upload success: {}".format(file.filename)
    print(file.filename)
    save_path = MEDIA_DIR_DB + file.filename
    return templates.TemplateResponse("input_test.html", 
                                      {"request": request, 
                                       "result": result,
                                       "save_path": save_path})

@router.post('/upload_files_docs')
async def upload_docs(request: Request, user_id: str, file: UploadFile = File(...)):
    # 파일을 저장할 디렉토리 체크 후 생성
    upload_dir = 'media/picture/'
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    # 파일 저장
    file_path = os.path.join(upload_dir, user_id + '_' + file.filename)
    df_path = 'media/DB/image_db.csv'

    image_db = {
        'id' : [user_id],
        'file_path' : [file_path],
        'file_name' : [file.filename]
    }
    df = pd.DataFrame(image_db)
    df.to_csv(df_path)

    print(file_path)
    with open(file_path, "wb") as buffer:
        while True:
            data = file.file.read(1024)
            if not data:
                break
            buffer.write(data)

    result = "Upload success: {}".format(file.filename)
    print(file.filename)
    save_path = upload_dir + file.filename
    return templates.TemplateResponse("input_test.html", 
                                      {"request": request, 
                                       "result": result,
                                       "save_path": save_path})