import fitz  # PyMuPDF
import sys

# 添加边距

def add_margin_to_pdf(input_path, output_path, margin_inches=-1):
    # 打开PDF文件
    pdf_document = fitz.open(input_path)

    # 创建一个新的PDF文档
    new_pdf_document = fitz.open()

    first = True

    for page_number in range(pdf_document.page_count):
        # 获取当前页
        page = pdf_document[page_number]

        # 获取页面的宽度和高度
        original_width = page.rect.width
        original_height = page.rect.height

        if margin_inches == -1:
            margin_inches = original_width / 72 / 2

        # 计算添加边距后的新宽度和高度
        new_width = original_width + margin_inches * 72  # 1英寸 = 72点
        new_height = original_height

        if first:
            print(
                "original_width: ", original_width, "original_height: ", original_height
            )
            print("new_width: ", new_width, "new_height: ", new_height)
            first = False

        # 在新文档中创建一个带有边距的页面
        new_page = new_pdf_document.new_page(width=new_width, height=new_height)

        # 将原始页面内容复制到新页面中间
        x_offset = (new_width - original_width) / 2
        rect = fitz.Rect(
            0 + x_offset,
            0,
            original_width + x_offset,
            original_height,
        )
        new_page.show_pdf_page(rect, pdf_document, page_number)

    # 保存新的PDF文件，并使用压缩选项
    new_pdf_document.save(output_path, garbage=4, deflate=True, clean=True)
    new_pdf_document.close()
    pdf_document.close()


if __name__ == "__main__":
    input_pdf_path = sys.argv[1]
    output_pdf_path = sys.argv[2]
    if len(sys.argv) == 4:
        margin_inches = float(sys.argv[3])
    else:
        margin_inches = -1
    add_margin_to_pdf(input_pdf_path, output_pdf_path, margin_inches)
