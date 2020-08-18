from operator import itemgetter
import fitz
import json
import operator

# get bold, uppercase, texts by font size
def get_bold_uppercase_font_size_texts(page, font_size):
    blocks = page.getText("dict", flags=11)["blocks"]
    # create a list contains texts
    texts = []
    for b in blocks:  # iterate through the text blocks
        for l in b["lines"]:  # iterate through the text lines
            for s in l["spans"]:  # iterate through the text spans'
                if (s["flags"] & 2 ** 4) and (s["size"] == font_size) and (s["text"].isupper()) and (s["text"] != ' '):
                    texts.append(s["text"])
    return texts

# get bold texts by font size
def get_bold_font_size_texts(page, font_size):
    blocks = page.getText("dict", flags=11)["blocks"]
    # create a list contains texts
    texts = []
    for b in blocks:  # iterate through the text blocks
        for l in b["lines"]:  # iterate through the text lines
            for s in l["spans"]:  # iterate through the text spans
                if (s["flags"] & 2 ** 4) and (s["size"] == font_size) and (s["text"] != ' '):
                    texts.append(s["text"])
    return texts

# get sans or serifed texts by font size
def get_sans_or_serifed_font_size_texts(page, font_size):
    blocks = page.getText("dict", flags=11)["blocks"]
    # create a list contains texts
    texts = []
    for b in blocks:  # iterate through the text blocks
        for l in b["lines"]:  # iterate through the text lines
            for s in l["spans"]:  # iterate through the text spans
                if (s["flags"] & 2 ** 2) or (s["flags"] & 2 ** 3) and (s["size"] == font_size) and (s["text"] != ' '):
                    texts.append(s["text"])
    return texts

# get uppercase texts by font size
def get_uppercase_font_size_texts(page, font_size):
    blocks = page.getText("dict", flags=11)["blocks"]
    # create a list contains texts
    texts = []
    for b in blocks:  # iterate through the text blocks
        for l in b["lines"]:  # iterate through the text lines
            for s in l["spans"]:  # iterate through the text spans'
                if (s["size"] == font_size) and (s["text"].isupper()) and (s["text"] != ' '):
                    texts.append(s["text"])
    return texts

# get underline, uppercase texts by font size
#######

# get texts by font size
def get_font_size_texts(page, font_size):
    blocks = page.getText("dict", flags=11)["blocks"]
    # create a list contains texts
    texts = []
    for b in blocks:  # iterate through the text blocks
        for l in b["lines"]:  # iterate through the text lines
            for s in l["spans"]:  # iterate through the text spans'
                if (s["size"] == font_size) and (s["text"] != ' '):
                    texts.append(s["text"])
    return texts

# get title
def get_title(page):
    # read page text as a dictionary, suppressing extra spaces in CJK fonts
    blocks = page.getText("dict", flags=11)["blocks"]
    # create a list contains font size
    font_size = []
    for b in blocks:  # iterate through the text blocks
        for l in b["lines"]:  # iterate through the text lines
            for s in l["spans"]:  # iterate through the text spans
                font_size.append(s["size"])
    font_size = list(dict.fromkeys(font_size))
    # check font size list
    if len(font_size) < 1:
        return "The file doesn't have any text"
    if len(font_size) == 1:
        return find_title(page, font_size[0])
    if len(font_size) == 2:
        # create a dic contains fonts and count
        fonts_counts = {}
        # find the most use font
        for run in font_size:
            # create a count variable
            count = 0
            for b in blocks:  # iterate through the text blocks
                for l in b["lines"]:  # iterate through the text lines
                    for s in l["spans"]:  # iterate through the text spans
                        if (s["text"] != ' ') and (s["size"] == run):
                            count = count + 1
            if count != 0:
                fonts_counts[run] = count
        # get the most use font_size
        most_use_font_size = max(fonts_counts.items(), key=operator.itemgetter(1))[0]
        return find_title(page, most_use_font_size)

    elif len(font_size) > 2:
        # create a dic contains fonts and count
        fonts_counts = {}
        # find the most use font
        for run in font_size:
            # create a count variable
            count = 0
            for b in blocks:  # iterate through the text blocks
                for l in b["lines"]:  # iterate through the text lines
                    for s in l["spans"]:  # iterate through the text spans
                        if (s["text"] != ' ') and (s["size"] == run):
                            count = count + 1
            if count != 0:
                fonts_counts[run] = count

        # get the most use font_size
        most_use_font_size = max(fonts_counts.items(), key=operator.itemgetter(1))[0]
        fonts_counts.pop(most_use_font_size)

        if most_use_font_size == max(font_size):
            return find_title(page, most_use_font_size)
        else:
            # create a new dic contains fonts and count
            font_and_count = {}
            for key in fonts_counts:
                if key > most_use_font_size:
                    font_and_count[key] = fonts_counts[key]
            if font_and_count:
                most_use_font_size = max(font_and_count.items(), key=operator.itemgetter(1))[0]
                return find_title(page, most_use_font_size)
            else:
                return find_title(page, most_use_font_size)

# find title
def find_title(page, font_size):
    # underline and uppercase texts condition
    #-------
    # condition
    if get_bold_uppercase_font_size_texts(page, font_size):
        return list2String(get_bold_uppercase_font_size_texts(page, font_size))
    # condition
    elif get_uppercase_font_size_texts(page, font_size):
        return list2String(get_uppercase_font_size_texts(page, font_size))
    # condition
    elif get_bold_font_size_texts(page, font_size):
        return list2String(get_bold_font_size_texts(page, font_size))
    # condition
    elif get_sans_or_serifed_font_size_texts(page, font_size):
        return list2String(get_sans_or_serifed_font_size_texts(page, font_size))
    # condition
    elif get_font_size_texts(page, font_size):
        return list2String(get_font_size_texts(page, font_size))

# list2String
def list2String(l):
    title = ''
    for run in l:
        if run != ' ' or run != '  ' or run != '   ' or run != '    ' or run != '     ':
            title = title + run + ' '
    return title

# main functiom
def main():
    # file path here
    doc = fitz.open('F:/WORKS/Get title from pdf/file_test/FAA FAAG06 Guidelines.pdf')
    # get the first page
    page = doc[0]
    print(get_title(page))


if __name__ == '__main__':
    main()