import zipfile


def main() -> None:
    xlsx_path = r"c:\Users\abous\Downloads\remonté d'incident opérationnel-12.xlsx"
    inner_path = "xl/worksheets/sheet1.xml"
    with zipfile.ZipFile(xlsx_path, "r") as z:
        xml = z.read(inner_path).decode("utf-8", errors="replace")

    # Dump around extLst and around the first occurrence of 'dataValidations'
    i = xml.find("<extLst")
    j = xml.find("</extLst>")
    if i != -1 and j != -1:
        ext = xml[i : j + len("</extLst>")]
    else:
        ext = ""

    k = xml.find("dataValidations")
    around = xml[max(0, k - 500) : k + 2500] if k != -1 else ""

    with open("sheet1_extlst.xml.txt", "w", encoding="utf-8") as f:
        f.write("=== extLst ===\n")
        f.write(ext)
        f.write("\n\n=== around dataValidations ===\n")
        f.write(around)

    print("Wrote sheet1_extlst.xml.txt")


if __name__ == "__main__":
    main()

