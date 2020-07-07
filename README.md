# VCB-Studio-Rename: VCB-Sudio 文件名简化工具

本项目提供一个重命名工具，专门用于简化 [VCB-Sudio](https://vcb-s.com) 压制的动画的文件名，例如从文件名中去掉 `[Ma10p_1080p]`。

做这个工具的起因是我下载了很多 VCB-Studio 的动画，然后放在 PLEX 内播放。
我在 PLEX 内安装了一个自动获取动画信息的插件，[HamaTV](https://github.com/ZeroQI/Hama.bundle)，来获取动画的简介，封面和演员信息。
HamaTV 通过文件夹名直接查询一些线上动画数据库 (如 AniDB)，但文件名或文件夹名内的一些特殊字段 (如 `[Ma10p_1080p]`) 会导致信息获取失败。

所以我做了这个工具来批量重命名文件名与文件夹名。

## 安装

1. 获取 Python 代码，只需要 `rename.py` 文件，可通过 Git clone 或浏览器下载。
2. 安装 Python3
3. 安装本代码所需的 Python3 库:
   - `pip3 install click`

至此安装结束

## 使用

参数和有效选项如下:

```shell
# python3 rename.py --help
Usage: rename.py [OPTIONS] PATH

Options:
  --apply  Apply renaming
  --dirs   Rename directories only
  --help   Show this message and exit.
```

`PATH` 为动画目录的绝对地址，当 `rename.py` 仅接收到这个参数，没有收到任何其他选项时，会列出重命名前后的文件名对比，但并不会实际进行重命名操作。
这里列出示例操作的一部分命令行输出：

```shell
# python3 rename.py "/files/[VCB-Studio] PERSONA5 the Animation [Ma10p_1080p]"
|[VCB-Studio] PERSONA5 the Animation [01][Ma10p_1080p][x265_flac_aac].mkv|	                    --> |PERSONA5 the Animation 01.mkv|
...
|[VCB-Studio] PERSONA5 the Animation [27(Dark Sun...)][Ma10p_1080p][x265_flac_aac].mkv|	        --> |PERSONA5 the Animation 27(Dark Sun...).mkv|
|[VCB-Studio] PERSONA5 the Animation -THE DAY BREAKERS- [OVA][Ma10p_1080p][x265_flac_aac].mkv|	--> |PERSONA5 the Animation -THE DAY BREAKERS- OVA.mkv|

```

当确认好重命名后的文件名没有问题之后，可在上述命令后加上 `--apply` 选项来应用重命名操作，同时生成一个 `rename.log` 文件记录重命名操作，方便后续恢复

```shell
# python3 rename.py "/files/[VCB-Studio] PERSONA5 the Animation [Ma10p_1080p]" --apply
|[VCB-Studio] PERSONA5 the Animation [01][Ma10p_1080p][x265_flac_aac].mkv|	                    --> |PERSONA5 the Animation 01.mkv|
...
|[VCB-Studio] PERSONA5 the Animation [27(Dark Sun...)][Ma10p_1080p][x265_flac_aac].mkv|	        --> |PERSONA5 the Animation 27(Dark Sun...).mkv|
|[VCB-Studio] PERSONA5 the Animation -THE DAY BREAKERS- [OVA][Ma10p_1080p][x265_flac_aac].mkv|	--> |PERSONA5 the Animation -THE DAY BREAKERS- OVA.mkv|
```

以上操作只重命名视频文件和字幕文件，详见 `rename.py` 代码中的 `rename_suffix`。
如需重命名文件夹，则需使用 `--dirs` 来重命名文件夹，并使用文件夹所在目录：

```shell
# python3 rename.py "/files/" --dirs
|[VCB-Studio] Dimension W [Ma10p_1080p]|                         --> |Dimension W|
|[VCB-Studio] Full Metal Panic! Invisible Victory [Ma10p_1080p]| --> |Full Metal Panic! Invisible Victory|
|[VCB-Studio] PERSONA5 the Animation [Ma10p_1080p]|              --> |PERSONA5 the Animation|

# python3 rename.py "/files/" --dirs --apply
|[VCB-Studio] Dimension W [Ma10p_1080p]|                         --> |Dimension W|
|[VCB-Studio] Full Metal Panic! Invisible Victory [Ma10p_1080p]| --> |Full Metal Panic! Invisible Victory|
|[VCB-Studio] PERSONA5 the Animation [Ma10p_1080p]|              --> |PERSONA5 the Animation|
```

注意一次操作只能重命名文件**或者**文件名，不会同时重命名两者。

## 致谢

感谢 VCB-Studio 为我们带来这么多精美的压制作品

## 开源协议

本项目代码基于 MIT 协议开源
