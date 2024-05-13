import argparse
import os
import re
import time

import aiofiles
import httpx


class ImageGenerator:
    """
    Synchronous AI Image Creator by Microsoft Bing Image Creator (https://bing.com/images/create/).
    :param auth_cookie_u: Your https://bing.com/ _U auth cookie.
    :param auth_cookie_srchhpgusr: Your https://bing.com/ SRCHHPGUSR auth cookie.
    :param logging_enabled: Identifies whether logging is enabled or not.
    """

    def __init__(self, auth_cookie_u: str, auth_cookie_srchhpgusr: str, logging_enabled: bool = True):
        # Setting up httpx client
        self.client: httpx.Client() = httpx.Client(
            cookies={
                '_U': auth_cookie_u,
                'SRCHHPGUSR': auth_cookie_srchhpgusr
            }
        )

        # Setting up logging
        self.logging_enabled = logging_enabled

    def __log(self, message: str):
        if self.logging_enabled:
            print(message)

    def generate(self, prompt: str, num_images: int) -> list:
        """
        Generates AI images from a prompt.
        :param prompt: Description of image you want to generate.
        :param num_images: Number of images to generate.
        :return: List of generated image URLs.
        """

        images = []
        cycle = 0
        start = time.time()

        while len(images) < num_images:
            cycle += 1

            # Sending request to https://bing.com/
            response = self.client.post(
                url=f"https://www.bing.com/images/create?q={prompt}&rt=3&FORM=GENCRE",
                data={
                    'q': prompt,
                    'qs': 'ds'
                },
                follow_redirects=False,
                timeout=200
            )

            # Validating that request succeeded
            if response.status_code != 302:
                raise Exception("🛑 Request to https://bing.com/ failed! (Redirect)")

            self.__log(f"✅ Request to https://bing.com/ sent! (cycle: {cycle})")

            # Verify that response does not contain errors
            if "being reviewed" in response.text or "has been blocked" in response.text:
                raise Exception("🛑 Prompt is being reviewed or blocked!")
            if "image creator in more languages" in response.text:
                raise Exception("🛑 Language is not supported by Bing yet!")

            # Get redirect url
            result_id = response.headers['Location'].replace('&nfy=1', '').split('id=')[-1]
            results_url = f"https://www.bing.com/images/create/async/results/{result_id}?q={prompt}"

            # Wait for results
            self.__log(f"🕗 Awaiting generation... (cycle: {cycle})")
            start_time = time.time()
            while True:
                response = self.client.get(results_url)

                if time.time() - start_time > 200:
                    raise Exception("🛑 Waiting for results timed out!")

                if response.status_code != 200:
                    raise Exception("🛑 Exception happened while waiting for image generation! (NoResults)")

                if not response.text or response.text.find("errorMessage") != -1:
                    time.sleep(1)
                    continue
                else:
                    break

            # Find and return image links
            images += ["https://tse" + link.split("?w=")[0] for link in re.findall(
                'src="https://tse([^"]+)"', response.text)]
            self.__log(f"✅ Successfully finished cycle {cycle} in {round(time.time() - start_time, 2)} seconds")

        self.__log(
            f"✅ Finished generating {num_images} images in {round(time.time() - start, 2)} seconds and {cycle} cycles")
        return images[:num_images]

    def save(self, images: list, output_dir: str) -> None:
        """
        Saves generated images to a folder.
        :param images: List of generated image URLs.
        :param output_dir: Directory where to save generated images.
        """

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for images in images:
            response = self.client.get(images)
            if response.status_code != 200:
                raise Exception("🛑 Exception happened while saving image! (Response was not ok)")

            filename = f"{images.split('/id/')[1]}.jpeg"
            with open(os.path.join(output_dir, filename), "wb") as f:
                f.write(response.content)
                f.close()

            self.__log(f"✅ Saved image {filename}!")


class AsyncImageGenerator:
    """
    Asynchronous AI Image Creator by Microsoft Bing Image Creator (https://bing.com/images/create/).
    :param auth_cookie_u: Your https://bing.com/ _U auth cookie.
    :param auth_cookie_srchhpgusr: Your https://bing.com/ SRCHHPGUSR auth cookie.
    :param logging_enabled: Identifies whether logging is enabled or not.
    """

    def __init__(self, auth_cookie_u: str, auth_cookie_srchhpgusr: str, logging_enabled: bool = True):
        # Setting up httpx client
        self.client: httpx.AsyncClient() = httpx.AsyncClient(
            cookies={
                '_U': auth_cookie_u,
                'SRCHHPGUSR': auth_cookie_srchhpgusr
            }
        )

        # Setting up logging
        self.logging_enabled = logging_enabled

    def __log(self, message: str):
        if self.logging_enabled:
            print(message)

    async def generate(self, prompt: str, num_images: int) -> list:
        """
        Generates AI images from a prompt.
        :param prompt: Description of image you want to generate.
        :param num_images: Number of images to generate.
        :return: List of generated image URLs.
        """

        images = []
        cycle = 0
        start = time.time()

        while len(images) < num_images:
            cycle += 1

            # Sending request to https://bing.com/
            response = await self.client.post(
                url=f"https://www.bing.com/images/create?q={prompt}&rt=3&FORM=GENCRE",
                data={
                    'q': prompt,
                    'qs': 'ds'
                },
                follow_redirects=False,
                timeout=200
            )

            # Validating that request succeeded
            if response.status_code != 302:
                raise Exception("🛑 Request to https://bing.com/ failed! (Redirect)")

            self.__log(f"✅ Request to https://bing.com/ sent! (cycle: {cycle})")

            # Verify that response does not contain errors
            if "being reviewed" in response.text or "has been blocked" in response.text:
                raise Exception("🛑 Prompt is being reviewed or blocked!")
            if "image creator in more languages" in response.text:
                raise Exception("🛑 Language is not supported by Bing yet!")

            # Get redirect url
            result_id = response.headers['Location'].replace('&nfy=1', '').split('id=')[-1]
            results_url = f"https://www.bing.com/images/create/async/results/{result_id}?q={prompt}"

            # Wait for results
            self.__log(f"🕗 Awaiting generation... (cycle: {cycle})")
            start_time = time.time()
            while True:
                response = await self.client.get(results_url)

                if time.time() - start_time > 200:
                    raise Exception("🛑 Waiting for results timed out!")

                if response.status_code != 200:
                    raise Exception("🛑 Exception happened while waiting for image generation! (NoResults)")

                if not response.text or response.text.find("errorMessage") != -1:
                    time.sleep(1)
                    continue
                else:
                    break

            # Find and return image links
            images += ["https://tse" + link.split("?w=")[0] for link in re.findall(
                'src="https://tse([^"]+)"', response.text)]
            self.__log(f"✅ Successfully finished cycle {cycle} in {round(time.time() - start_time, 2)} seconds")

        self.__log(
            f"✅ Finished generating {num_images} images in {round(time.time() - start, 2)} seconds and {cycle} cycles")
        return images[:num_images]

    async def save(self, images: list, output_dir: str) -> None:
        """
        Saves generated images to a folder.
        :param images: List of generated image URLs.
        :param output_dir: Directory where to save generated images.
        """

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for images in images:
            response = await self.client.get(images)
            if response.status_code != 200:
                raise Exception("🛑 Exception happened while saving image! (Response was not ok)")

            filename = f"{images.split('/id/')[1]}.jpeg"
            async with aiofiles.open(os.path.join(output_dir, filename), "wb") as f:
                await f.write(response.content)
                await f.close()

            self.__log(f"✅ Saved image {filename}!")


def main():
    parser = argparse.ArgumentParser(
        prog="Image Creator",
        description="A simple lightweight AI Image Generator from text description using Bing Image Creator (DALL-E 3)",
        epilog="Made by Waenara ^^"
    )

    parser.add_argument(
        "--u",
        help="Your _U cookie from https://bing.com/",
        required=True
    )

    parser.add_argument(
        "--s",
        help="Your SRCHHPGUSR cookie from https://bing.com/",
        required=True
    )

    parser.add_argument(
        "--prompt",
        help="Description of image to generate",
        required=True
    )

    parser.add_argument(
        "--number",
        help="How many images to generate. Default: 4",
        type=int,
        default=4
    )

    parser.add_argument(
        "--output",
        help="Directory where to save generated images. If not specified you will just get links printed out",
    )

    parser.add_argument(
        "--quiet",
        help="If present logging is disabled",
        action="store_true"
    )

    args = parser.parse_args()
    generator = ImageGenerator(args.u, args.s, not args.quiet)
    generated_images = generator.generate(args.prompt, args.number)

    if args.out_dir:
        generator.save(generated_images, args.out_dir)
    else:
        for generated_image in generated_images:
            print(f"🖼 {generated_image}")


if __name__ == "__main__":
    main()
