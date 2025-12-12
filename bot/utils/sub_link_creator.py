from configs.settings import settings


class SubLinkCreator:
    @staticmethod
    def create(short_uid) -> str:
        base_sub_link = settings.REMNAWAVE_BASE_SUB_LINK
        return f"{base_sub_link}{short_uid}"