import copy
import json
import os
from typing import Dict, List

from method.gen_pages import gen_pages
from method.get_plain_dataframe import get_plain_dataframe

MULTI_PROFILE_MODE = True


def single_run(profile_name=""):
    def get_profile(profile_name: str) -> dict:
        if profile_name == None or profile_name == "":
            # profile_name = "registry.moe.gov.hx.json"
            profile_name = "airports.mot.gov.hx.json"
        profile_file = open(
            "../assets/profile/" + profile_name, "r", encoding="utf-8"
        )
        profile = json.loads(profile_file.read())
        profile_file.close()
        return profile

    def get_elements_dataframe() -> List[Dict]:
        return get_plain_dataframe(
            {
                "key": get_profile(profile_name)["key"],
                "type": get_profile(profile_name)["type"],
                "poly": get_profile(profile_name)["poly"],
            }
        )

    elements_dataframe = (
        get_elements_dataframe()
    )  # To avoid multiple tile's network query.

    def elements_full() -> List[Dict]:
        return copy.deepcopy(elements_dataframe)

    def elements_completed() -> List[Dict]:
        return list(
            filter(
                bool,
                [
                    item_dict
                    if item_dict.get(get_profile(profile_name)["vital_key"])
                    != ""
                    else None
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

    def elements_completed_sorted():
        return sorted(
            elements_completed(),
            key=lambda x: (
                x.get("addr:province"),
                x.get("short_name"),
                x["@id"],
            ),
            reverse=True,
        )

    def elements_uncompleted_sorted():
        return sorted(elements_uncompleted(), key=lambda x: x["@id"])

    print(
        len(elements_completed_sorted()),
        "+",
        len(elements_uncompleted_sorted()),
        "=",
        len(elements_full()),
    )

    gen_pages(
        elements_completed_sorted(),
        elements_uncompleted_sorted(),
        template_file_name=get_profile(profile_name)["template_file_name"],
        optional_data={"page_title": get_profile(profile_name)["page_title"]},
    )


if MULTI_PROFILE_MODE == False:
    single_run()
else:
    for profile in os.listdir("../assets/profile/"):
        print(profile)
        single_run(profile_name=profile)
