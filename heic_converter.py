# Copyright (c) 2025 hprombex
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.
#
# Author: hprombex

"""
HEIC Converter for converting .HEIC images to other formats like JPEG or PNG,
while preserving metadata and providing additional options for quality and optimization.
"""

from __future__ import annotations

import os
import argparse
import logging
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

import pillow_heif
from PIL import Image
from PIL.ExifTags import TAGS


file_stem = Path(__file__).stem
log_directory = Path(__file__).with_name(f"{file_stem}_logs")
log_file = log_directory / f"{file_stem}_{datetime.now():%H_%M_%d_%m_%Y}.log"
os.makedirs(log_directory, exist_ok=True)

logger = logging.getLogger(__name__)
console = logging.StreamHandler()
file_handler = logging.FileHandler(log_file)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)6.8s:%(lineno)4d][%(levelname)-5.5s]: %(message)s",
    handlers=[console, file_handler],
)


class HeicConverter:
    """Class to handle conversion of .HEIC images to other formats."""

    @staticmethod
    def remove_exif_orientation(image: Image) -> Image:
        """
        Remove EXIF orientation metadata from the image.

        :param image: Image object from which EXIF orientation will be removed.
        :return: Updated EXIF data without orientation tag.
        """
        exif_data = image.getexif()

        if exif_data:
            for tag in exif_data.keys():
                if TAGS.get(tag) == "Orientation":
                    exif_data.pop(tag)

                    return exif_data

        return exif_data

    def convert_heic(
        self,
        input_file: str,
        output_file: str | None = None,
        quality: int = 80,
        optimize: bool = True,
        progressive: bool = True,
        image_format: str = "JPEG",
        delete: bool = False,
    ):
        """
        Convert a .HEIC file to the specified image format while preserving metadata.

        :param input_file: Path to the input .HEIC file.
        :param output_file: Path to the output file or directory.
        :param quality: Quality of the output image (1-100).
        :param optimize: Flag to optimize the output file size.
        :param progressive: Flag to enable progressive image generation.
        :param image_format: Output image format.
        :param delete: Flag to delete the original file after conversion.
        """
        pillow_heif.register_heif_opener()

        image_format = image_format.lower()
        if image_format not in ["jpeg", "png"]:  # only those formats are tested
            logger.warning(f"Untested format: {image_format}.")

        image = Image.open(input_file)

        exif_data = self.remove_exif_orientation(image)
        image.info["exif"] = exif_data

        original_name = Path(input_file).name
        filename = f"{original_name.replace('.', '_')}.{image_format.lower()}"

        if output_file is None:
            output_file = Path(input_file).parent / filename
        else:
            output_file = Path(output_file) / filename

        image.save(
            output_file,
            format=image_format,
            exif=exif_data,
            quality=quality,
            optimize=optimize,
            progressive=progressive,
        )

        logger.info(f"Converted {original_name} to {output_file}")

        if delete:
            logger.info(f"Deleting original file: '{input_file}'")
            Path(input_file).unlink(missing_ok=True)

    @staticmethod
    def find_heic_files(directory: str) -> list[str]:
        """
        Find all .HEIC files in a directory and its subdirectories.

        :param directory: The path to the directory to search.
        :return: A list of paths to .HEIC files.
        """
        heic_files = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.lower().endswith(".heic"):
                    heic_files.append(os.path.join(root, file))

        logger.info(f"Found {len(heic_files)} .HEIC files in '{directory}'.")

        return heic_files

    @staticmethod
    def parse_args() -> argparse.Namespace:
        """
        Parse command-line arguments.

        :return: Parsed command-line arguments.
        """
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--input_file",
            help="Path to a single .HEIC file to be converted.",
            type=str,
            required=False,
            default=None,
        )
        parser.add_argument(
            "--output_path",
            help="Path to the output file or directory.",
            type=str,
            required=False,
            default=None,
        )
        parser.add_argument(
            "--input_dir",
            help="Path to a directory containing .HEIC files.",
            type=str,
            required=False,
            default=None,
        )
        parser.add_argument(
            "--delete",
            help="Delete the original file after conversion.",
            required=False,
            action="store_true",
            default=False,
        )
        parser.add_argument(
            "--format",
            help="Output image format.",
            type=str,
            required=False,
            default="jpeg",
        )

        parser.add_argument(
            "--quality",
            help="Quality of the output image (1-100).",
            type=int,
            required=False,
            default=80,
        )

        parser.add_argument(
            "--optimize",
            help="Optimize the output file size.",
            required=False,
            action="store_true",
            default=True,
        )
        parser.add_argument(
            "--progressive",
            help="Enable progressive image generation.",
            required=False,
            action="store_true",
            default=True,
        )

        return parser.parse_args()

    def main(self) -> None:
        """Main method for executing the conversion process based on CLI arguments."""
        args = self.parse_args()

        if args.input_file:
            if not os.path.isfile(args.input_file):
                raise FileNotFoundError(
                    f"Input file '{args.input_file}' does not exist."
                )

            self.convert_heic(
                input_file=args.input_file,
                output_file=args.output_path,
                quality=args.quality,
                optimize=args.optimize,
                progressive=args.progressive,
                image_format=args.format,
                delete=args.delete,
            )

        if args.input_dir:
            if not os.path.isdir(args.input_dir):
                raise NotADirectoryError(
                    f"Input directory '{args.input_dir}' does not exist."
                )

            heic_files = self.find_heic_files(args.input_dir)
            max_threads: int = os.cpu_count()
            with ThreadPoolExecutor(max_threads) as executor:
                for idx, file in enumerate(heic_files):
                    executor.submit(
                        self.convert_heic,
                        file,
                        args.output_path,
                        args.quality,
                        args.optimize,
                        args.progressive,
                        args.format,
                        args.delete,
                    )


if __name__ == "__main__":
    heic = HeicConverter()
    heic.main()
