# ChatGPT-Fortran-generator
Python script to generate Fortran codes by ChatGPT to perform tasks, compile them with gfortran, fix errors and warnings, and run them. ChatGPT is asked to code each task multiple times, because sometimes it produces code that fails to compile or gives wrong answers. See `output_xfortran_chat.txt` for sample output from `python xfortran_chat.py` and `output_xdebug_fortran.txt` and `output_xdebug_fortran_chatgpt_4.txt` for sample output of `python xdebug_fortran.py`.

The `debug_fortran` function in `fortran.py` shows how you can get a Fortran code to compile by iteratively sending compiler error messages
to ChatGPT and asking for fixes.

#### Update 2023-07-07
`gpt-4` is now an allowed model in the API, and in the script one can set the variable `gpt_model` to it.

#### Update 2025-03-31
The scripts here no longer run, with error messages such as

```
You tried to access openai.ChatCompletion, but this is no longer supported in openai>=1.0.0 - see the README at https://github.com/openai/openai-python for the API.
```
I suggest trying https://github.com/Beliavsky/OpenAI-Fortran-agent instead.
