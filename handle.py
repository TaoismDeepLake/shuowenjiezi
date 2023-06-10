import os
import re
from PIL import Image, ImageFont, ImageDraw
from fontTools.ttLib import TTFont

# 字体文件路径
font_path = "chongxi_seal.otf" 

# 加载字体
font = ImageFont.truetype(font_path, size=256)
ttfont = TTFont(font_path)

# 图像尺寸
image_size = (256, 256)

# 创建 output 和 output2 目录（如果不存在）
for dir_name in ["output", "output2"]:
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

# 读取字符列表
with open("input.txt", "r", encoding="utf-8") as file:
    characters = file.read().replace("\n", "").replace(" ", "")

# 读取输入文件
with open('input.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 字典映射“部”到其数字代号
bu_to_num = {}
count = 1

def char_in_font(Unicode_char, font):
    for cmap in font['cmap'].tables:
        if cmap.isUnicode():
            if ord(Unicode_char) in cmap.cmap:
                return True
    return False

# 遍历每一行数据
for line in lines:
    # 提取编号
    id_ = re.search(r'编号:(\d+)', line)
    if id_ is None:
        continue
    else:
        id_ = id_.group(1)

    # 提取部
    bu_ = re.search(r'(\w+)部', line)
    if bu_ is None:
        continue
    else:
        bu_ = bu_.group(1)
        if bu_ not in bu_to_num:
            bu_to_num[bu_] = str(count).zfill(4)
            count += 1

    # 创建 output2 的子目录（如果不存在）
    sub_dir = f'output2/6_bu_{bu_to_num[bu_]}'
    if not os.path.exists(sub_dir):
        os.makedirs(sub_dir)

    # 提取部后的字符
    char_after_bu = re.search(r'{}部\s+(\w)'.format(bu_), line)
    if char_after_bu is not None:
        char_after_bu = char_after_bu.group(1)
        # 检查字符是否在字体中
        if not char_in_font(char_after_bu, ttfont):
            continue

    # 提取从后的汉字
    from_words = re.findall(r'从(\w)', line)

    # 提取声前的汉字
    sound_words = re.findall(r'(\w)聲', line)

    # 提取切
    qie_words = re.findall(r'(\w+切)', line)
        
    # 将所有单词合并
    words = [bu_, bu_ + '部', char_after_bu] + from_words + sound_words + qie_words

    # 写入到 output 和 output2 的子目录的文件
    for output_dir in ['output', sub_dir]:
        with open(f'{output_dir}/ch_{str(id_).zfill(4)}.txt', 'w', encoding='utf-8') as f:
            f.write(','.join(words))

        # 创建图像并绘制字符
        image = Image.new("1", image_size, color=1)  
        draw = ImageDraw.Draw(image)
        # 检查字符是否在字体中
        if not char_in_font(char_after_bu, TTFont(font_path)):
            continue
        draw.text((0, 0), char_after_bu, font=font, fill=0)
        
        # 保存图像
        image_filename = f'{output_dir}/ch_{str(id_).zfill(4)}.png'
        image.save(image_filename)
