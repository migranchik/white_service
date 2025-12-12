from configs.settings import settings


class RefLinkCreator:
    @staticmethod
    def create(ref_code) -> str:
        bot_username = settings.BOT_USERNAME
        return f"https://t.me/{bot_username}?start={ref_code}"