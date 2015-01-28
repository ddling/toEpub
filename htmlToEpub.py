# _*_ coding: utf-8 _*_

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

import os
import shutil
import zipfile

class HtmlToEpub:

    ROOT_DIR     = None
    META_INF_DIR = None
    OEBPS_DIR    = None

    def __init__(self):
        self.ROOT_DIR     = os.getcwd()
        self.META_INF_DIR = self.ROOT_DIR + "/tmp/META-INF"
        self.OEBPS_DIR    = self.ROOT_DIR + "/tmp/OEBPS"
        # 创建临时文件夹，将epub的所有文件都放在里面
        os.mkdir("tmp")
        os.chdir("tmp")

        os.mkdir("META-INF")
        os.mkdir(self.OEBPS_DIR)

        for htmlFile in os.listdir(self.ROOT_DIR + "/res/"):
            shutil.copy(self.ROOT_DIR + "/res/" + htmlFile, self.OEBPS_DIR)

    def getHtmlFile(self):
        htmlArr = []
        for htmlFile in os.listdir(self.OEBPS_DIR):
            if htmlFile.split(".")[1] == 'html' and htmlFile.split(".")[0] != 'cover':
                htmlArr.append(htmlFile)

        print htmlArr
        return sorted(htmlArr)

    def createMetaInf(self):
        xml = u'''<?xml version="1.0" encoding="UTF-8" ?>
        <container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
           <rootfiles>
                 <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
           </rootfiles>
        </container>'''

        container = open(self.META_INF_DIR + "/container.xml", 'w')
        container.write(xml)
        container.close()

    def createMimetype(self):

        mimetype = open("mimetype", 'wb')
        mimetype.write('application/epub+zip')
        mimetype.close()

    def createOPF(self):
        opf_tpl = u'''<?xml version="1.0" encoding="UTF-8" ?>
        <package version="2.0" unique-identifier="PrimaryID" xmlns="http://www.idpf.org/2007/opf">
        <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
        <dc:identifier opf:scheme="ISBN"></dc:identifier>
        <dc:language>zh-CN</dc:language>
        <dc:title>凌东东自传2</dc:title>
        <dc:creator>凌东东</dc:creator>
        <dc:publisher>dd</dc:publisher>
        <dc:description>dd</dc:description>
        <dc:date>2014-11-23</dc:date>
        </metadata>
        <manifest>
            %(manifest)s
        </manifest>
        <spine toc="ncx">
            %(spine)s
        </spine>
        <guide>
        <reference type="cover" title="封面"  href="cover.html"/>

        </guide>
        </package>
        '''

        manifest = ""
        spine = ""

        manifest += '<item id="cover" href="cover.html" media-type="application/xhtml+xml"/>\n<item id="ncx"  href="nav.ncx" media-type="application/x-dtbncx+xml"/>\n<item id="css" href="main.css" media-type="text/css"/>'
        spine += '<itemref idref="cover" linear="yes"/>'

        i = 1
        htmlDict = self.getHtmlFile()
        for html in htmlDict:
            manifest += '<item id="file_%s" href="%s" media-type="application/xhtml+xml"/>\n' % (i, html)
            spine += '<itemref idref="file_%s"  linear="yes"/>\n' % (i)
            i += 1

        
        opf = open(self.OEBPS_DIR + "/content.opf", 'w')
        opf.write(opf_tpl % {'manifest': manifest, 'spine': spine})
        opf.close()

    def createNCX(self):
        ncx_tpl = u'''<?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE ncx PUBLIC
        "-//NISO//DTD ncx 2005-1//EN"
        "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
        <ncx version="2005-1"
        xml:lang="en-US"
        xmlns="http://www.daisy.org/z3986/2005/ncx/">
        <head>
        <!-- The following four metadata items are required for all
            NCX documents, including those conforming to the relaxed
            constraints of OPS 2.0 -->
            <meta name="dtb:uid" content="51037e82-03ff-11dd-9fbb-0018f369440e"/>
            <meta name="dtb:depth" content="1"/>
            <meta name="dtb:totalPageCount" content="0"/>
            <meta name="dtb:maxPageNumber" content="0"/>
            <meta name="provider" content="www.cnepub.com"/>
            <meta name="builder" content="epubBuilder present by www.cnepub.com"/>
            <meta name="right" content="该文档由epubBuilder生成。epubBuilder为掌上书苑（www.cnepub.com)提供的epub制作工具，仅供个人交流与学习使用。在未获得掌上书苑的商业授权前，不得用于任何商业用途。"/>
        </head>
        <docTitle><text> 简写本水浒传 </text></docTitle>
        <docAuthor><text> 施耐奄 </text></docAuthor>
        <navMap>
            <navPoint id="cover" playOrder="0">
            <navLabel><text>封面</text></navLabel>
            <content src="cover.html"/>
            </navPoint>
            <navPoint id="chapter1" playOrder="1">
            <navLabel><text>目录</text></navLabel>
            <content src="chapter1.html"/>
            </navPoint>
            <navPoint id="chapter48" playOrder="2">
            <navLabel><text>第一回　天罡地煞魔君转世</text></navLabel>
            <content src="chapter48.html"/>
            </navPoint>
        </navMap>
        </ncx>
        '''

        ncx = open(self.OEBPS_DIR + "/nav.ncx", 'w')
        ncx.write(ncx_tpl)
        ncx.close()

    def compressToEpub(self, EpubName = "test.epub"):
        epub = zipfile.ZipFile(EpubName,'w')
        epub.write('mimetype', compress_type=zipfile.ZIP_STORED)

        def Help_ZipToEpub(Dir='.'):
            for p in os.listdir(Dir):
                if p == EpubName or p == 'mimetype':
                    continue
                filepath = os.path.join(Dir,p)
                if not os.path.isfile(filepath):
                    if p == '.' or p == '..':
                        continue
                    Help_ZipToEpub(Dir=filepath)
                else:
                    epub.write(filepath, compress_type=zipfile.ZIP_STORED)
        Help_ZipToEpub()
        epub.close()

htmlToEpub = HtmlToEpub()
htmlToEpub.createMetaInf()
htmlToEpub.createMimetype()
htmlToEpub.createOPF()
htmlToEpub.createNCX()
htmlToEpub.compressToEpub()
