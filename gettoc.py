from bs4 import BeautifulSoup, NavigableString

with open("tipitaka2500.github.io/index.html", "r") as index:
    soup = BeautifulSoup(index, 'html.parser')

    main = soup.main
    menu = main.ul
    # print(menu.prettify())
    for li in menu.children:
        if (li.name == 'li'):
            if li.button:
                print(f"## {li.button.string.strip()}\n")
                subli = li.ul
                if subli.button:
                    for sli in subli.children:
                        if type(sli) is NavigableString:
                            continue
                        if sli.button:
                            print(f"### {sli.button.string.strip()}\n") 
                            subsubli = subli.ul
                            links = sli.find_all('a')
                            for link in links:
                                print(f"* [{link.string.strip()}]({link['href'][1:].replace('.html', '.md')})")
                            print('')
                else:
                    links = li.find_all('a')
                    for link in links:
                        print(f"* [{link.string.strip()}]({link['href'][1:].replace('.html', '.md')})")
                print('')
