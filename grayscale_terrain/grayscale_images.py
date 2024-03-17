import os
import numpy as np
from PIL import Image


def perlin_noise(shape, scale=100, octaves=6, persistence=0.5, lacunarity=2.0):
    # 初始化一个形状为 shape 的全零数组用于存储噪声
    noise = np.zeros(shape)
    frequency = 1
    amplitude = 1
    # 循环生成不同频率的噪声并叠加
    for _ in range(octaves):
        noise += amplitude * generate_perlin_noise(shape, int(frequency))
        frequency *= lacunarity
        amplitude *= persistence
    # 将噪声数组归一化到 [-1, 1] 范围内
    return noise / np.max(np.abs(noise))
def generate_perlin_noise(shape, frequency):
    # 定义插值函数
    def interpolate(a, b, x):
        return a + (b - a) * (3 * x ** 2 - 2 * x ** 3)
    # 生成梯度向量
    def generate_gradient_vector(ix, iy):
        random = 2920 * np.sin(ix * 21942 + iy * 171324 + 8912) * np.cos(ix * 23157 * iy * 217832 + 9758)
        return np.cos(random), np.sin(random)
    # 计算格子数量和每个格子的像素数
    d = (shape[0] // frequency, shape[1] // frequency)
    p = (shape[0] / d[0], shape[1] / d[1])
    # 生成梯度向量网格
    ix0, iy0 = np.mgrid[0:frequency, 0:frequency]
    gradient = np.zeros((frequency, frequency, 2))
    for i in range(frequency):
        for j in range(frequency):
            gradient[i, j] = generate_gradient_vector(ix0[i, j], iy0[i, j])
    # 生成噪声地图
    noise_map = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            x = i / p[0]
            y = j / p[1]
            ix = int(x)
            iy = int(y)
            dx = x - ix
            dy = y - iy
            a = gradient[ix % frequency][iy % frequency]
            b = gradient[(ix + 1) % frequency][iy % frequency]
            c = gradient[ix % frequency][(iy + 1) % frequency]
            d = gradient[(ix + 1) % frequency][(iy + 1) % frequency]
            sx = interpolate(a[0], b[0], dx)
            sy = interpolate(c[0], d[0], dx)
            noise_map[i][j] = interpolate(sx, sy, dy)
    return noise_map

os.makedirs("images", exist_ok=True)
# 生成地形灰度图
terrain_noise = perlin_noise((500, 500), scale=100, octaves=6)
# 将噪声数组转换为图像，并保存为PNG格式
terrain_image = Image.fromarray((terrain_noise * 255).astype(np.uint8), mode='L')
terrain_image.save("images/terrain.png")
