import subprocess

def markdown_to_fortran(md_text, strip_blanks=False, comment_char="!! "):
    """
    Converts a string of Markdown text into Fortran code. Lines that are not part of 
    a Fortran code block (enclosed with ```fortran and ```) are treated as comments.

    Args:
        md_text (str): The input Markdown text.
        strip_blanks (bool, optional): If True, blank lines are removed from the output.
            Default is False, which retains all lines.
    Returns:
        str: The resulting Fortran code as a string.
    """
    lines = md_text.split('\n')
    in_code_block = False
    fortran_lines = []
    for line in lines:
        line = line.rstrip()  # remove trailing whitespace
        if line.lower() == "```fortran":
            in_code_block = True
            continue  # skip this line
        elif line == "```":
            in_code_block = False
            continue  # skip this line
        if not in_code_block:
            # add !! to non-Fortran lines
            line = comment_char + line
        if not (strip_blanks and line == ''):
            fortran_lines.append(line)
    return '\n'.join(fortran_lines)

def markdown_file_to_fortran_file(md_filename, fortran_filename):
    in_code_block = False
    with open(md_filename, 'r') as md_file, open(fortran_filename, 'w') as fortran_file:
        for line in md_file:
            line = line.rstrip()  # remove trailing whitespace
            if line == "```fortran":
                in_code_block = True
                continue  # skip this line
            elif line == "```":
                in_code_block = False
                continue  # skip this line
            if not in_code_block:
                # add !! to non-Fortran lines
                line = '!! ' + line
            fortran_file.write(line + '\n')

def compile_and_run_fortran_on_windows(code, compiler="gfortran", filename='temp.f90',
    run=True, title="", output_title = "output:\n"):
    """
    Writes Fortran code to a file, compiles it, and runs the resulting 
    executable on Windows. If any step fails, it prints an error message and returns.

    Args:
        code (str): The Fortran code to be written to a file, compiled, and executed.
        filename (str, optional): The name of the file to which the Fortran code is
                                  written. Defaults to 'temp.f90'.
        run (boolean, optional): whether to run generated executable
    """
    print(title)
    # write the code to a file
    with open(filename, 'w') as f:
        f.write(code)
    result = subprocess.run([compiler, filename, '-o', 'output.exe'], text=True,
        capture_output=True)
    # check for compilation errors
    if result.returncode != 0:
        print(f'Compilation failed with the following output:\n{result.stderr}')
        return
    if run:
        result = subprocess.run(['.\output.exe'], text=True, capture_output=True)
        if result.returncode != 0:
            print(f'Execution failed with the following output:\n{result.stderr}')
            return
        # print the output
        print(output_title + result.stdout)
