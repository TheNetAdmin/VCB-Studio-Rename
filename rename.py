from pathlib import Path
import os
import click
import re

@click.command()
@click.argument("path")
@click.option("--apply", is_flag=True)
def anima_rename(path, apply):
    os.chdir(path)
    path = Path(".")
    rename_suffix = [".mkv", ".mka", ".acc"]
    src_fname = []
    for f in path.iterdir():
        if not f.is_dir() and f.suffix in rename_suffix:
            src_fname.append(f.name)
    
    common_entries = [
        r"(\s)*\[VCB-Studio\](\s)*",
        r"(\s)*\[Ma10p_1080p\](\s)*",
        r"(\s)*\[x265_flac\](\s)*"
    ]

    dst_fname = []
    for f in src_fname:
        for entry in common_entries:
            p = re.compile(entry)
            f = p.sub('', f)
        # remove final brackets
        f = f.replace('[', '')
        f = f.replace(']', '')
        dst_fname.append(f)

    for i in range(len(src_fname)):
        print(f'|{src_fname[i]}| --> |{dst_fname[i]}|')

    if apply:
        with open('rename.log', 'w') as logfile:
            for i in range(len(src_fname)):
                logfile.write('|' + 'src_fname[i]' + '| --> |' + '{dst_fname[i]' + '|\n')
        for i in range(len(src_fname)):
            sf = Path(src_fname[i])
            sf.rename(dst_fname[i])


if __name__ == "__main__":
    anima_rename()