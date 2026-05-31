import json
import zipfile
import xml.etree.ElementTree as ET


def _strip_ns(tag: str) -> str:
    if "}" in tag:
        return tag.split("}", 1)[1]
    return tag


def parse_sheet_xml(xml_bytes: bytes) -> dict:
    root = ET.fromstring(xml_bytes)
    out = {
        "dataValidations": [],
        "ext_dataValidations": [],
    }

    # Standard dataValidations
    for dv_parent in root.iter():
        if _strip_ns(dv_parent.tag) == "dataValidations":
            for dv in list(dv_parent):
                if _strip_ns(dv.tag) != "dataValidation":
                    continue
                out["dataValidations"].append(
                    {
                        "type": dv.attrib.get("type"),
                        "operator": dv.attrib.get("operator"),
                        "allowBlank": dv.attrib.get("allowBlank"),
                        "sqref": dv.attrib.get("sqref"),
                        "formula1": (dv.find(".//{*}formula1").text if dv.find(".//{*}formula1") is not None else None),
                        "formula2": (dv.find(".//{*}formula2").text if dv.find(".//{*}formula2") is not None else None),
                    }
                )

    # Extension list (often contains x14:dataValidations)
    # We'll keep it resilient by searching for any element whose localname includes 'dataValidations' under extLst.
    for extlst in root.iter():
        if _strip_ns(extlst.tag) != "extLst":
            continue
        for ext in list(extlst):
            # Try to locate any nested dataValidations-like nodes
            for node in ext.iter():
                local = _strip_ns(node.tag)
                if local == "dataValidations":
                    # x14:dataValidations can contain x14:dataValidation children with different schema
                    for dv in list(node):
                        if _strip_ns(dv.tag) != "dataValidation":
                            continue
                        out["ext_dataValidations"].append(
                            {
                                "attrib": dict(dv.attrib),
                                "children": [
                                    {"tag": _strip_ns(ch.tag), "attrib": dict(ch.attrib), "text": (ch.text or "").strip()}
                                    for ch in list(dv)
                                ],
                            }
                        )
    return out


def main() -> None:
    xlsx_path = r"c:\Users\abous\Downloads\remonté d'incident opérationnel-12.xlsx"
    with zipfile.ZipFile(xlsx_path, "r") as z:
        names = z.namelist()
        workbook_xml = z.read("xl/workbook.xml")
        wb_root = ET.fromstring(workbook_xml)

        # map sheetId order to worksheet file via workbook relationships
        rels_root = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        rId_to_target = {}
        for rel in rels_root.findall(".//{*}Relationship"):
            rId_to_target[rel.attrib.get("Id")] = rel.attrib.get("Target")

        sheets = []
        for sh in wb_root.findall(".//{*}sheet"):
            name = sh.attrib.get("name")
            rid = sh.attrib.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
            target = rId_to_target.get(rid)
            if not target:
                continue
            # Targets are relative to xl/
            sheet_path = "xl/" + target.lstrip("/")
            if sheet_path not in names:
                # some targets are like worksheets/sheet1.xml already
                sheet_path = "xl/" + target
            xml = z.read(sheet_path)
            parsed = parse_sheet_xml(xml)
            sheets.append(
                {
                    "name": name,
                    "sheet_path": sheet_path,
                    "dataValidations_count": len(parsed["dataValidations"]),
                    "ext_dataValidations_count": len(parsed["ext_dataValidations"]),
                    "dataValidations": parsed["dataValidations"][:200],
                    "ext_dataValidations": parsed["ext_dataValidations"][:200],
                }
            )

    print(json.dumps({"path": xlsx_path, "sheets": sheets}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

