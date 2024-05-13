# Image Creator
This is a simple lightweight reverse engineered [Bing Image Creator](https://bing.com/create) API made in python that allows you to quickly generate high quality AI images. This package was inspired by [BingImageCreator package](https://github.com/acheong08/BingImageCreator) and the main goal is to make better version of it.

**Advantages over the original package:**
- Actively maintained
- Lightweight
- Easier to use
- Ability to specify the number of images to generate
- Termux support
- Complete code rewrite

You can use it from console\terminal or integrate it to your python project. To get started read the instructions below.

## Installation
To install the package you can use pip:
```bash
pip install image_creator
```
or you can clone the repository and install it manually:
```bash
git clone 
cd image_creator
pip install .
```
## Usage
### Getting cookies
After installing the package as described above you will need to get your **_U** and **SRCHHPGUSR** cookies from [Bing](https://bing.com). You can do this by logging in to [Bing](https://bing.com), opening the developer tools (F12) and going to the console tab. Then you can run the following code:
```javascript
console.log(`_U:\n${document.cookie.match(/(?:^|;\s*)_U=(.*?)(?:;|$)/)[1]}\n\nSRCHHPGUSR:\n${document.cookie.match(/(?:^|;\s*)SRCHHPGUSR=(.*?)(?:;|$)/)[1]}`)
```
This will output your **_U** and **SRCHHPGUSR** cookies.

### Terminal\Console
If you are an average user you can use the package from the console\terminal. 
After you installed the package and got the cookies. use the following command to get help, or you may enter arguments from below to generate images:
```bash
image_creator
```
**All arguments:**
- `--u` - Your **_U** cookie
- `--s` - Your **SRCHHPGUSR** cookie
- `--prompt` - Description of images you want to generate
- `--output` (Optional) - Path to directory where the images will be saved
- `--number` (Optional, default: 4) - Number of images to generate
- `--quiet` (Optional) - If present logging is disabled

### Integration to your python project
If you are a developer you can integrate the package to your python project. Here is an example of how you can use the package:

Synchronous:
```python
from image_creator.main import ImageGenerator

# Create an instance of the ImageGenerator class
generator = ImageGenerator(
    auth_cookie_u='Your _U cookie',
    auth_cookie_srchhpgusr='Your SRCHHPGUSR cookie'
)

# Generate 5 images from a text prompt
images = generator.generate(
    prompt='A cute cat',
    num_images=5
)

# Save the images to the directory called 'output'
generator.save(
    images=images, 
    output_dir='output'
)
```

Asynchronous:
```python
import asyncio
from image_creator.main import AsyncImageGenerator


async def main():
    # Create an instance of the AsyncImageGenerator class
    generator = AsyncImageGenerator(
        auth_cookie_u='Your _U cookie',
        auth_cookie_srchhpgusr='Your SRCHHPGUSR cookie'
    )

    # Generate 5 images from a text prompt
    images = await generator.generate(
        prompt='A cute cat',
        num_images=5
    )

    # Save the images to the directory called 'output'
    await generator.save(
        images=images,
        output_dir='output'
    )


asyncio.run(main())
```