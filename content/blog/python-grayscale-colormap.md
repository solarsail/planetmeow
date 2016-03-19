Title: [Python] 为灰度数据应用颜色表（colormap）并绘制图例
Category: 技巧
Date: 2016-03-19 23:05
Tags: python, pil, aggdraw
Slug: python-apply-colormap-on-grayscale-data

Matplotlib可以自动为单通道数据应用颜色表并绘制图例，但是保存为图片时可能不满足细节要求，而需要使用PIL。创建应用颜色表的PIL图像，最简单的方法是利用`matplotlib.cm`库。

```python
from matplotlib import cm
from PIL import Image

...
# img_data 为单通道数据，已归一化至 [0, MAX_VALUE]
img_data = np.uint8(cm.jet(img_data / MAX_VALUE) * 255) # 应用 jet 颜色表
img = Image.fromarray(img_data)
```

为了能够表示颜色的具体含义，还需要添加图例。没有找到类似`matplotlib`的很简单的方法，所以采取手工绘制。

首先建立一个比需要增加图例的图像大一圈的底图，然后依次把原图像和图例添加上去。最后在原图像周围绘制边框。
假设图例尺寸为300x20。

```python
import aggdraw # 绘制抗锯齿线条和字符
from matplotlib import cm
from PIL import Image

def draw_colorbar(image):
    font_size = 16                         # 文字尺寸
    tick_pen = aggdraw.Pen('black', 1.0)   # 刻度颜色
    border_pen = aggdraw.Pen('white', 1.0) # 图框颜色
    font = aggdraw.Font('white', r"c:\windows\fonts\times.ttf", size=font_size) # 图例字体
    
    figure_size = (image.size[0] + 150, image.size[1] + 50) # 底图尺寸
    figure = Image.new('RGB', figure_size) # 底图
    legend = Image.new('RGB', (100, 350))  # 图例
    
    xorg = 20 # 原图像在底图上的原点
    yorg = 25
    bar = np.linspace(1, 0, 300)
    bar = bar.reshape(300, 1).repeat(20, 1) # 生成20像素宽的条带
    bar_data = np.uint8(cm.jet(bar) * 255)
    bar_img = Image.fromarray(bar_data)
    
    tick = np.linspace(MAX_VALUE, 0, 11)    # 刻度，共11个
    
    # 将条带粘贴到图例中
    legend.paste(bar_img, (xorg, yorg, bar_img.size[0]+xorg, bar_img.size[1]+yorg))
    # 绘制刻度和文字
    draw = aggdraw.Draw(legend)
    for t in tick:
        y = (MAX_VALUE - t) * 300 / MAX_VALUE
        # 为显示清晰的刻度线，需要绘制在半像素坐标上
        draw.line((15+xorg,y+yorg-0.5, 20+xorg,y+yorg-0.5), tick_pen) 
        draw.text((25+xorg, y+yorg-font_size/2), str(t), font)
    draw.flush() # aggdraw 需要此操作使绘制生效
    
    # 将原图粘贴到底图上
    image_boundary = (25, 25, 25+image.size[0], 25+image.size[1]) # 原图边界
    figure.paste(image, image_boundary)
    # 将图例粘贴到底图上
    legend_x = 30 + image.size[0]
    legend_y = (figure.size[1]-legend.size[1]) / 2
    figure.paste(legend, (legend_x, legend_y, legend_x+legend.size[0], legend_y+legend.size[1]))
    # 绘制边框
    draw = aggdraw.Draw(figure)
    draw.rectangle(image_boundary, border_pen)
    draw.flush()
    
    return figure
```
