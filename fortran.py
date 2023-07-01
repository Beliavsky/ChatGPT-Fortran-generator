import subprocess
import re
import os
from chat_python import ask_gpt, strip_blank_lines
from util import truncated_string, save_numbered_file

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
    if "```" not in md_text:
        return extract_fortran_code(md_text)
    lines = md_text.split('\n')
    in_code_block = False
    fortran_lines = []
    for line in lines:
        line = line.rstrip()  # remove trailing whitespace
        if (line == "```" and not in_code_block) or line.lower() == "```fortran":
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

def compile_and_run_fortran(code, compiler="gfortran", compiler_options=
    ["-std=f2018","-Wall"], filename="temp.f90", run=True, title="",
    output_title = "output:\n", exec_name="a.exe", save_sources=True):
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
    if save_sources and os.path.exists(filename):
        save_numbered_file(filename)
    # write the code to a file
    with open(filename, "w") as f:
        f.write(code)
    result = subprocess.run([compiler, *compiler_options, filename, '-o', exec_name],
        text=True, capture_output=True)
    # check for compilation errors
    if result.returncode != 0:
        print(f'Compilation failed with the following output:\n{result.stderr}')
        return
    if run:
        result = subprocess.run([exec_name], text=True, capture_output=True)
        if result.returncode != 0:
            print(f'Execution failed with the following output:\n{result.stderr}')
            return
        # print the output
        print(output_title + result.stdout)

def compiler_output(code="", compiler="gfortran", compiler_options=
    ["-std=f2018","-Wall"], filename="temp.f90", exec_name="a.exe",
    save_sources=True):
    """ save code to a file and compile it """
    if code:
        if save_sources and os.path.exists(filename):
            save_numbered_file(filename)
        with open(filename, "w") as f:
            f.write(code)
    result = subprocess.run([compiler, *compiler_options, filename, "-o", exec_name],
        text=True, capture_output=True)
    return result

def debug_fortran(code, compiler="gfortran", compiler_options=["-std=f2018","-Wall"],
    niter_fix=1, gpt_model="gpt-3.5-turbo-0613", print_query=False,
    print_code_sent=False, print_gpt_output=False, run=True):
    """ get a Fortran code to compile by iteratively sending compiler error messages
    to ChatGPT and asking for fixes """
    new_code = code
    if print_code_sent:
        print("\ncode sent to debug_fortran:\n" + code)
    errmsg = ""
    for iter in range(1, niter_fix+1):
        print("\niteration ", iter, ":", sep="")
        errmsg = compiler_output(new_code, compiler,
            compiler_options=compiler_options).stderr.strip()
        if errmsg:
            print("error message:\n", errmsg)
            new_output = fix_fortran(new_code, errmsg)
            if print_gpt_output:
                print("\nresult from fix_fortran:\n" + new_output)
            new_code = markdown_to_fortran(new_output, strip_blanks=True)
            print("\nnew code:\n" + new_code)
        else:
            print("no compiler error messages\n")
            break
    if run:
        compile_and_run_fortran(new_code, compiler=compiler)
    return new_code, errmsg
        
def fix_fortran(code, errmsg=None, gpt_model="gpt-3.5-turbo-0613", print_query=False):
    query = "Fix the following Fortran code:\n" + code
    if errmsg:
        query = query + "\n\nerror message:\n" + errmsg
    if print_query:
        print("\nquery sent:\n" + query + "\nEND OF QUERY")
    return strip_blank_lines(ask_gpt(query, gpt_model=gpt_model))

def fix_run_fortran(code, ntries_unassisted=0, ntries_assisted=1, print_response=False,
    print_new_code=True, print_query=True, compile_new_code=True, run=True):
    """
    Process Fortran code by attempting unassisted and assisted fixing based on error messages.
    
    Args:
        code (str): The Fortran code to process.
        ntries_unassisted (int): Number of attempts for unassisted fixing without compiler error message.
        ntries_assisted (int): Number of attempts for assisted fixing with compiler error message.
        print_response (bool, optional): Whether to print the response from fixing attempts. Defaults to False.
        print_new_code (bool, optional): Whether to print the new code generated after fixing. Defaults to False.
        compile_new_code (bool, optional): Whether to compile and run the new code. Defaults to False.
        run (bool, optional): Whether to run generated executable. Defaults to True.
    """
    for itry in range(ntries_unassisted):
        response = fix_fortran(code, print_query=print_query)
        if print_response:
            print("\nresponse:\n" + response + "\n")
        new_code = markdown_to_fortran(response)
        if print_new_code:
            print("\nnew code:\n" + new_code)
        if compile_new_code:
            compile_and_run_fortran(new_code, run=run)
    compiler_result = compiler_output(code)
    errmsg = compiler_result.stderr.strip()
    if errmsg:
        print("\nerrmsg:\n" + errmsg)
    else:
        compile_and_run_fortran(code, run=run)
    if errmsg:
        for itry in range(ntries_assisted):
            response = fix_fortran(code, errmsg, print_query=print_query)
            if print_response:
                print("\nresponse:\n" + response + "\n")
            new_code = markdown_to_fortran(response)
            if print_new_code:
                print("\nnew code:\n" + new_code)
            if compile_new_code:
                compile_and_run_fortran(new_code, run=run)

def extract_fortran_code(text):
    """ return the Fortran code from a string, defined as the lines starting with `program`
    through the line starting with `end program`, case insensitive """
    # Define the regular expression pattern to match the Fortran code
    pattern = r"(?i)(?s)(program\b.*?\bend\s+program\b).*"
    # Find the first match of the pattern in the input string
    match = re.search(pattern, text)
    if match:
        # Extract the matched Fortran code
        fortran_code = match.group(1).strip()
        return fortran_code
    else:
        return ""

def run_exec(exec_name, print_stderr=True, print_stdout=True):
    """ run an executable and return the return code """
    result = subprocess.run([exec_name], text=True, capture_output=True)
    if result.returncode != 0 and print_stderr:
        errmsg = truncated_string(result.stderr, "Error termination").strip()
        print(f'Execution failed with the following output:\n{errmsg}')
    if print_stdout:
        print(result.stdout)
    return result.returncode

def run_exec_debug_fortran(exec_name, code, print_stderr=True, print_stdout=True,
    print_response=False):
    """ run an executable and debug code if it crashes """
    result = subprocess.run([exec_name], text=True, capture_output=True)
    if result.returncode != 0 and print_stderr:
        run_time_errmsg = truncated_string(result.stderr, "Error termination").strip()
        print(f'Execution failed with the following output:\n{run_time_errmsg}')
        new_output = fix_fortran(code, run_time_errmsg)
        if print_response:
            print("\nresult from fix_fortran():\n" + new_output)
        new_code = markdown_to_fortran(new_output, strip_blanks=True)
    else:
        new_code = code
        if print_stdout:
            print("\nprogram output:\n" + result.stdout)
    return result.returncode, new_code
