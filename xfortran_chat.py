import time
import openai
from fortran import markdown_to_fortran, compile_and_run_fortran

start = time.time()
openai.api_key = "my_key" # change to your key
gpt_model = "gpt-3.5-turbo-0613" # "gpt-4"
print_answer = False
print_code = True
ntries = 2 # of times each task is attempted
run_exec = True
compiler = "gfortran"
compiler_options = ["-Wall"]
if "-c" in compiler_options:
    run_exec = False

print("gpt model:", gpt_model)
style = """ Set `integer, parameter :: dp = kind(1.0d0)` and declare real variables
as `real(kind=dp)`. Use :: in declarations.  Use implicit none on the 2nd line
and make sure to declare all variables. Name the program 'main`. You MUST use
```fortran to show the start of Fortran code. Use loop variables named i, j, k, and
remember to declare them if used."""

task_start = "Write a Fortran program to "

base_tasks = [
"""compute Euler's number in a variable called `euler` using a Taylor series with the number of terms
`nterms` equal to 1000.""",
"""compute the prime numbers below 50."""]

for base_task in base_tasks:
    task = task_start + base_task + style
    print("\n**task: " + task + "**\n")
    for itry in range(1, ntries+1):
        print("attempt", itry)
        completion = openai.ChatCompletion.create(model=gpt_model,
        messages=[{"role": "user", "content": task}])
        answer = completion.choices[0].message.content
        if print_answer:
            print("\nanswer:\n", answer, sep="")
        fortran_code = markdown_to_fortran(answer, strip_blanks=True)
        if print_code:
            print(fortran_code)
        compile_and_run_fortran(fortran_code, compiler=compiler, compiler_options=
            compiler_options, run=run_exec)

print("\ntime elapsed (sec):", "%0.2f"%(time.time() - start), "for",
    len(base_tasks), "tasks and", ntries, "tries each.")
