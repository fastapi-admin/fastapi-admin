import subprocess


def build(setup_kwargs):
    print("Compile translations:")
    subprocess.run(["pybabel", "compile", "--directory", "fastapi_admin/locales"])
    return setup_kwargs
