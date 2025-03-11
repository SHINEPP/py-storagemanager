from PyPDF2 import PdfReader, PdfWriter


def compress_pdf(input_path, output_path):
    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    with open(output_path, 'wb') as out:
        writer.write(out)


if __name__ == '__main__':
    in_pdf = '/Users/zhouzhenliang/Desktop/zhouz/wangwei.pdf'
    out_pdf = '/Users/zhouzhenliang/Desktop/zhouz/wangwei_out.pdf'
    compress_pdf(in_pdf, out_pdf)
