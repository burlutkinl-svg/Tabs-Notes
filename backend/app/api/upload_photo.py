import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi import APIRouter
import aiofiles
from uuid import uuid4

router = APIRouter()

@router.post("/upload_photo")
async def upload_multiple_files(photos: list[UploadFile] = File(...)):
    saved_filenames = []
    
    for file in photos:
        # Генерируем уникальное имя для каждого файла
        ext = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid4().hex}{ext}"
        file_path = os.path.join('uploads', unique_filename)  # теперь строка
        
        try:
            # Убедимся, что папка uploads существует
            os.makedirs('uploads', exist_ok=True)
            
            # Асинхронная запись
            async with aiofiles.open(file_path, 'wb') as buffer:
                content = await file.read()
                await buffer.write(content)
            
            saved_filenames.append(unique_filename)
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка сохранения {file.filename}: {e}")
        finally:
            await file.close()
    
    return JSONResponse(content={"status": "загружено", "filenames": saved_filenames})
