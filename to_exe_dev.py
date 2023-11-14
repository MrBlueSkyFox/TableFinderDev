import PyInstaller.__main__

PyInstaller.__main__.run([
    'dev_exe.py',
    '--onefile',
    # '--onedir',
    "-y",
    # "--hidden-import", "numpy",
    # "--hidden-import", "torch"
    # "--collect-submodules", "transformers"
    # "--collect-submodules", "torch"
    # "--collect-data", "torch",

    # "--copy-metadata" ,"torch"
    # '--windowed'
])
