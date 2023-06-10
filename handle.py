import os
import re
import os
from PIL import Image, ImageFont, ImageDraw

# 字体文件路径
font_path = "chongxi_seal.otf"  # 替换为你的字体文件路径

# 图像尺寸
image_size = (256, 256)

# 创建 output 目录（如果不存在）
if not os.path.exists("output"):
    os.makedirs("output")

# 读取字符列表
with open("input.txt", "r", encoding="utf-8") as file:
    characters = file.read().replace("\n", "").replace(" ", "")

# 加载字体
font = ImageFont.truetype(font_path, size=256)  # 替换为你的字体大小

# 读取输入文件
with open('input.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 遍历每一行数据
for line in lines:
    # 提取编号
    id_ = re.search(r'编号:(\d+)', line)
    if id_ is not None:
        id_ = id_.group(1)
        
        print(id_)

        # 提取部
        bu_ = re.search(r'(\w+)部', line)
        if bu_ is None:
            continue
        else:
            bu_ = bu_.group(1)
        
        # 提取部后的字符
        char_after_bu = re.search(r'{}部\s+(\w)'.format(bu_), line)
        if char_after_bu is not None:
            char_after_bu = char_after_bu.group(1)
            
        # 提取从后的汉字
        from_words = re.findall(r'从(\w)', line)

        # 提取声前的汉字
        sound_words = re.findall(r'(\w)聲', line)

        # 提取切
        qie_words = re.findall(r'(\w+切)', line)
        
        # 将所有单词合并
        words = [bu_, bu_ + '部', char_after_bu] + from_words + sound_words + qie_words
        
        # 写入到输出文件
        with open(f'output/ch_{str(id_).zfill(4)}.txt', 'w', encoding='utf-8') as f:
            f.write(','.join(words))

        image = Image.new("1", image_size, color=1)  # "1" 表示黑白图像，color=1表示初始背景为白色

        char = char_after_bu
        i = id_

        # 创建绘图对象
        draw = ImageDraw.Draw(image)

        # 在图像上绘制文本
        draw.text((0, 0), char, font=font, fill=0)  # fill=0表示文本颜色为黑色

        # 生成文件路径
        image_filename = f"output/ch_{str(i).zfill(4)}.png"
        # text_filename = f"output/ch_{str(i).zfill(4)}.txt"

        # 保存图像为PNG格式
        image.save(image_filename)

        # # 保存文本文件
        # with open(text_filename, "w", encoding="utf-8") as text_file:
        #     text_file.write(char)
