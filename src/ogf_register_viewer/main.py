import copy
import json
from typing import Dict, List

from method.gen_pages import gen_pages
from method.get_plain_dataframe import (
    get_plain_dataframe,
)

# profile_name = "registry.moe.gov.hx.json"
profile_name = "airports.mot.gov.hx.json"
profile_file = open("../assets/profile/" + profile_name, "r", encoding="utf-8")
profile = json.loads(profile_file.read())
profile_file.close()

elements_dataframe: List[Dict] = get_plain_dataframe(
    {
        "key": profile["key"],
        "type": profile["type"],
        "poly": profile["poly"],
    }
)
elements_full: List[Dict] = copy.deepcopy(elements_dataframe)
elements_completed: List[Dict] = list(
    filter(
        bool,
        [
            item_dict if item_dict.get(profile["vital_key"]) != "" else None
            for item_dict in elements_dataframe
        ],
    )
)
elements_uncompleted: List[Dict] = list(
    filter(
        bool,
        [
            (
                item_dict
                if (item_dict["@type"], item_dict["@id"])
                in list(
                    set([(i["@type"], i["@id"]) for i in elements_full])
                    - set([(i["@type"], i["@id"]) for i in elements_completed])
                )
                else None
            )
            for item_dict in elements_dataframe
        ],
    )
)

elements_completed_sorted = sorted(
    elements_completed,
    key=lambda x: (x.get("addr:province"), x.get("short_name"), x["@id"]),
    reverse=True,
)
elements_uncompleted_sorted = sorted(
    elements_uncompleted, key=lambda x: x["@id"]
)

print(
    len(elements_completed_sorted),
    "+",
    len(elements_uncompleted_sorted),
    "=",
    len(elements_full),
)



gen_pages(
    elements_completed_sorted,
    elements_uncompleted_sorted,
    template_file_name=profile["template_file_name"],
    optional_data={"page_title": profile["page_title"]},
)
