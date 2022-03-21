# lambda-practice
Practice AWS Lambda using Python

## practice

### execute-ffmpeg

Layer 設定
ffmpeg-bin, ffmpeg-python と一緒に ZIP すると、

```text
1 validation error detected: Value '[]' at 'layers' failed to satisfy constraint: Member must satisfy constraint: [Member must have length less than or equal to 140, Member must have length greater than or equal to 1, Member must satisfy regular expression pattern: (arn:[a-zA-Z0-9-]+:lambda:[a-zA-Z0-9-]+:\d{12}:layer:[a-zA-Z0-9-_]+:[0-9]+)|(arn:[a-zA-Z0-9-]+:lambda:::awslayer:[a-zA-Z0-9-_]+)]
```

ffmpeg-bin と ffmpeg-python を分けて ZIP して Layer 登録すれば、Layer 設定＆実行も問題ない。

## development 

Kinesis Video Stream から Python Lambda により、 WebM を扱う方法を模索した。

### MATROSKA

> Matroska the extensible, open source, open standard Multimedia container. Matroska is usually found as .mkv files (Matroska video), .mka files (Matroska audio), .mks files (subtitles) and .mk3d files (stereoscopic/3D video). It is also the basis for .webm (WebM) files.

What is Matroska?

> Matroska aims to become THE standard of multimedia container formats. It was derived from a project called MCF, but differentiates from it significantly because it is based on EBML (Extensible Binary Meta Language), a binary derivative of XML. EBML enables the Matroska Development Team to gain significant advantages in terms of future format extensibility, without breaking file support in old parsers.

### MKVToolNix

> MKVToolNix is a set of tools to create, alter and inspect Matroska & WebM files under Windows, macOS, Linux and other Unices. It is the de-facto reference implementation of a Matroska multiplexer.

### 開発準備

[Python][python] で [Matroska][MATROSKA] (include WebM) を扱うための選択肢

1. [pymkv][pymkv] を利用する
    1. 事前に [MKVToolNix][MKVToolNix] をインストールする
        1. libEBML, libMatroska などに依存している

macOS では、`brew install mkvtoolnix` で、問題無くインストールできた。

### install MKVToolNix on macOS

```shell
brew install mkvtoolnix
```

しかし、依存関係が激しいなぁ(嫌な予感)

```shell
brew info mkvtoolnix
Warning: Treating mkvtoolnix as a formula. For the cask, use homebrew/cask/mkvtoolnix
mkvtoolnix: stable 66.0.0 (bottled), HEAD
Matroska media files manipulation tools
https://mkvtoolnix.download/
Not installed
From: https://github.com/Homebrew/homebrew-core/blob/HEAD/Formula/mkvtoolnix.rb
License: GPL-2.0-or-later
==> Dependencies
Build: docbook-xsl ✘, pkg-config ✔
Required: boost ✘, flac ✔, fmt ✘, gettext ✔, gmp ✔, libebml ✘, libmatroska ✘, libogg ✔, libvorbis ✔, nlohmann-json ✘, pugixml ✘, qt ✘, utf8cpp ✘
==> Requirements
Required: macOS >= 10.15 ✔
==> Options
--HEAD
	Install HEAD version
==> Analytics
install: 3,655 (30 days), 11,650 (90 days), 40,046 (365 days)
install-on-request: 3,518 (30 days), 11,244 (90 days), 38,631 (365 days)
build-error: 0 (30 days)
```

Ubuntu では、 あっさりと [MKVToolNixサイトの手順][MKVToolNix(Ubuntu)] でインストールできた。

### AWS Lambda Layer 作成準備

AWS Lambda 関数で利用可能な [MKVToolNix][MKVToolNix] を準備するには、  
[AWS Lambda デプロイパッケージで Amazon Linux AMI ネイティブバイナリパッケージを使用する方法][llbp] を参考に準備を進めた。

のだが、Amazon Linux2 に `MKVToolNix` をインストールするのは諦めた。

以下は、諦めるまでの経緯。

```shell
sudo rpm -Uhv https://mkvtoolnix.download/centosstream/bunkus-org-repo-2-4.noarch.rpm
```

レポジトリのパス名を修正: 用意されているダウンロードサイトのパス名が `centosstream/8` のみなので、

`/etc/yum.repos.d/bunkus-org.repo` 変更した。

```config
[bunkus-org]
name=bunkus.org MKVToolNix repository
baseurl=https://mkvtoolnix.download/centosstream/8/$basearch/
enabled=1
metadata_expire=7d
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-BUNKUS-ORG-20150211

[bunkus-org-source]
name=bunkus.org MKVToolNix repository
baseurl=https://mkvtoolnix.download/centosstream/8/SRPMS/
enabled=0
metadata_expire=7d
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-BUNKUS-ORG-20150211
```

インストールコマンド `sudo yum install mkvtoolnix` の処理が進むのだが、

```shell
Failed to set locale, defaulting to C
Loaded plugins: priorities, update-motd, upgrade-helper
Resolving Dependencies
--> Running transaction check
---> Package mkvtoolnix.x86_64 0:66.0.0-1 will be installed
--> Processing Dependency: libQt5Core.so.5(Qt_5)(64bit) for package: mkvtoolnix-66.0.0-1.x86_64
--> Processing Dependency: libQt5Core.so.5(Qt_5.15)(64bit) for package: mkvtoolnix-66.0.0-1.x86_64
--> Processing Dependency: libFLAC.so.8()(64bit) for package: mkvtoolnix-66.0.0-1.x86_64
--> Processing Dependency: libQt5Core.so.5()(64bit) for package: mkvtoolnix-66.0.0-1.x86_64
--> Processing Dependency: libcmark.so.0.28.3()(64bit) for package: mkvtoolnix-66.0.0-1.x86_64
--> Processing Dependency: libdvdread.so.4()(64bit) for package: mkvtoolnix-66.0.0-1.x86_64
--> Processing Dependency: libfmt.so.6()(64bit) for package: mkvtoolnix-66.0.0-1.x86_64
--> Processing Dependency: libogg.so.0()(64bit) for package: mkvtoolnix-66.0.0-1.x86_64
--> Processing Dependency: libvorbis.so.0()(64bit) for package: mkvtoolnix-66.0.0-1.x86_64
--> Running transaction check
---> Package flac.x86_64 0:1.2.1-7.7.amzn1 will be installed
---> Package libogg.x86_64 2:1.1.4-2.1.5.amzn1 will be installed
---> Package libvorbis.x86_64 1:1.3.3-8.7.amzn1 will be installed
---> Package mkvtoolnix.x86_64 0:66.0.0-1 will be installed
--> Processing Dependency: libQt5Core.so.5(Qt_5)(64bit) for package: mkvtoolnix-66.0.0-1.x86_64
--> Processing Dependency: libQt5Core.so.5(Qt_5.15)(64bit) for package: mkvtoolnix-66.0.0-1.x86_64
--> Processing Dependency: libQt5Core.so.5()(64bit) for package: mkvtoolnix-66.0.0-1.x86_64
--> Processing Dependency: libcmark.so.0.28.3()(64bit) for package: mkvtoolnix-66.0.0-1.x86_64
--> Processing Dependency: libdvdread.so.4()(64bit) for package: mkvtoolnix-66.0.0-1.x86_64
--> Processing Dependency: libfmt.so.6()(64bit) for package: mkvtoolnix-66.0.0-1.x86_64
--> Finished Dependency Resolution
Error: Package: mkvtoolnix-66.0.0-1.x86_64 (bunkus-org)
           Requires: libQt5Core.so.5()(64bit)
Error: Package: mkvtoolnix-66.0.0-1.x86_64 (bunkus-org)
           Requires: libQt5Core.so.5(Qt_5)(64bit)
Error: Package: mkvtoolnix-66.0.0-1.x86_64 (bunkus-org)
           Requires: libQt5Core.so.5(Qt_5.15)(64bit)
Error: Package: mkvtoolnix-66.0.0-1.x86_64 (bunkus-org)
           Requires: libfmt.so.6()(64bit)
Error: Package: mkvtoolnix-66.0.0-1.x86_64 (bunkus-org)
           Requires: libdvdread.so.4()(64bit)
Error: Package: mkvtoolnix-66.0.0-1.x86_64 (bunkus-org)
           Requires: libcmark.so.0.28.3()(64bit)
 You could try using --skip-broken to work around the problem
 You could try running: rpm -Va --nofiles --nodigest
```

https://centos.pkgs.org/8/centos-appstream-x86_64/qt5-qtbase-5.15.2-3.el8.i686.rpm.html

から `qt5-qtbase-5.15.2-3.el8.aarch64.rpm` をダウンロードし、

`rpm -i ./qt5-qtbase-5.15.2-3.el8.aarch64.rpm` を実施し。依存パッケージの嵐、この時点で諦めた。

```shell 
warning: ./qt5-qtbase-5.15.2-3.el8.aarch64.rpm: Header V3 RSA/SHA256 Signature, key ID 8483c65d: NOKEY
error: Failed dependencies:
	ld-linux-aarch64.so.1()(64bit) is needed by qt5-qtbase-5.15.2-3.el8.aarch64
	ld-linux-aarch64.so.1(GLIBC_2.17)(64bit) is needed by qt5-qtbase-5.15.2-3.el8.aarch64
	libc.so.6(GLIBC_2.28)(64bit) is needed by qt5-qtbase-5.15.2-3.el8.aarch64
	libcrypto.so.1.1()(64bit) is needed by qt5-qtbase-5.15.2-3.el8.aarch64
	libcrypto.so.1.1(OPENSSL_1_1_0)(64bit) is needed by qt5-qtbase-5.15.2-3.el8.aarch64
	libcrypto.so.1.1(OPENSSL_1_1_1)(64bit) is needed by qt5-qtbase-5.15.2-3.el8.aarch64
	libdbus-1.so.3(LIBDBUS_1_3)(64bit) is needed by qt5-qtbase-5.15.2-3.el8.aarch64
	libdl.so.2(GLIBC_2.17)(64bit) is needed by qt5-qtbase-5.15.2-3.el8.aarch64
	libicudata.so.60()(64bit) is needed by qt5-qtbase-5.15.2-3.el8.aarch64
	libicui18n.so.60()(64bit) is needed by qt5-qtbase-5.15.2-3.el8.aarch64
	libicuuc.so.60()(64bit) is needed by qt5-qtbase-5.15.2-3.el8.aarch64
	libm.so.6(GLIBC_2.17)(64bit) is needed by qt5-qtbase-5.15.2-3.el8.aarch64
	libpcre2-16.so.0()(64bit) is needed by qt5-qtbase-5.15.2-3.el8.aarch64
	libpthread.so.0(GLIBC_2.17)(64bit) is needed by qt5-qtbase-5.15.2-3.el8.aarch64
	libssl.so.1.1()(64bit) is needed by qt5-qtbase-5.15.2-3.el8.aarch64
	libssl.so.1.1(OPENSSL_1_1_0)(64bit) is needed by qt5-qtbase-5.15.2-3.el8.aarch64
	libssl.so.1.1(OPENSSL_1_1_1)(64bit) is needed by qt5-qtbase-5.15.2-3.el8.aarch64
	libsystemd.so.0()(64bit) is needed by qt5-qtbase-5.15.2-3.el8.aarch64
	libsystemd.so.0(LIBSYSTEMD_209)(64bit) is needed by qt5-qtbase-5.15.2-3.el8.aarch64
	qt5-qtbase-common = 5.15.2-3.el8 is needed by qt5-qtbase-5.15.2-3.el8.aarch64
```


[python]: https://python.org
[pymkv]: https://github.com/sheldonkwoodward/pymkv
[pymkv Docs]: https://pymkv.shel.dev/en/stable/
[MATROSKA]: https://www.matroska.org/
[MKVToolNix]: https://mkvtoolnix.download
[MKVToolNix(Ubuntu)]: https://mkvtoolnix.download/downloads.html#ubuntu
[llbp]: https://aws.amazon.com/jp/premiumsupport/knowledge-center/lambda-linux-binary-package/