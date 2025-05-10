from PIL import Image

# Open the PNG file
png_image = Image.open("logo.png")

# Convert to ICO format and save
png_image.save("logo.ico", format="ICO")

print("Converted logo.png to logo.ico")