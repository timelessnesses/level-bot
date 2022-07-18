from PIL import Image, ImageDraw
import io


def box(rgb: tuple) -> io.BytesIO:
    image = Image.new("RGBA", (100, 100))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 100, 100), fill=(rgb))
    file = io.BytesIO()
    image.save(file, "png")
    file.seek(0)
    return file


open("g.png", "wb").write(box((0, 255, 1)).read())
