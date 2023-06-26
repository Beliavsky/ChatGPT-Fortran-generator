import time
import openai
from fortran import markdown_to_fortran, compile_and_run_fortran_on_windows

start = time.time()
openai.api_key = "my_key" # change to your OpenAI key
print_answer = False
print_code = True
ntries = 10

style = """ Set `integer, parameter :: dp = kind(1.0d0)` and declare real variables
as `real(kind=dp)`. Use :: in declarations.  Use implicit none and make sure to declare
all variables. You MUST use ```fortran to show the start of Fortran code."""

task_start = "Write a Fortran program to "

base_tasks = [
"""compute Euler's number using a Taylor series with the number of terms
`nterms` equal to 1000.""",
"""compute the prime numbers below 50."""]

for base_task in base_tasks:
    task = task_start + base_task + style
    print("\n**task: " + task + "**\n")
    for itry in range(1, ntries+1):
        print("attempt", itry)
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": task}])
        answer = completion.choices[0].message.content
        if print_answer:
            print("\nanswer:\n", answer, sep="")
        fortran_code = markdown_to_fortran(answer, strip_blanks=True)
        if print_code:
            print(fortran_code)
        compile_and_run_fortran_on_windows(fortran_code)

print("\ntime elapsed (sec):", "%0.2f"%(time.time() - start), "for",
    len(base_tasks), "tasks and", ntries, "tries each.")
