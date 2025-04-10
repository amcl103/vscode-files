#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from collections import defaultdict

def process_gff3(input_file, output_file):
    """
    处理GFF3文件，按照要求重新格式化并写入新文件
    
    Args:
        input_file (str): 输入GFF3文件路径
        output_file (str): 输出文件路径
    """
    # 用于存储不同区块的数据
    blocks = defaultdict(list)
    
    # 读取输入文件
    with open(input_file, 'r') as f:
        for line in f:
            # 跳过注释行和空行
            if line.startswith('#') or not line.strip():
                continue
                
            # 分割每一行
            fields = line.strip().split('\t')
            if len(fields) < 9:
                continue
                
            # 获取序列名称（最后一列）
            seq_name = fields[-1]
            # 使用正则表达式提取数字部分
            match = re.search(r'Nsyl(\d+)', seq_name)
            if not match:
                continue
                
            block_num = int(match.group(1))
            # 将行数据添加到对应的区块中
            blocks[block_num].append(fields)
    
    # 对每个区块进行排序
    for block_num in blocks:
        # 按照起始位点和终止位点排序
        blocks[block_num].sort(key=lambda x: (int(x[3]), int(x[4])))
    
    # 写入输出文件
    with open(output_file, 'w') as f:
        for block_num in sorted(blocks.keys()):
            # 为每个区块生成新的序列编号
            seq_counter = 1
            for fields in blocks[block_num]:
                # 1. 添加区块编号作为第一列
                new_fields = [str(block_num)]
                
                # 2. 添加原有的前8列（跳过类型列）
                new_fields.extend(fields[:2])  # 序列名称和来源
                new_fields.extend(fields[3:8])  # 起始、终止、分数、链、相位
                
                # 3. 添加自然数列（从1开始）
                new_fields.append(str(seq_counter))
                
                # 4. 生成新的序列名称
                new_seq_name = f"Nsyl{block_num}g{seq_counter:05d}"
                new_fields.append(new_seq_name)
                
                # 写入新行
                f.write('\t'.join(new_fields) + '\n')
                
                # 更新序列计数器
                seq_counter += 1

if __name__ == "__main__":
    input_file = "new_nsyl.txt"  # 输入文件路径
    output_file = "new.txt"  # 输出文件路径
    process_gff3(input_file, output_file)
    print("处理完成！")
