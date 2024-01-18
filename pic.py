from AppKit import NSPasteboard, NSPasteboardTypePNG
from PIL import Image
from io import BytesIO  # 添加这一行
import subprocess


def get_clipboard_image():
    # 获取剪贴板实例
    clipboard = NSPasteboard.generalPasteboard()

    # 检查剪贴板是否包含图像数据
    if NSPasteboardTypePNG in clipboard.types():
        # 获取图像数据
        image_data = clipboard.dataForType_(NSPasteboardTypePNG)

        # 将图像数据转为 Image 对象
        image = Image.open(BytesIO(image_data))
        return image
    else:
        print("剪贴板上没有图像数据")


def open_with_preview(image):
    # 保存图像到临时文件
    temp_path = "/tmp/clipboard_image.png"
    image.save(temp_path)

    # 使用预览应用程序打开图像
    subprocess.run(["open", "-a", "Preview", temp_path])


if __name__ == "__main__":
    clipboard_image = get_clipboard_image()
    if clipboard_image:
        open_with_preview(clipboard_image)
