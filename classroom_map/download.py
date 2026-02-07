from pathlib import Path

import requests

building_id = [
    "0", "1", "3", "4", "5", "6", "7", "8", "9",
    "CM", "TC", "MA", "PH", "BT", "LI"
]

skip_url = "https://sso.nknu.edu.tw/WebServices/ajaxImageReader.aspx?cAES=fXsbMu6B1ZJBrfsl15kdZgG3NL%2bkMN7ClE3rsUl9Who%3d"

current_path = Path(__file__).parent.resolve()
if not current_path.joinpath("images").exists():
    current_path.joinpath("images").mkdir()


def get_download_url(building, floor):
    s = 1 if building != "LI" else 50
    end = 21 if building != "LI" else 60
    for cid in range(s, end):
        print(f"{building}{floor}{cid:0>2}")
        req = requests.post(
            "https://sso.nknu.edu.tw/iCampus/iManagement/Map/ajaxServices/ajaxFloorPlan.aspx",
            json={"cFunction": "getImagemapsterAreasJsonByRoomID",
                  "cRoomID": f"{building}{floor}{cid:0>2}"}
        )

        if req.json()["data"]["ImageSrc"] == skip_url:
            continue
        else:
            return req.json()["data"]["ImageSrc"]

    return None


def main():
    for building in building_id:
        s = 1 if building != "LI" else 1
        end = 10 if building != "LI" else 2
        for floor in range(s, end):
            print(f"Requesting image url for building {building} floor {floor}")

            image_url = get_download_url(building, floor)
            if image_url is None:
                continue

            image_data = requests.get(image_url).content
            image_path = current_path.joinpath(
                "images", f"{building}{floor}.png")
            with open(image_path, "wb+") as f:
                f.write(image_data)



if __name__ == "__main__":
    main()
