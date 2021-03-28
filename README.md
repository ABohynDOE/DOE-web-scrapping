# DOE-web-scrapping

Python code to collect information about journal publication over the year, using web-scrapping.
Informations collected are:

- Author name(s)
- DOI
- Year of publication
- Type of publication (Article, Book review, ...)
- Issue and volume of the journal
- Number of citations

The project only aims at design-of-experiments (DOE) oriented journals, therefore data are only collected in the following journals:

- Journal of Quality Technology (JQT)
- Technometrics (TCH)
- American Journal of the Statistical Association (ASA)
- Journal of Applied Statistics (JAS)
- Quality Engineering (QEN)

## Requirements

The following packages are required:

- `urllib`
- `BeautifulSoup`
- `requests`
- `pandas`
