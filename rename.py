from pathlib import Path
import os
import click
import re

@click.command()
@click.argument("path")
@click.option("--apply", is_flag=True)
@click.option("--dirs", is_flag=True)
def anima_rename(path, apply, dirs):
	os.chdir(path)
	path = Path(".")
	rename_suffix = [".mkv", ".mka", ".ass"]
	src_fname = []
	for f in path.iterdir():
		if not dirs:
			if not f.is_dir() and f.suffix in rename_suffix:
				src_fname.append(f.name)
		else:
			if f.is_dir():
				src_fname.append(f.name)
	
	common_entries = [
		r"(\s)*\[.*VCB-Studio\](\s)*",
		r"(\s)*\[Ma10p_1080p\](\s)*",
		r"(\s)*\[Ma10p_720p\](\s)*",
		r"(\s)*\[x265_flac\](\s)*",
		r"(\s)*\[x265_ac3\](\s)*",
		r"(\s)*\[x265_flac_ac3\](\s)*",
		r"(\s)*\[x265_flac_aac\](\s)*",
		r"(\s)*\[[0-9A-F]{8}\](\s)*",
		r"\.HKG\&X2",
		r"\.EMD\&HKG",
		r"\.HKG"
	]

	dst_fname = []
	for f in src_fname:
		for entry in common_entries:
			p = re.compile(entry)
			f = p.sub('', f)
		# remove final brackets
		f = f.replace('[', ' ')
		f = f.replace(']', ' ')
		f = f.replace('_', ' ')
		f = f.replace('  ', ' ')
		f = f.replace(' .', '.')
		dst_fname.append(f)

	sf = src_fname.copy()
	df = dst_fname.copy()
	src_fname = []
	dst_fname = []
	for i in range(len(sf)):
		if sf[i] != df[i]:
			src_fname.append(sf[i])
			dst_fname.append(df[i])

	if len(src_fname) == 0:
		print('Nothing to do')
		return

	max_col_width = max([len(f) for f in src_fname]) + 4

	for i in range(len(src_fname)):
		print(('|' + src_fname[i] + '|').ljust(max_col_width) +  '--> |' + dst_fname[i] + '|')

	if apply:
		with open('rename.log', 'w') as logfile:
			for i in range(len(src_fname)):
				logfile.write('|' + src_fname[i] + '|\t --> |' + dst_fname[i] + '|\n')
		for i in range(len(src_fname)):
			sf = Path(src_fname[i])
			sf.rename(dst_fname[i])


if __name__ == "__main__":
	anima_rename()
