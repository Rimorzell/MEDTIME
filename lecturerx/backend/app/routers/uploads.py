from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, status

from app.utils.s3 import generate_presigned_upload_url

router = APIRouter(prefix="/api/uploads", tags=["uploads"])


class PresignedUploadRequest(BaseModel):
    file_name: str
    file_type: str


class PresignedUploadResponse(BaseModel):
    upload_url: str


@router.post("/presigned-url", response_model=PresignedUploadResponse)
def create_presigned_upload_url(payload: PresignedUploadRequest) -> PresignedUploadResponse:
    try:
        return PresignedUploadResponse(upload_url=generate_presigned_upload_url(payload.file_name, payload.file_type))
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)) from exc
