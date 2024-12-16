from PIL import Image, ImageEnhance, ImageOps
from io import BytesIO
from flask import Flask, request, send_file

app = Flask(__name__)

# GRAYSCALE FILTER
def grayscale_filter(image_stream):
    image = Image.open(image_stream)

    grayscale_image = image.convert("L")

    enhancer = ImageEnhance.Contrast(grayscale_image)
    enhanced_image = enhancer.enhance(1.5)

    output_stream = BytesIO()
    enhanced_image.save(output_stream, format="JPEG")
    output_stream.seek(0)
    return output_stream

# INVERT FILTER
def invert_filter(image_stream):
    image = Image.open(image_stream)

    inverted_image = ImageOps.invert(image.convert("RGB"))

    output_stream = BytesIO()
    inverted_image.save(output_stream, format="JPEG")
    output_stream.seek(0)
    return output_stream

# SEPIA FILTER
def sepia_filter(image_stream):
    image = Image.open(image_stream)

    sepia_image = ImageOps.colorize(image.convert("L"), black="#704214", white="#C0A080")

    output_stream = BytesIO()
    sepia_image.save(output_stream, format="JPEG")
    output_stream.seek(0)
    return output_stream

@app.route('/grayscale-filter', methods=['POST'])
def convert_grayscale_image():
    if 'image' not in request.files:
        return {"error": "No image provided"}, 400

    image_file = request.files['image']
    filtered_image_stream = grayscale_filter(image_file.stream)
    return send_file(filtered_image_stream, mimetype='image/jpeg')

@app.route('/invert-filter', methods=['POST'])
def convert_invert_image():
    if 'image' not in request.files:
        return {"error": "No image provided"}, 400

    image_file = request.files['image']
    filtered_image_stream = invert_filter(image_file.stream)
    return send_file(filtered_image_stream, mimetype='image/jpeg')

@app.route('/sepia-filter', methods=['POST'])
def convert_sepia_image():
    if 'image' not in request.files:
        return {"error": "No image provided"}, 400

    image_file = request.files['image']
    filtered_image_stream = sepia_filter(image_file.stream)
    return send_file(filtered_image_stream, mimetype='image/jpeg')

if __name__ == "__main__":
    app.run(debug=True)
