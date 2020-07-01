import asyncio
from pathlib import Path
import click
from pyppeteer import launch
from PIL import Image


async def capture_screenshot(url: str, path: Path, viewport_width: int, viewport_height: int) -> None:
    browser = await launch()
    page = await browser.newPage()
    await page.setViewport({'width': viewport_width, 'height': viewport_height})
    await page.goto(url)
    await page.screenshot({'path': path})
    await browser.close()


def resize_screenshot(original_path: Path, resized_path: Path, width: int, height: int) -> None:
    im = Image.open(original_path)
    im.thumbnail((width, height))
    im.save(resized_path)


@click.group()
def cli():
    pass


@cli.command()
@click.option('--url')
@click.option('--viewport_width', default=1200)
@click.option('--viewport_height', default=800)
@click.option('--width', default=700)
@click.option('--height', default=466)
@click.option('--filename', default='screenshot.png')
@click.option('--resized_filename', default='screenshot_resized.png')
def screenshot(url, viewport_width, viewport_height, width, height, filename, resized_filename):
    print(url)
    click.echo("Capturing screenshot...")
    original_path = Path(filename)
    resized_path = Path(resized_filename)
    asyncio.get_event_loop().run_until_complete(capture_screenshot(url, original_path, viewport_width, viewport_height))
    resize_screenshot(original_path, resized_path, width, height)
    click.echo("Done")


if __name__ == "__main__":
    cli()