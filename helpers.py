import re
from string import ascii_lowercase
from flask import redirect, render_template, request, session

# create alphabet dictionary
alpha_dict = dict(zip(list(range(0, 26)), list(ascii_lowercase)))
# assign {-1; " "} to avoid the overlap when adding "step"
alpha_dict[-1] = " "

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=escape(message), bottom=code), code

# pattern of a typical word
w_pattern = "(?!\s)(\w+)(((?!\s)(\W)?)\w+)?"

# Check number of words in the string
def check(inp):
    #num = sum(1 for i in re.finditer(w_pattern, inp))
    num, e = 0, 0
    inp = inp.replace("*", "")
    for match in re.finditer(w_pattern, inp):
        # call the ending position of the ending letter of the word
        e = match.end()
        num += 1
        # Break at # words = 100, record the appropriate number of words to convert
        if num == 100:    
            return inp[ :(e+2)]
    return inp

def convert(text, step):
        inp_data = [ord(c.lower()) - 97 if (c.isalpha() == True) else c for c in text]
        out_data = list()
        for i in inp_data:
            if isinstance(i, str) == True:
                out_data.append(i)
            else:
                out_data.append(alpha_dict[(i + step) % 26])
        # Return a string
        return "".join(out_data)