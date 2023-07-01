# ChatGPT-Fortran-generator
Python script to generate Fortran codes by ChatGPT to perform tasks, compile them with gfortran, and run them. ChatGPT is asked to code each task multiple times, because sometimes it produces code that fails to compile or gives wrong answers. See `output_xfortran_chat.txt` for sample output from `python xfortran_chat.py` and `output_xdebug_fortran.txt` for sample output of `python xdebug_fortran.py`.

The `debug_fortran` function in `fortran.py` shows how you can get a Fortran code to compile by iteratively sending compiler error messages
to ChatGPT and asking for fixes.
