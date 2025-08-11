def clean_line(line):
    line = line.strip()
    line = line.strip("\n")

    return line


def markdown_to_blocks(md):
    md = md.strip("\n")

    array = md.split("\n\n")

    array = list(map(clean_line, array))

    for i in range(len(array)):
        if array[i] == "":
            array.pop(i)

    # print(array)
    return array


if __name__ == "__main__":
    md = ""

    markdown_to_blocks(md)
