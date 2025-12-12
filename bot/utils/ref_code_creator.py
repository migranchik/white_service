class RefCodeCreator():
    @staticmethod
    def create(tg_id: int) -> str:
        return f"ref_{tg_id}"