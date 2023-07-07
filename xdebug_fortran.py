import time
import openai
from fortran import markdown_to_fortran, debug_fortran, compile_and_run_fortran
from chat_python import ask_gpt

start = time.time()
openai.api_key = "my_key" # change to your key
gpt_model = "gpt-3.5-turbo-0613" # "gpt-4"
print_answer = True
print_raw_code = True
ntries = 4 # of times each task is attempted
max_tasks = 3
niter_fix = 3 # of times ChatGPT tries to fix code based on error messages
compile_and_run = True
compiler = "gfortran"
compiler_options = ["-Wall"]

print("gpt model:", gpt_model)
style = """ Set `integer, parameter :: dp = kind(1.0d0)` and declare real variables
as `real(kind=dp)`. Use :: in declarations.  Use implicit none on the 2nd line
and make sure to declare all variables. Name the program 'main`. You MUST use
```fortran to show the start of Fortran code. Use loop variables named i, j, k, and
remember to declare them if used."""

print("compiler:", compiler)
print("compiler options:", compiler_options)
print("style instructions:", style)

task_start = "Write a Fortran program to "

base_tasks = [
"estimate pi using Monte Carlo using 1000 samples.",
"""compute Euler's number in a variable called `euler` using a Taylor series with the number of terms
`nterms` equal to 1000.""",
"compute the prime numbers below 50."]

base_tasks = base_tasks[:max_tasks]

for base_task in base_tasks:
    task = task_start + base_task + style
    print("\n**task: " + task + "**\n")
    for itry in range(1, ntries+1):
        print("attempt", itry)
        answer = ask_gpt(task)
        if print_answer:
            print("\nanswer:\n", answer, sep="")
        fortran_code = markdown_to_fortran(answer, strip_blanks=True)
        if print_raw_code:
            print("\noriginal code from ChatGPT:\n" + fortran_code)
        fortran_code, errmsg = debug_fortran(fortran_code, compiler=compiler,
            compiler_options=compiler_options, niter_fix=niter_fix)
        if compile_and_run:
            compile_and_run_fortran(fortran_code, compiler=compiler,
                compiler_options=compiler_options)

print("\ntime elapsed (sec):", "%0.2f"%(time.time() - start), "for",
    len(base_tasks), "task(s) and", ntries, "tries each.")
