import qrcode


URL = "https://www.yourcoffeeapp.com/select-coffee"

qr_code = qrcode.make(URL)

qr_code.save("coffee_selection_qr.png")

print("QR code has been generated and saved as 'coffee_selection_qr.png'")

