# confluence_export_with_jira_issue_images #

## Confluence with Jira lists with images print cleaner. ##

If you add a list of Jira issues with description onto a confulence page,
and,
there are images in the description.
then
The pdf export will not show those images.
[Jira support issue](https://jira.atlassian.com/browse/CONFSERVER-37123)

However, if you "save as html" of the page, then the images are there.
This code deletes out all of the extra page elements, so that you can open it in
the browser and save it as a clean PDF page.


## how to ##

1. Safe the page as html
2. Put this script in the same folder
3. Run the script. A copy of the HTML file will be made with only the desired content
4. open in firefox, print to PDF.
5. play around with the confulence page and this script until it works.
    For example: full-with jira tables on a normal widtch page will get cut off.
6. use the firefox/chrome inspect element functions to adjust as necessary