import os
import asyncio
import aiohttp
from lxml import html
from PIL import Image
from io import BytesIO


async def download_image(session, image_url, folder_name, index):
    async with session.get(image_url) as response:
        if response.status == 200:
            image = Image.open(BytesIO(await response.read()))
            image = image.convert("RGBA")
            image.save(os.path.join(folder_name, f"image_{index}.png"), format="PNG")
            print(f"Image {index} downloaded successfully.")
        else:
            print(f"Failed to download Image {index}.")


async def download_images(url, folder_name):
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        if response.status == 200:
            tree = html.fromstring(await response.text())
            xpath = "/html/body/div[1]/div[2]/div[2]/section/div[1]/div[3]/div[2]/div[3]/ul/li"
            image_elements = tree.xpath(xpath)

            # Create the folder if it doesn't exist
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)

            tasks = []
            for i, element in enumerate(image_elements, start=1):
                style_attribute = element.xpath(".//span[@class='mdCMN09Image']/@style")
                if style_attribute:
                    image_url = style_attribute[0].split("url(")[1].split(")")[0]
                    tasks.append(
                        download_image(session, image_url, folder_name, i)
                    )
                else:
                    print(f"Image URL not found for {i}.")

            await asyncio.gather(*tasks)
