import copy
import json
import os
from typing import Dict, List

from method.const import NOT_PROFILE_NAME
from method.gen_pages import gen_pages
from method.get_plain_dataframe import get_plain_dataframe

FEATURE_BATCH = False

def single_run(profile_name="", clustering: bool = False):
    def get_profile(profile_name: str) -> dict:
        if profile_name == None or profile_name == "":
            profile_name = "hx.gov.miit.registry.post.json"
        profile_file = open(
            "../assets/profile/" + profile_name, "r", encoding="utf-8"
        )
        profile = json.loads(profile_file.read())
        profile_file.close()
        return profile

    def get_elements_dataframe() -> List[Dict]:
        return get_plain_dataframe(
            {
                "key": get_profile(profile_name)["data"]["key"],
                "type": get_profile(profile_name)["data"]["type"],
                "poly": get_profile(profile_name)["data"]["poly"],
            }
        )

    elements_dataframe = (
        get_elements_dataframe()
    )  # To avoid multiple tile's network query.

    def elements_full() -> List[Dict]:
        return copy.deepcopy(elements_dataframe)

    def elements_completed() -> List[Dict]:
        def detect_conform_vital_key(
            item_dict, vital_key_list: List[str]
        ) -> bool:
            flag_conform = True
            for vital_key in vital_key_list:
                if item_dict.get(vital_key) == "":
                    flag_conform = False
                    break
            return flag_conform

        vital_key_list = get_profile(profile_name)["data"]["vital_key"]

        return list(
            filter(
                bool,
                [
                    (
                        item_dict
                        if detect_conform_vital_key(
                            item_dict=item_dict, vital_key_list=vital_key_list
                        )
                        else None
                    )
                    for item_dict in elements_dataframe
                ],
            )
        )

    def elements_uncompleted() -> List[Dict]:
        return list(
            filter(
                bool,
                [
                    (
                        item_dict
                        if (item_dict["@type"], item_dict["@id"])
                        in list(
                            set(
                                [
                                    (i["@type"], i["@id"])
                                    for i in elements_full()
                                ]
                            )
                            - set(
                                [
                                    (i["@type"], i["@id"])
                                    for i in elements_completed()
                                ]
                            )
                        )
                        else None
                    )
                    for item_dict in elements_dataframe
                ],
            )
        )

    def detect_langid(working_data: List[dict]) -> List[dict]:
        # print("FEATURE_LANG_SORT")
        from langdetect import detect

        pure_name_list = [
            (
                i.get("name")
                if (i.get("name") != "" and i.get("name") != None)
                else "暂无"
            )
            for i in working_data
        ]
        print(pure_name_list)
        for i in range(len(pure_name_list)):
            pure_name_list[i] = detect(pure_name_list[i])
        extend_element_completed = []
        normal_elements_completed = working_data
        for i in range(len(normal_elements_completed)):
            new_item = normal_elements_completed[i]
            new_item["@langid"] = pure_name_list[i]
            # print(new_item)
            extend_element_completed.append(new_item)
        # from pprint import pprint
        # pprint(extend_element_completed)

        return extend_element_completed

    def get_sort_order() -> List[str]:
        return get_profile(profile_name)["data"]["sort_key"]

    def elements_sort(elements_unsorted):

        default_sort_lang = "ja"
        elements_to_sort = (
            detect_langid(elements_unsorted)
            if "@langid" in get_sort_order()
            else elements_unsorted
        )
        
        return sorted(
            elements_to_sort,
            key=lambda x: tuple(
                list(
                    [x.get("@langid", default_sort_lang)]
                    + [x.get(key) for key in get_sort_order()]
                )
            ),
            reverse=True,
        )

    def get_clustering() -> List[str]:
        full_data = elements_full()
        clustered_data = list(
            set([slice.get("name", "None") for slice in full_data])
        )
        return "\n".join(clustered_data)

    print(
        len(elements_sort(elements_completed())),
        "+",
        len(elements_sort(elements_uncompleted())),
        "=",
        len(elements_full()),
    )

    if get_profile(profile_name)["data"].get("clustering", False):
        # print("☆" * 10, "\n", get_clustering(), "\n", "★" * 10)
        gen_pages(
            elements_sort(elements_completed()),
            elements_sort(elements_uncompleted()),
            template_file_name=get_profile(profile_name)["page"]["template"],
            dst_file_name=get_profile(profile_name)["id"],
            optional_data={
                "page_title": get_profile(profile_name)["page"]["title"],
                "clustered_data": get_clustering(),
            },
        )
    else:
        gen_pages(
            elements_sort(elements_completed()),
            elements_sort(elements_uncompleted()),
            template_file_name=get_profile(profile_name)["page"]["template"],
            dst_file_name=get_profile(profile_name)["id"],
            optional_data={
                "page_title": get_profile(profile_name)["page"]["title"]
            },
        )


if FEATURE_BATCH == False:
    single_run()
else:
    ignore_filename_list = NOT_PROFILE_NAME

    for profile in list(
        filter(
            bool,
            [
                profile if profile[0] != "_" else ""
                for profile in os.listdir("../assets/profile/")
            ],
        )
    ):
        print(profile)
        if profile not in ignore_filename_list:
            single_run(profile_name=profile)

    os.system("python publish_bundle.py")
