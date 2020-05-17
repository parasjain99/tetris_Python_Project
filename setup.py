import cx_Freeze

executables = [cx_Freeze.Executable("tetris_project2019.py")]

cx_Freeze.setup(
    name = "Tetris-By Para",
    options = { "build_exe":{ "packages" : ["pygame"] } },
    description = "Tetris Made By Para",
    executables = executables
)
