import os  # 导入os模块，用于处理文件路径
import shutil  # 导入shutil模块，用于文件操作
import xml.etree.ElementTree as Et  # 导入xml.etree.ElementTree模块，用于XML操作

def get_image_abs_path(image_path: str) -> str:
    """获取图片的绝对路径"""
    if image_path.startswith("/"):  # 如果图片路径已经是绝对路径
        return image_path  # 直接返回该路径
    cwd = os.getcwd()  # 获取当前工作目录
    return os.path.join(cwd, image_path)  # 返回图片的绝对路径

def get_assets_dir_abs_path() -> str:
    """获取assets文件夹的绝对路径"""
    return os.path.join(os.path.dirname(__file__), "xml")  # 返回xml文件夹在当前文件目录下的绝对路径

def get_assets_xml_abs_path(filename: str) -> str:
    """获取指定XML文件在assets文件夹下的绝对路径"""
    assets_dir_path = get_assets_dir_abs_path()  # 获取assets文件夹的绝对路径
    return os.path.join(assets_dir_path, filename)  # 返回指定XML文件的绝对路径

def get_tmp_xml_abs_path(filename: str) -> str:
    """获取临时XML文件在tmp文件夹下的绝对路径"""
    tmp_dir = os.path.join(os.getcwd(), "tmp")  # 设置临时文件夹路径
    os.makedirs(tmp_dir, exist_ok=True)  # 如果临时文件夹不存在，则创建
    return os.path.join(tmp_dir, filename)  # 返回临时XML文件的绝对路径

def make_terrain(xml_name: str, terrain_image_name: str):
    """生成地形XML文件"""
    assets_xml_path = get_assets_xml_abs_path(xml_name)  # 获取assets文件夹中指定XML文件的绝对路径
    tmp_xml_path = get_tmp_xml_abs_path(xml_name)  # 获取临时XML文件的绝对路径
    shutil.copyfile(assets_xml_path, tmp_xml_path)  # 复制assets文件夹中的XML文件到临时文件夹
    tmp_xml_file = Et.parse(tmp_xml_path)  # 解析临时XML文件
    root = tmp_xml_file.getroot()  # 获取XML文件的根节点
    image_abs_path = get_image_abs_path(terrain_image_name)  # 获取地形图片的绝对路径
    for child in root:
        if child.tag == "asset":  # 如果节点标签为"asset"
            hfield = child.find("hfield")  # 查找子节点"hfield"
            hfield.set("file", image_abs_path)  # 设置"hfield"节点的文件路径属性为地形图片的绝对路径
    tmp_xml_file.write(tmp_xml_path, encoding="UTF-8")  # 将修改后的临时XML文件写入文件
    print("make terrain successfully !")  
    return tmp_xml_path  # 返回生成的地形XML文件的绝对路径
