import PyPDF2


def main():
    file = open("../stats/adams.PDF", "rb")

    pdf = PyPDF2.PdfFileReader(file)

    print(pdf.getPage(0).extractText())

    file.close()

main()
