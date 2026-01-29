from PIL import Image
import base64
from io import BytesIO

def image2base64(image: Image.Image) -> str:
    """Convert a PIL Image to a base64 encoded string."""


    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str