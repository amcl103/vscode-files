import re

# 设置前缀
prefix = "Ntab"

with open('ntab.gff3', 'r') as gff3:
    GffList = gff3.readlines()

SelList = []
for m in GffList:
    line = m.split("\t")
    if re.match('^#',line[0]):  # 判断第一列是否以#开头
        continue
    if re.match('(?!transcript)', line[2]):   # 判断第三列是不是transcript
        continue
    
    attribute = line[8]
    # 提取第九列前缀后面的数
    gene_part = attribute.split(prefix)[1]
    gene_num = int(gene_part.split("g")[0])
    # group = attribute.removeprefix('ID=').split(';',1)
    group = re.split(r'=|;',line[8])
    LineList = [gene_num,line[3],line[4],line[6],group[1]]
    SelList.append(LineList)

NewList= sorted(SelList, key = lambda x: (int(x[0]),int(x[1])),reverse = False) # 按1、2列升序排列，先比较第一列，再比较第二列

ChrNum  = 0
GeneNum = 0
GeneBp = 0
ChrOrder = {}
ChrBp = {}

NewFa = {}  # 创建字典用于处理fa文件
with open('Ntab.new.gff', 'w+') as gff:
    for i in range(len(NewList)):
        if(int(NewList[i][0]) > ChrNum):
            ChrNum = int(NewList[i][0])
            GeneNum = 1
        else:
            GeneNum = GeneNum + 1
        
        ChrBp[ChrNum] = int(NewList[i][2])
        ChrOrder[ChrNum] = GeneNum
        GeneO = "{:0>5d}".format(GeneNum) # 格式化，宽度为5的字符串，不足在左侧填充0
        NewId = f"{prefix}{NewList[i][0]}g{GeneO}"
        
        NewList[i].insert(1,NewId)  # 在第二列插入新id
        NewList[i].insert(5,str(GeneNum))
        
        gff.write("\t".join(map(str,NewList[i]))+"\n")
        NewFa[NewList[i][6]] = NewId    # 键为最后一列，值为新id
        
with open('ntab.prot.fa', 'r') as fa, open('Ntab.newprot', 'w') as new_fa:
    for f in fa:
        if f.startswith('>'):   # 判断是否以>开头
            #geneID = f[1:].strip().split(' ', 1)
            geneID = f.removeprefix('>').split(' ', 1)
            if geneID[0] in NewFa:
                NewgeneID = NewFa[geneID[0]]
                new_fa.write(f"\n>{NewgeneID} {geneID[1]}")
        else:
            new_fa.write(f)

with open('Ntab.lens', 'w+') as lens:
    for k in ChrOrder.keys():
        lens.write(str(k) +"\t"+str(ChrBp[k])+"\t"+ str(ChrOrder[k]) +"\n")