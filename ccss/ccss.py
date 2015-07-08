"""
    ccss
    ~~~~

    Function to compress CSS

    :copyright: (c) 2012 by Thomas Skaflem.
    :license: BSD, see LICENSE for more details.
"""
import re


def compress_css(css):
    """Compress CSS code by removing comments, white-spaces, surplus
    characters and empty rules.

    Will lower case all hex values and shorten them where possible,
    condense margin and padding, multidimensional zeros, floating points
    and zero units, convert RGB colors to HEX and wrap CSS lines.

    :param css: the Cascading Style Sheets code to compress.
    """
    regexps = {
        # Lowercase everything between the curly braces.
        r"(\{(.*?)\})": lambda lower: "%s" % lower.group(1).lower(),
        # Remove spaces from before things.
        r"\s+([!{};:>+\(\)\],])": r"\1",
        # Remove spaces from after things.
        r"([!{}:;>+\(\[,])\s+": r"\1",
        # Condense padding and margin.
        r"(padding|margin)\s*?:\s*?([^;]+?)(?:\s+\2)+(;|})": r"\1:\2\3",
        # Condense zero units. Replace `0(px, em, %, etc)` with `0`.
        r"([\s:])(0)(px|em|%|in|cm|mm|pc|pt|ex)": r"\1\2",
        # Condense multiple adjacent whitespace characters into one.
        r"\s+": " ",
        # Remove leading space.
        r"^ ": "",
        # Condense multiple adjacent semicolon characters into one.
        r";;+": ";",
        # Condense floating points. Replace `0.5` with `.5` where possible.
        r"(:|\s)0+\.(\d+)": r"\1.\2",
        # Condense multidimensional zeros.
        r"(:0 0 0 0|:0 0)+;": ":0;",
        # Remove both double or single quotes in url().
        r"url\((['\"])([^)]*)\1\)": r"url(\2)",
        # Shorten 6-digit hex color codes to 3-digits whenever possible.
        r"#((?i)[0-9a-fA-F])\1((?i)[0-9a-fA-F])\2((?i)[0-9a-fA-F])\3": r"#\1\2\3",
        # Convert RGB to HEX. `255, 255, 255` -> `#ffffff`.
        r"rgb\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)": lambda s:
        "#%02x%02x%02x" % (eval(s.group(1)), eval(s.group(2)), eval(s.group(3))),
        # Remove empty rules.
        r"[^\}\{]+\{\}": "",
        # Remove all CSS comment blocks.
        r"/\*[\s\S]*?\*/": "",
        # Remove unnecessary semicolons.
        r";\}": "}",
        # If there is a `@charset`, then only allow one, and move to the beginning.
        r"^(\s*@charset [^;]+;\s*)+": r"\1",
        # Remove excess commas between selectors and declaration.
        r"(\s*?)(,*)\s*?{": r"\1{",
    }

    for pattern, replace in regexps.items():
        css = re.sub(pattern, replace, css)

    # Revert `background-position:0;` to the valid `background-position:0 0;`.
    css = css.replace("background-position:0;", "background-position:0 0;")
    # Put the space back in for a few cases, such as:
    # `@media screen and (-webkit-min-device-pixel-ratio:0)`.
    css = css.replace(" and(", " and (")

    return css
