from itertools import count
import sys
from PIL import Image
from io import BytesIO

from google import genai

client = genai.Client()
MODEL_ID = "imagen-3.0-generate-002" # @param {isTemplate: true}
# prompt = sys.argv[1] # @param {type:"string"}
# prompt = "blurry watercolor of abstract shapes, THREE ancient stone lamps that light the world, solitary silhouette figure in shadow in the background, possibly female Buddha, sitting under a tree, pink hues" # @param {type:"string"}
prompt = "blurry watercolor of abstract shapes, THREE ancient stone lamps that light the world, pink hues" # @param {type:"string"}
number_of_images = 4 # @param {type:"slider", min:1, max:4, step:1}
person_generation = "ALLOW_ADULT" # @param ['DONT_ALLOW', 'ALLOW_ADULT']
aspect_ratio = "4:3" # @param ["1:1", "3:4", "4:3", "16:9", "9:16"]

result = client.models.generate_images(
    model=MODEL_ID,
    prompt=prompt,
    config=dict(
        number_of_images=number_of_images,
        output_mime_type="image/jpeg",
        person_generation=person_generation,
        aspect_ratio=aspect_ratio
    )
)

count = 0
for generated_image in result.generated_images:
  image = Image.open(BytesIO(generated_image.image.image_bytes))
  # Save the image to a file
  image.save(f"generated_image_{count}.jpg")
  count += 1