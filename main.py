from pathlib import Path

from PIL import Image, ImageOps


INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")
TARGET_SIZE = (800, 600)
JPEG_QUALITY = 100
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"}


def center_crop_box(width: int, height: int) -> tuple[int, int, int, int]:
    target_ratio = TARGET_SIZE[0] / TARGET_SIZE[1]
    source_ratio = width / height

    if source_ratio > target_ratio:
        crop_width = int(height * target_ratio)
        left = (width - crop_width) // 2
        return left, 0, left + crop_width, height

    crop_height = int(width / target_ratio)
    top = (height - crop_height) // 2
    return 0, top, width, top + crop_height


def save_image(image: Image.Image, path: Path) -> None:
    if image.mode in {"RGBA", "LA"} or (
        image.mode == "P" and "transparency" in image.info
    ):
        image = image.convert("RGBA")
        background = Image.new("RGB", image.size, (255, 255, 255))
        background.paste(image, mask=image.getchannel("A"))
        image = background
    elif image.mode != "RGB":
        image = image.convert("RGB")

    image.save(path, format="JPEG", quality=JPEG_QUALITY, subsampling=0)


def crop_image(source: Path, destination: Path) -> None:
    with Image.open(source) as image:
        image = ImageOps.exif_transpose(image)
        cropped = image.crop(center_crop_box(*image.size))
        resized = cropped.resize(TARGET_SIZE, Image.Resampling.LANCZOS)
        save_image(resized, destination)


def main() -> None:
    INPUT_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)

    images = sorted(
        path for path in INPUT_DIR.iterdir() if path.suffix.lower() in SUPPORTED_EXTENSIONS
    )
    if not images:
        print("No images found in input/")
        return

    for source in images:
        destination = OUTPUT_DIR / source.with_suffix(".jpeg").name
        crop_image(source, destination)
        print(f"{source} -> {destination}")


if __name__ == "__main__":
    main()
