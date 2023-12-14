import copy
from typing import Dict, List

from src.ogf_register_viewer.method.gen_pages import gen_pages
from src.ogf_register_viewer.method.get_plain_dataframe import (
    get_plain_dataframe,
)

universities_dataframe: List[Dict] = get_plain_dataframe()
universities_full: List[Dict] = copy.deepcopy(universities_dataframe)
universities_completed: List[Dict] = list(
    filter(
        bool,
        [
            item_dict if item_dict["short_name"] != "" else None
            for item_dict in universities_dataframe
        ],
    )
)
universities_uncompleted: List[Dict] = list(
    filter(
        bool,
        [
            (
                item_dict
                if (item_dict["@type"], item_dict["@id"])
                in list(
                    set([(i["@type"], i["@id"]) for i in universities_full])
                    - set(
                        [
                            (i["@type"], i["@id"])
                            for i in universities_completed
                        ]
                    )
                )
                else None
            )
            for item_dict in universities_dataframe
        ],
    )
)

# # Power saving but not elegant in my eye
# universities_uncompleted_temp: List[tuple] = list(
#     set([(i["@type"], i["@id"]) for i in universities_full])
#     - set([(i["@type"], i["@id"]) for i in universities_completed])
# )
# universities_uncompleted: List[Dict] = list(
#     filter(
#         bool,
#         [
#             (
#                 item_dict
#                 if (item_dict["@type"], item_dict["@id"])
#                 in universities_uncompleted_temp
#                 else None
#             )
#             for item_dict in universities_dataframe
#         ],
#     )
# )

universities_completed_sorted = sorted(
    universities_completed,
    key=lambda x: (x["addr:province"], x["short_name"], x["@id"]),
    reverse=True,
)
universities_uncompleted_sorted = sorted(
    universities_uncompleted, key=lambda x: x["@id"]
)
# from pprint import pprint
# pprint(universities_full)
print(
    len(universities_completed_sorted),
    "+",
    len(universities_uncompleted_sorted),
    "=",
    len(universities_full),
)

# TODO
# 1. 对short_name进行查重，出现重复的时候自动加粗标红
# 2. 自动识别母体大学，合并多个校区代码不会重复出现
# 3. 在英文名中自动识别简称可能来自的字母（首字母大写）并给出加粗该字母的建议。（可能比较困难）

gen_pages(universities_completed_sorted, universities_uncompleted_sorted)
