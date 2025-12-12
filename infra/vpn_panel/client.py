from remnawave import RemnawaveSDK
from configs.settings import settings

# ленивый синглтон, чтобы не создавать SDK каждый раз
_remnawave_client: RemnawaveSDK | None = None


def get_remnawave_client() -> RemnawaveSDK:
    global _remnawave_client
    if _remnawave_client is None:
        _remnawave_client = RemnawaveSDK(
            base_url=settings.REMNAWAVE_BASE_URL,
            token=settings.REMNAWAVE_TOKEN,
        )
    return _remnawave_client
