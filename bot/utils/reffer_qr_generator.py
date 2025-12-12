import qrcode
from io import BytesIO
from aiogram.types import BufferedInputFile


async def generate_qr_image(data: str) -> BufferedInputFile:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # --- ВАЖНО: цвет QR и фон ---
    img = qr.make_image(
        fill_color="black",        # цвет точек
        back_color="#F4C90F"       # светло-жёлтый фон (например: soft yellow)
    )

    byte_io = BytesIO()
    img.save(byte_io, format="PNG")
    byte_io.seek(0)

    return BufferedInputFile(byte_io.read(), filename="qr.png")