from pathlib import Path
from datetime import datetime
import os
import click
import re

@click.command()
@click.argument("path")
@click.option("--apply", is_flag=True, help="Apply renaming")
@click.option("--dirs", is_flag=True, help="Rename directories only")
def anima_rename(path, apply, dirs):
	os.chdir(path)
	path = Path(".")
	rename_suffix = [".mkv", ".mka", ".ass", ".mp4"]
	src_fname = []
	for f in path.iterdir():
		if not dirs:
			if not f.is_dir() and f.suffix in rename_suffix:
				src_fname.append(f.name)
		else:
			if f.is_dir():
				src_fname.append(f.name)
	
	common_entries = [
                # Vendors
		#r"(\s)*\[.*VCB-S[(tudio)]*[\w\d\&\-]*\](\s)*",
		r"(\s)*\[.*?VCB.*?\](\s)*",
		r"(\s)*\[.*FLsnow\](\s)*",
		r"(\s)*\[LoliHouse.*?\](\s)*",
		r"(\s)*\[Moozzi2.*?\](\s)*",
		r"(\s)*\[Kamigami\](\s)*",
		r"(\s)*\[DMG\](\s)*",
		r"(\s)*\[SFEO-Raws\](\s)*",
		r"(\s)*\[ANK-Raws\](\s)*",
		r"(\s)*\[SumiSora\](\s)*",
		r"(\s)*\[YYDM-11FANS\](\s)*",
		r"(\s)*\[UHA\-WINGS\&LoliHouse\](\s)*",
		r"(\s)*\[Nekomoe kissaten[(\&LoliHouse)]*\](\s)*",
                # Labels
		r"(\s)*\[(1080)[pP].*?\](\s)*",
		r"(\s)*\[Ma10[pP].*?\](\s)*",
		r"(\s)*\[BDRip.*?\](\s)*",
		r"(\s)*\[HEVC.*?\](\s)*",
		r"(\s)*\[MKV.*?\](\s)*",
		r"(\s)*\[x265.*?\](\s)*",
		r"(\s)*\[H264.*?\](\s)*",
		r"(\s)*\(BD.*?\)(\s)*",
                # Labels - more exact matches
		r"(\s)*\[1080[pP]_Ma10P\](\s)*",
		r"(\s)*\[1080[pP]_Hi10P\](\s)*",
		r"(\s)*\[720[pP]\](\s)*",
		r"(\s)*\[1920[xX]1080\](\s)*",
		r"(\s)*\[BD[Rr][Ii][Pp][\-\s\w\d\_]*\](\s)*",
		r"(\s)*\(BD 1080P x264 FLAC\)(\s)*",
		r"(\s)*\[[(Ma)(Hi)]*10p_[(2160)(1080)(720)]*p[\_\w]*\](\s)*",
		r"(\s)*\[x264_[2]*flac\](\s)*",
		r"(\s)*\[[xX]264_AAC\](\s)*",
		r"(\s)*\[x265_[2]*flac\](\s)*",
		r"(\s)*\[x265_ac3\](\s)*",
		r"(\s)*\[x265_flac_ac3\](\s)*",
		r"(\s)*\[x265_flac_[2]*aac\](\s)*",
		r"(\s)*\[AVC_AAC\](\s)*",
		r"(\s)*\[AVC_FLAC[xX2]*\](\s)*",
		r"(\s)*\[[0-9A-F]{8}\](\s)*",
		r"(\s)*\([0-9A-F]{8}\)(\s)*",
		r"(\s)*\[WEBRIP\](\s)*",
		r"(\s)*\[Movie[\w\(\)\.\s]*\](\s)*",
		r"(\s)*\[H264_FLAC\](\s)*",
		r"(\s)*\[HEVC[\s\w\d]*FLAC\](\s)*",
		r"(\s)*\[HEVC_ALS\](\s)*",
		#r"(\s)*\(BD[Rr]ip[\-\s\w\d\_]*FLAC\)(\s)*",
		#r"(\s)*\(BD[\-\s\w\d\_]*AAC\)(\s)*",
		#r"(\s)*\[BD[\-\s\w\d\_\(\)\.\,]*\](\s)*",
                # lazy match https://stackoverflow.com/a/766384
		r"(\s)*\[BD.*?\](\s)*",
		r"(\s)*\[WebRip 1080p HEVC\-[\w\d]* [(AAC)(ASSx2)\s]*\](\s)*",
		r"\.HKG\&X2",
		r"\.EMD\&HKG",
		r"\.HKG",
                # Misc
		r"(\s)*「.*」(\s)*",
		r"[第話章]",
                r"YY-",
                r"\.JYFanSub-",
                r"\ V2",
		r"^\s+"
	]

	post_process_entries = [
		r"^\s+",
		r"\s+$"
                #"[\(\)]"
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
		f = f.replace(' - ', ' ')
		f = f.replace('-', ' ')
		f = f.replace('～', ' ')
		f = f.replace('~', ' ')
		f = f.replace(':', ' ')
		f = f.replace(';', ' ')
		f = f.replace('：', ' ')
		f = f.replace('!', ' ')
		f = f.replace('/', ' ')
		f = f.replace('／', ' ')
		f = f.replace('？', ' ')
		f = f.replace(' .', '.')
		while '  ' in f:
			f = f.replace('  ', ' ')
		for entry in post_process_entries:
			p = re.compile(entry)
			f = p.sub('', f)
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
		with open('rename.log', 'a') as logfile:
			logfile.write('\n' + str(datetime.now()) + '\n')
			for i in range(len(src_fname)):
				logfile.write(('|' + src_fname[i] + '|').ljust(max_col_width) + '--> |' + dst_fname[i] + '|\n')
		for i in range(len(src_fname)):
			sf = Path(src_fname[i])
			sf.rename(dst_fname[i])


if __name__ == "__main__":
	anima_rename()
