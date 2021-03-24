import argparse
import subprocess


ROOT_FOLDER_NAME = "python"
PACKAGE_NAME = "lambda-utility"
OUTPUT_FILENAME = "lambda-utility.zip"


def install():
    subprocess.run(["rm", "-rf", ROOT_FOLDER_NAME], check=True)
    subprocess.run(["mkdir", ROOT_FOLDER_NAME], check=True)
    subprocess.run(["pip", "install", PACKAGE_NAME, "-t", ROOT_FOLDER_NAME], check=True)


def compress(filename: str):
    subprocess.run(
        ["zip", "-r", filename, ROOT_FOLDER_NAME, "-x", "__MACOSX"], check=True
    )


def main():
    parser = argparse.ArgumentParser(description="Create a layer file")
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help=f"output filename (default: {OUTPUT_FILENAME!r})",
        default=OUTPUT_FILENAME,
    )
    arguments = parser.parse_args()
    output_filename = arguments.output

    print("Start")
    try:
        install()
        compress(output_filename)
        print(f"Complete -> {output_filename!r}")
    finally:
        subprocess.run(["rm", "-rf", ROOT_FOLDER_NAME], check=True)


if __name__ == "__main__":
    main()
