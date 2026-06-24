"""
This file is part of Goodreads Exporter.
This file contains the required regex patterns to successfully parse the book title
string that goodreads_export.csv contains.
"""

import re

""" This rule handles """
RULE_1 = re.compile(
    r"^(?P<Title>[\w\s'.,-]+?)(?:$|(?P<HasSeries>\s\()"
    r"(?(HasSeries)(?:(?P<SN1>[\w\s'&:-]+?)"
    r"(?:(?:,?\s#|,?\sBook\s)(?P<N1>\d+(?:-\d)?"
    r"(?:\.\d)?)?(?:(,\s(?P<N2>\d+(?:\.\d)?))?,\s"
    r"(?P<N3>\d+(?:\.\d)?))?)?[)])))",
    flags=re.MULTILINE | re.IGNORECASE,
)

RULE_2 = re.compile(
    r"^(?=.*book)(?P<Title>[\w\s'-]+.*)"
    r"(?::\s|\s[(]+)(?P<SN1>[\s\w]+)(,\s|\s)book\s"
    r"(?P<N1>[\w.]+)\)?$",
    flags=re.MULTILINE | re.IGNORECASE,
)

RULE_3 = re.compile(
    r"^(?P<Title>[\w\s'.,:#-]+?)(?:$|(?P<HasSeries>\s+\()"
    r"(?(HasSeries)(?:(?P<SN1>[\w\s'&:-]+?)"
    r"(?:(?:,?\s#|,?\sBook\s)(?P<N1>\d+(?:-\d)?"
    r"(?:\.\d)?)?(?:(,\s(?P<N2>\d+(?:\.\d)?))?,\s"
    r"(?P<N3>\d+(?:\.\d)?))?)?[)])))",
    flags=re.MULTILINE | re.IGNORECASE,
)

# Crossover books like Will Trent/Jack Reacher/Forgotten realm part of multiple series
RULE_4 = re.compile(
    r"(?P<Title>.*)\s\((?:(?P<ForgottenRealms>Forgotten\sRealms):\s)?"
    r"(?P<SN1>.*), #(?P<SN1N>\d(?:\.\d)?);\s(?P<SN2>.*)"
    r",\s#(?P<SN2N>\d+(?:\.\d+)?)\)",
    flags=re.MULTILINE | re.IGNORECASE,
)

RULE_Z = re.compile(
    r"^(?P<Title>[\w\s'.,:-]+)(?P<HasSeries>\s\()"
    r"(?(HasSeries)((?P<SeriesName>[\w\s'&:0-9-]+)(,?\s#(?P<SeriesNumber1>\d+(-\d)?"
    r"(?:\.\d)?)?(,\s(?P<SeriesNumber2>\d+(?:\.\d)?),\s(?P<SeriesNumber3>\d+(?:\.\d)?))?"
    r")?[)])$|$)",
    flags=re.MULTILINE | re.IGNORECASE,
)

TITLE_ONLY = re.compile(
    r"^(?!.*[:#()])(?P<Title>.*)$", flags=re.IGNORECASE | re.MULTILINE
)

ADDITIONAL_AUTHOR = re.compile(
    r"^(?P<name>.+?)(?:\s+(?:\(|-\s+)"
    r"((?P<type>editor|translator)|(?P<narrator>narrator)"
    r")?\)?)?$",
    flags=re.MULTILINE | re.IGNORECASE,
)

AUTHOR_NAME = re.compile(
    r"(?:(?P<first_name>.*?)\s+)?(?P<last_name>[\w'-]+(?:\s+Jr\b\.?)?)",
    flags=re.IGNORECASE,
)
