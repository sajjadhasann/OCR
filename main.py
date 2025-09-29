import base64
import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from mistralai import Mistral

app = FastAPI()

# اجلب مفتاح Mistral من Environment Variables
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
if not MISTRAL_API_KEY:
    raise RuntimeError("MISTRAL_API_KEY is not set in environment variables")

client = Mistral(api_key=MISTRAL_API_KEY)

# الامتدادات المسموحة
ALLOWED_EXTENSIONS = [".pdf", ".jpg", ".jpeg", ".png"]

@app.post("/extract-text")
async def extract_text(file: UploadFile = File(...)):
    try:
        # تحقق من الامتداد
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"File type not supported. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
            )

        # اقرأ الملف في الذاكرة
        file_bytes = await file.read()
        b64 = base64.b64encode(file_bytes).decode()

        # اختر MIME type المناسب
        if ext == ".pdf":
            mime_type = "application/pdf"
        elif ext in [".jpg", ".jpeg"]:
            mime_type = "image/jpeg"
        elif ext == ".png":
            mime_type = "image/png"
        else:
            mime_type = "application/octet-stream"

        # جرب إرسال الملف لـ Mistral OCR
        try:
            resp = client.ocr.process(
                model="mistral-ocr-latest",
                document={
                    "type": "document_url",
                    "document_url": f"data:{mime_type};base64,{b64}"
                },
                include_image_base64=False,
            )

            pages_text = [page.markdown for page in resp.pages]

            return JSONResponse(content={
                "status": "success",
                "pages": pages_text
            })

        except Exception as api_error:
            # إذا API ما تدعم الصورة أو رجعت خطأ
            return JSONResponse(
                status_code=422,
                content={
                    "status": "failed",
                    "error": "Mistral OCR could not process this file type",
                    "details": str(api_error)
                }
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
