import subprocess


ROOT_FOLDER_NAME = "python"
PACKAGE_NAME = "lambda-utility"
OUTPUT_ZIP_NAME = "lambda-utility"


def install():
    subprocess.run(["rm", "-rf", ROOT_FOLDER_NAME], check=True)
    subprocess.run(["mkdir", ROOT_FOLDER_NAME], check=True)
    subprocess.run(["pip", "install", PACKAGE_NAME, "-t", ROOT_FOLDER_NAME], check=True)


def compress():
    subprocess.run(["zip", "-r", f"{OUTPUT_ZIP_NAME}.zip", ROOT_FOLDER_NAME, "-x", "__MACOSX"], check=True)


def main():
    print("Start")
    try:
        install()
        compress()
        print(f"Complete -> '{OUTPUT_ZIP_NAME}.zip'")
    finally:
        subprocess.run(["rm", "-rf", ROOT_FOLDER_NAME], check=True)


if __name__ == "__main__":
    main()
