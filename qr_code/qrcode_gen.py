from qrcode.main import QRCode


def gen_qrcode(data: str):
    qr = QRCode(
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    with open('build/output.png', 'wb') as f:
        img.save(f)


if __name__ == '__main__':
    gen_qrcode('https://play.google.com/store/apps/details?id=com.browser.privacy.stool.bookmark.security')
    # gen_qrcode('https://play.google.com/store/apps/details?id=com.wheresmyphone.eltools')
