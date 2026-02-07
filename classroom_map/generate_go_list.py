from pathlib import Path


def main():
    current_path = Path(__file__).parent.resolve()

    maps = [f"\"{i.name.split('.')[0]}\"" for i in current_path.joinpath("images").iterdir()]
    print("[]string{" + ", ".join(maps) + "}")


if __name__ == "__main__":
    main()
