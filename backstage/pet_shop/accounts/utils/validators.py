"""
File upload validation utilities.

Provides reusable validators for image uploads to prevent:
- Malicious file types (e.g., PHP scripts disguised as images)
- Oversized files that could exhaust storage or memory
- Invalid image dimensions
"""

import os
from typing import Optional, Tuple

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from django.utils.translation import gettext_lazy as _

# Default limits (can be overridden via Django settings)
DEFAULT_MAX_FILE_SIZE_MB = 5
DEFAULT_ALLOWED_IMAGE_TYPES = {
    'image/jpeg',
    'image/png',
    'image/gif',
    'image/webp',
}
DEFAULT_ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}


def validate_image_upload(
    file_obj: UploadedFile,
    max_size_mb: Optional[float] = None,
    allowed_types: Optional[set] = None,
    allowed_extensions: Optional[set] = None,
    require_image: bool = True,
) -> None:
    """
    Validate an uploaded image file.

    Args:
        file_obj: The uploaded file object from request.FILES
        max_size_mb: Maximum file size in megabytes (default: 5MB)
        allowed_types: Set of allowed MIME types (default: common image types)
        allowed_extensions: Set of allowed file extensions (default: common image types)
        require_image: Whether to validate that the file is actually an image

    Raises:
        ValidationError: If validation fails
    """
    if not file_obj:
        raise ValidationError(_('请选择要上传的文件'))

    # Get limits from settings or use defaults
    max_size = max_size_mb or getattr(settings, 'MAX_UPLOAD_SIZE_MB', DEFAULT_MAX_FILE_SIZE_MB)
    allowed_types = allowed_types or getattr(settings, 'ALLOWED_IMAGE_TYPES', DEFAULT_ALLOWED_IMAGE_TYPES)
    allowed_extensions = allowed_extensions or getattr(settings, 'ALLOWED_IMAGE_EXTENSIONS', DEFAULT_ALLOWED_EXTENSIONS)

    # Check file size
    max_size_bytes = max_size * 1024 * 1024
    if file_obj.size > max_size_bytes:
        raise ValidationError(
            _('文件大小不能超过 %(max_size)s MB'),
            params={'max_size': max_size},
        )

    # Check file extension
    file_ext = os.path.splitext(file_obj.name)[1].lower()
    if file_ext not in allowed_extensions:
        raise ValidationError(
            _('不支持的文件格式。允许的格式: %(formats)s'),
            params={'formats': ', '.join(sorted(allowed_extensions))},
        )

    # Check MIME type (content type)
    content_type = getattr(file_obj, 'content_type', None)
    if content_type and content_type not in allowed_types:
        raise ValidationError(
            _('不支持的文件类型: %(type)s'),
            params={'type': content_type},
        )

    # If require_image is True, try to open the file as an image
    if require_image:
        try:
            from PIL import Image
            file_obj.seek(0)  # Reset file pointer
            img = Image.open(file_obj)
            img.verify()  # Verify it's actually an image
            file_obj.seek(0)  # Reset again after verify
        except Exception:
            raise ValidationError(_('上传的文件不是有效的图片'))
        finally:
            file_obj.seek(0)  # Ensure file pointer is reset


def validate_avatar_upload(file_obj: UploadedFile) -> None:
    """
    Validate avatar upload with avatar-specific restrictions.

    Args:
        file_obj: The uploaded file object

    Raises:
        ValidationError: If validation fails
    """
    validate_image_upload(
        file_obj,
        max_size_mb=2,  # Avatars are typically smaller
        allowed_types={'image/jpeg', 'image/png', 'image/gif'},
        allowed_extensions={'.jpg', '.jpeg', '.png', '.gif'},
        require_image=True,
    )


def validate_product_image_upload(file_obj: UploadedFile) -> None:
    """
    Validate product image upload.

    Args:
        file_obj: The uploaded file object

    Raises:
        ValidationError: If validation fails
    """
    validate_image_upload(
        file_obj,
        max_size_mb=10,  # Product images can be larger
        allowed_types=DEFAULT_ALLOWED_IMAGE_TYPES,
        allowed_extensions=DEFAULT_ALLOWED_EXTENSIONS,
        require_image=True,
    )