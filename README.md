# HEIC Converter

A Python-based utility for converting `.HEIC` image files to other formats such as `.JPEG` or `.PNG`. This tool preserves metadata while providing flexible options for output quality, format, and other parameters.

## Features
- Convert `.HEIC` files to `.JPEG` or `.PNG` formats.
- Preserve EXIF metadata during the conversion.
- Optionally delete the original `.HEIC` files after conversion.
- Batch conversion of `.HEIC` files in a directory.
- Customizable output options such as quality, optimization, and progressive encoding.

## Prerequisites
Ensure you have the following dependencies installed:

- Python 3.9+
- Required Python libraries:
  - `pillow`
  - `pillow_heif`

Install the required dependencies using:
```bash
pip install pillow pillow-heif
```

## Installation
Clone the repository:
```bash
git clone https://github.com/hprombex/heic_converter.git
cd heic_converter
```

## Usage

### Command-Line Interface
Run the script using the command line with the following arguments:

#### Arguments

- `--input_file`
  - Description: Path to a single `.HEIC` file to be converted.
  - Example: `--input_file /path/to/image.heic`

- `--output_path`
  - Description: Path to save the converted file(s). Defaults to the input file's directory.
  - Example: `--output_path /path/to/output`

- `--input_dir`
  - Description: Path to a directory containing `.HEIC` files for batch conversion.
  - Example: `--input_dir /path/to/heic_files`

- `--delete`
  - Description: Delete original `.HEIC` file(s) after successful conversion.
  - Example: `--delete`

- `--format`
  - Description: Output image format (`jpeg` or `png`). Defaults to `jpeg`.
  - Example: `--format png`

- `--quality`
  - Description: Quality of the output image (1-100). Defaults to 80.
  - Example: `--quality 90`

- `--optimize`
  - Description: Optimize the output image size. Enabled by default.

- `--progressive`
  - Description: Save images in progressive format. Enabled by default.

#### Examples

**Convert a single file:**
```bash
python heic_converter.py --input_file /path/to/image.heic --output_path /path/to/output --quality 90
```

**Convert all `.HEIC` files in a directory:**
```bash
python heic_converter.py --input_dir /path/to/heic_files --output_path /path/to/output --format png
```

**Convert and delete original files:**
```bash
python heic_converter.py --input_dir /path/to/heic_files --delete
```

### Use Case: Converting `.HEIC` Images from iPhone
This tool is handy for converting `.HEIC` images downloaded from an iPhone to formats like `.JPEG` for easier sharing or compatibility with other devices and applications. Simply point the script to the folder containing downloaded `.HEIC` files from iPhone, and it will handle the conversion efficiently.

```bash
python heic_converter.py --input_dir /path/to/iphone_images --output_path /path/to/converted_images --format jpeg
```

## Programmatic Usage

You can also use the `HeicConverter` class directly in your Python code:

```python
from heic_converter import HeicConverter

converter = HeicConverter()
converter.convert_heic(
    input_file="/path/to/image.heic",
    output_file="/path/to/output/image.jpeg",
    quality=90,
    optimize=True,
    progressive=True,
    image_format="jpeg",
    delete=False,
)
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

**hprombex**

Feel free to contribute or suggest improvements!
