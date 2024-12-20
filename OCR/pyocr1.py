from PIL import Image
import sys
import os
import pyocr
import pyocr.builders

os.chdir(os.path.dirname(__file__)) #設定目前目錄為工作目錄

tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)
tool = tools[0]  #取得可用工具

txt = tool.image_to_string(
    Image.open('test.jpg'),
    builder=pyocr.builders.TextBuilder()
)
print("result=",txt)
