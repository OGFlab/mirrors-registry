import copy
from typing import Dict, List

from method.gen_pages import gen_pages
from method.get_plain_dataframe import (
    get_plain_dataframe,
)

elements_dataframe: List[Dict] = get_plain_dataframe()
elements_full: List[Dict] = copy.deepcopy(elements_dataframe)
elements_completed: List[Dict] = list(
    filter(
        bool,
        [
            item_dict if item_dict["short_name"] != "" else None
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
                    - set(
                        [
                            (i["@type"], i["@id"])
                            for i in elements_completed
                        ]
                    )
                )
                else None
            )
            for item_dict in elements_dataframe
        ],
    )
)

elements_completed_sorted = sorted(
    elements_completed,
    key=lambda x: (x["addr:province"], x["short_name"], x["@id"]),
    reverse=True,
)
elements_uncompleted_sorted = sorted(
    elements_uncompleted, key=lambda x: x["@id"]
)
# from pprint import pprint
# pprint(universities_full)
print(
    len(elements_completed_sorted),
    "+",
    len(elements_uncompleted_sorted),
    "=",
    len(elements_full),
)

# TODO
# 1. 对short_name进行查重，出现重复的时候自动加粗标红
# 2. 自动识别母体大学，合并多个校区代码不会重复出现
# 3. 在英文名中自动识别简称可能来自的字母（首字母大写）并给出加粗该字母的建议。（可能比较困难）

gen_pages(elements_completed_sorted, elements_uncompleted_sorted)
