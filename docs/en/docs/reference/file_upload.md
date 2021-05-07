# File Upload

## FileUpload

`fastapi_admin.file_upload.FileUpload`

`FileUpload` is used in `file` input widget.

```python
upload = FileUpload(uploads_dir=os.path.join(BASE_DIR, "static", "uploads"))

@app.register
class AdminResource(Model):
    fields = [
        Field(
            name="avatar",
            label="Avatar",
            display=displays.Image(width="40"),
            input_=inputs.Image(null=True, upload=upload),
        ),
    ]
```

### Parameters

- `uploads_dir`: File upload directory.
- `allow_extensions`: Alow extensions list, default allow all extensions.
- `max_size`: Max size allow of file upload.
- `filename_generator`: Filename generator `Callable`, which param type passed is `starlette.datastructures.UploadFile`.

## ALiYunOSS (💗 Pro only)

`fastapi_admin.file_upload.ALiYunOSS`

See <https://help.aliyun.com/product/31815.html>

### Parameters

- `access_key`: Access key of aliyun.
- `access_key_secret`: Access ket secret of aliyun.
- `bucket`: Bucket name of aliyun oss.
- `endpoint`: Endpoint of aliyun oss.

## AwsS3 (💗 Pro only)

`fastapi_admin.file_upload.AwsS3`

See <https://aws.amazon.com/s3>

### Parameters

- `access_key`: Access key of aws.
- `access_key_secret`: Access ket secret of aws.
- `bucket`: Bucket name of aws.
- `region_name`: Regin name of aws.
