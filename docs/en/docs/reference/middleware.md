# Middleware

## LoginPasswordMaxTryMiddleware (💗 Pro only)

If you want limit login failed ip with error password, you can use `LoginPasswordMaxTryMiddleware`.

```python
admin_app.add_middleware(BaseHTTPMiddleware, dispatch=LoginPasswordMaxTryMiddleware(max_times=3, after_seconds=3600))
```

After that, user can try max `3` times password, if all failed, the ip will be limited `3600` seconds.
