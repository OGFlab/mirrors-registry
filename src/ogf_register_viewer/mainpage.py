import yaml
from jinja2 import Template

# 读取YAML文件
with open("../assets/profile/_index.yaml", "r", encoding="utf-8") as file:
    data = yaml.safe_load(file)


# 准备一个函数，递归地处理YAML数据，并生成带有层级关系的链接列表
def generate_links(d, hosting_path="", prefix=""):
    links = []
    for k, v in d.items():
        if isinstance(v, dict):
            # 递归处理子字典
            links.extend(generate_links(v, hosting_path, f"{prefix}{k}/"))
        elif isinstance(v, list) and len(v) > 0 and isinstance(v[0], dict):
            for item in v:
                # 提取名字和配置文件名
                name = item.get("name", "")
                profile = item.get("profile", "")
                # 添加到链接列表
                links.append(
                    {
                        "name": name,
                        "url": f"https://{hosting_path}{prefix}{profile}",
                        "depth": prefix.count("/"),  # 用于确定层级
                    }
                )
    return links


hosting_path = "your-hosting-path"  # 替换为你的主机路径
profiles_list = generate_links(data, hosting_path)

# 使用Jinja2渲染模板
template_file = open(
    "../assets/template/mainpage.jinja2", "r", encoding="utf-8"
)
template_str = template_file.read()
template_file.close()
template = Template(template_str)
output = template.render(
    profiles=profiles_list, gen_time="2023-11-09 10:00:00"
)

# 输出到文件或直接返回给浏览器
with open("../../dist/mainpage.html", "w", encoding="utf-8") as file:
    file.write(output)
