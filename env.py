import os


def loadenv():
    os.environ.update({
        "NLS_LANG": "RUSSIAN_RUSSIA.UTF8",
        "PROJECT_ROOT": os.path.dirname(os.path.abspath(__file__))
    })

    dotenv_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '.env.config')
    if os.path.exists(dotenv_path):
        from dotenv import load_dotenv

        load_dotenv(dotenv_path)
