# File Upload

## FileUpload

`fastapi_admin.file_upload.FileUpload`

### uploads_dir

File upload directory.

### allow_extensions

Alow extensions list, default allow all extensions.

### max_size

Max size allow of file upload.

### filename_generator

Filename generator `Callable`, which param is `starlette.datastructures.UploadFile`.

## ALiYunOSSProvider (💗 Pro only)

`fastapi_admin.file_upload.ALiYunOSS(FileUpload)`

See <https://help.aliyun.com/product/31815.html>

### access_key

Access key of aliyun.

### access_key_secret

Access ket secret of aliyun.

### bucket

Bucket name of aliyun oss.

### endpoint

Endpoint of aliyun oss.

## AwsS3Provider (💗 Pro only)

`fastapi_admin.file_upload.AwsS3(FileUpload)`

See <https://aws.amazon.com/s3>

### access_key

Access key id of aws.

### access_key_secret

Access key secret of aws.

### bucket

Bucket name of s3.

### region_name

Regin name of s3.
