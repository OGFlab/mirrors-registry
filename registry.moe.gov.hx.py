original_query_result="""@type|@id|amenity|name|name:en|short_name|addr:province|operator
way|2048453|university|Główna Jednostka Sił Mundurowych Nothinglandu||||
***
relation|348353|university|国立上京大学|National Shangjing University|NSJU||
"""

header = original_query_result.split("\n")[0].split("|")
query_result = original_query_result.replace(str("|".join(header) + "\n"), "")

result_list = list(
    filter(
        bool,
        [
            item_dict if item_dict["short_name"] != "" else None
            for item_dict in [
                dict(zip(header, item.split("|")))
                for item in list(filter(bool, query_result.split("\n")))
            ]
        ],
    )
)

from pprint import pprint

pprint(result_list)
pprint(len(result_list))
