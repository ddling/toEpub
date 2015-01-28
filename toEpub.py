# _*_ coding: utf-8 _*_

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

import zipfile
import os
import shutil
import ConfigParser

class Epub:

    ROOT = None
    OPES_DIR = None
    CSS_DIR = None
    IMAGE_DIR = None

    def __init__(self):

        shutil.copytree("template", "tmp")
        self.ROOT = os.getcwd()
        self.OPES_DIR = self.ROOT + "/tmp/OPS"
        self.IMAGE_DIR = self.OPES_DIR + "/images"
        self.CSS_DIR = self.OPES_DIR + "/css"

    def createOPF(self):

        opf_file = open(self.OPES_DIR + "/content.opf", 'w')
        config = ConfigParser.ConfigParser()
        config.read("config.ini")
        title = config.get("epub", "title")
        creator = config.get("epub", "creator")
        desc = config.get("epub", "desc")

        xml = u'''<?xml version="1.0" encoding="UTF-8" ?>
<package version="2.0" unique-identifier="PrimaryID" xmlns="http://www.idpf.org/2007/opf">
    <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
    <dc:title>''' + title + '''</dc:title>
    <dc:identifier opf:scheme="ISBN"></dc:identifier>
    <dc:language>zh-CN</dc:language>
    <dc:creator>''' + creator +  '''</dc:creator>
    <dc:publisher>epub掌上书苑</dc:publisher>
    <dc:description>''' + desc + '''</dc:description>
    <dc:coverage></dc:coverage>
    <dc:source>http://www.cnepub.com</dc:source>
    <dc:date>2014-11-23</dc:date>
    <dc:rights>本电子书由epubBuilder制作生成，欢迎访问http://www.cnepub.com分享交流海量电子书。
    epubBuilder仅供交流使用，未经授权，不得用于商业用途。</dc:rights>
    <dc:subject></dc:subject>
    <dc:contributor></dc:contributor>
    <dc:type>[type]</dc:type>
    <dc:format></dc:format>
    <dc:relation></dc:relation>
    <dc:builder>epubBuilder</dc:builder>
    <dc:builder_version>3.1.08.28</dc:builder_version>
    </metadata>
    <manifest>
    <!-- Content Documents -->
    <item id="main-css" href="css/main.css" media-type="text/css"/>
    <item id="coverpage"  href="coverpage.html"  media-type="application/xhtml+xml"/>
    <item id="chapter1"  href="chapter1.html"  media-type="application/xhtml+xml"/>
    <item id="chapter48"  href="chapter48.html"  media-type="application/xhtml+xml"/>

    <item id="ncx"  href="nav.ncx" media-type="application/x-dtbncx+xml"/>
    <item id="css" href="css/main.css" media-type="text/css"/>
    </manifest>
    <spine toc="ncx">
    <itemref idref="coverpage" linear="yes"/>
    <itemref idref="chapter1" linear="yes"/>
    <itemref idref="chapter48" linear="yes"/>

    </spine>
    <guide>
    <reference type="cover" title="封面"  href="coverpage.html"/>

    </guide>
</package>'''

        opf_file.write(xml)
        opf_file.close()

    def createNCX(self):

        ncx_file = open(self.OPES_DIR + "/nav.ncx", 'w')
        for file_ in os.listdir("res/"):
            shutil.copy("res/" + file_, self.OPES_DIR)
        xml = u'''<?xml version="1.0" encoding="UTF-8"?>
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
<navPoint id="coverpage" playOrder="0">
<navLabel><text>封面</text></navLabel>
<content src="coverpage.html"/>
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
        ncx_file.write(xml)
        ncx_file.close()
        
    def compressToEpub(self, EpubName = "test.epub"):
        os.chdir("tmp")
        epub    =   zipfile.ZipFile(EpubName,'w')
        epub.write('mimetype', compress_type=zipfile.ZIP_STORED)
    
        def Help_ZipToEpub(Dir='.'):
            for p   in  os.listdir(Dir):
                if  p   ==  EpubName    or  p   ==  'mimetype':
                    continue
                filepath    =   os.path.join(Dir,p)
                if  not os.path.isfile(filepath):
                    if  p   ==  '.' or  p   ==  '..':
                        continue
                    Help_ZipToEpub(Dir=filepath)
                else:
                    epub.write(filepath, compress_type=zipfile.ZIP_STORED)
        Help_ZipToEpub()
        epub.close()
    
epub = Epub()
epub.createOPF()
epub.createNCX()
epub.compressToEpub()
