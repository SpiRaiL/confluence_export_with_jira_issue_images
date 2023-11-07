"""
Confluence with Jira lists print cleaner.

1. Safe the page as html
2. Put this script in the same folder
3. Run the script. A copy of the HTML file will be made with only the desired content
4. open in firefox, print to PDF.
5. play around with the confulence page and this script until it works.
    For example: full-with jira tables on a normal widtch page will get cut off.
6. use the firefox/chrome inspect element functions to adjust as necessary

uses python 3.
requires:
pip3 insrtall cssselect lxml
"""


import lxml.html
import glob
import re

# get all htm files
files = glob.glob("*.htm")

# for each file
for fname in files:
    #skip names starting with "output"
    if "output" in fname:
        continue
    print(fname)

    #get all the text out of the file
    f = open(fname,'+r', encoding="utf-8")
    html_txt = f.read()
    f.close

    #get all as html content
    content = lxml.html.fromstring(html_txt)

    #CSS select commands for things to remove from the page.
    # open the out
    css_to_remove = [
        "div[data-testid=grid-topNav]",         #the nav bar
        "div[data-testid=grid-left-sidebar]",   #the sidebar
        "div[data-skip-link-wrapper=true]",     #skip link bar
        "div[data-test-id=page-main-div]",      #the stuff under the title page
        "#AkBanner",                            #refresh the page header
        "#content-header-container",            #breadcrumb links etc
        ".new-file-experience-wrapper",         #click over image popups
        "#likes-and-labels-container",          #the page footer
        ".refresh-issues-bottom",               #refresh at bottoms of tables
        "button",                               #all the buttons and icons
    ]

    #loop over the above list and remove these elsements.
    for tag in css_to_remove:
        print("removing: %s" % tag)
        elements = content.cssselect(tag)

        for html_element in elements:
            # print(lxml.html.tostring(button))
            html_element.getparent().remove(html_element)

    #go into all the jira table and drop the horizontal scorlling
    # on the jira tables
    jira_issues = content.cssselect(".jira-issues")
    for jira_issue in jira_issues:
        jira_issue.set("style", "width: 100%;  overflow: visible;")


    #grab all the rendered blocks
    blocks = content.cssselect(".ak-renderer-extension")

    print("scaling the table widths to 1000px to avoid text overflow")
    for block in blocks:
        new_style =""
        style = block.get("style")
        pairs = style.split(";")
        for pair in pairs:
            if pair.strip():
                key, value = pair.split(":")
                if key == "width":
                    if "%" in value:
                        continue
                    new_value = int(value.replace("px",""))
                    if new_value > 1000:
                        new_value = 1000
                new_style = f"{key}: {new_value}px;"

        block.set("style", new_style)

    print("scaling down images to fit in the tables as necessary")
    images = content.cssselect("img")
    for image in images:
        width = image.get("width")
        height = image.get("height")
        if width is not None and int(width) > 680:
            image.set("width", "%s" % 680)
            image.set("height", "%s" % int(int(height)*680/int(width)))

    #convert it all back to a string and put it into a new file with "output" in the file name
    string = lxml.html.tostring(content).decode("utf8")
    f = open("output %s" % fname, '+w', encoding="utf-8")
    f.write(str(string))
    f.close()
