import os
import mujoco
import mujoco.viewer

import sys
sys.path.append(os.getcwd())

from grayscale_terrain.make_terrain_xml import make_terrain

# 生成随机地形灰度图 位于 grayscale_images.py 中，后续使用时需创建 一个类 方便管理和统一调用

# 根据灰度图生成mujoco地形
tmp_file = make_terrain("custom_terrain.xml","images/terrain0.png")

model = mujoco.MjModel.from_xml_path(tmp_file)
data = mujoco.MjData(model)

mujoco.viewer.launch(model)

