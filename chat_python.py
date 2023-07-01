import subprocess
import openai

def ask_gpt(query, gpt_model = "gpt-3.5-turbo-0613"):
    """ return the reply of ChatGPT to `query` """
    completion = openai.ChatCompletion.create(model=gpt_model,
    messages=[{"role": "user", "content": query}])
    return completion.choices[0].message.content
    
def markdown_to_python(md_text, strip_blanks=False, comment_char="## ",
    code_only=True):
    """
    Converts a string of Markdown text into Python code. Lines that are not part of 
    a Python code block (enclosed with ```python and ```) are treated as comments.

    Args:
        md_text (str): The input Markdown text.
        strip_blanks (bool, optional): If True, blank lines are removed from the output.
            Default is False, which retains all lines.
    Returns:
        str: The resulting Python code as a string.
    """
    if "```" not in md_text:
        return md_text
    lines = md_text.split('\n')
    in_code_block = False
    python_lines = []
    for line in lines:
        line = line.rstrip()  # remove trailing whitespace
        if line.lower() == "```python":
            in_code_block = True
            continue  # skip this line
        elif line == "```":
            in_code_block = False
            continue  # skip this line
        if not in_code_block:
            if code_only:
                continue
            # add !! to non-Python lines
            line = comment_char + line
        if not (strip_blanks and line == ''):
            python_lines.append(line)
    return '\n'.join(python_lines)

def strip_blank_lines(text):
    """ remove blank lines from text """
    return "\n".join([line for line in text.splitlines()
        if line.strip()])
