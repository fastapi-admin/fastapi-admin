import os
from typing import List, Optional

import aiofiles
from starlette.datastructures import UploadFile

from fastapi_admin.exceptions import FileExtNotAllowed, FileMaxSizeLimit


class FileUpload:
    def __init__(
        self,
        uploads_dir: str,
        all_extensions: Optional[List[str]] = None,
        prefix: str = "/static/uploads",
        max_size: int = 1024 ** 3,
    ):
        self.max_size = max_size
        self.all_extensions = all_extensions
        self.uploads_dir = uploads_dir
        self.prefix = prefix

    def get_file_name(self, file: UploadFile):
        return file.filename

    async def upload(self, file: UploadFile):
        filename = self.get_file_name(file)
        if not filename:
            return
        content = await file.read()
        file_size = len(content)
        if file_size > self.max_size:
            raise FileMaxSizeLimit(f"File size {file_size} exceeds max size {self.max_size}")
        if self.all_extensions:
            for ext in self.all_extensions:
                if filename.endswith(ext):
                    raise FileExtNotAllowed(
                        f"File ext {ext} is not allowed of {self.all_extensions}"
                    )
        async with aiofiles.open(os.path.join(self.uploads_dir, filename), "wb") as f:
            await f.write(content)
        return os.path.join(self.prefix, filename)
