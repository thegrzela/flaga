def open_poem_ukr():
    text_lines = open('/var/www/flaga/dane/poem_ukr.txt', encoding='utf-8').readlines()

    poem_lines_ukr = []
    for line in text_lines:
        line = line.strip()
        poem_lines_ukr.append(line)
    
    return poem_lines_ukr