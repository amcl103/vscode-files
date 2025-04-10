"""
GFF3文件处理脚本 - 交互式版本
功能:
1. 基于指定前缀(如Nsyl/Ntab/Ntom)编号添加新的第一列
2. 对每个区块内的记录按起始位点排序
3. 添加自然数序列编号
4. 重构序列名称格式
5. 删除类型列
"""

import os

def extract_gff3(input_file, output_file, prefix):
    """处理GFF3文件的主函数"""
    # 将前缀首字母大写，确保格式一致
    prefix = prefix.capitalize()
    
    # 步骤1：读取输入文件
    print(f"读取文件: {input_file}")
    try:
        with open(input_file, 'r') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return False
    
    # 步骤2：创建一个字典来存储各个区块的数据
    gene_blocks = {}  # 格式: {基因编号: [记录列表]}
    
    # 步骤3：解析每一行数据
    for line in lines:
        # 跳过空行和注释行
        if line.strip() == "" or line.startswith("#"):
            continue
        
        # 分割行内容
        fields = line.strip().split()
        
        # 确保行有足够的字段
        if len(fields) < 6:
            print(f"警告: 跳过格式不正确的行: {line.strip()}")
            continue
        
        # 从第6列(索引5)提取基因编号
        attribute = fields[5]
        if prefix not in attribute:
            continue
            
        # 提取前缀后面的数字
        try:
            gene_part = attribute.split(prefix)[1]
            gene_num = int(gene_part.split("g")[0])
        except (IndexError, ValueError):
            print(f"警告: 无法从 '{attribute}' 提取 {prefix} 编号")
            continue
        
        # 创建记录
        record = {
            'seqid': fields[0],        # 序列名称
            'start': int(fields[2]),   # 起始位点
            'end': int(fields[3]),     # 终止位点
            'strand': fields[4],       # 转录方向
            'attribute': attribute     # 属性字段
        }
        
        # 将记录添加到对应的基因区块
        if gene_num not in gene_blocks:
            gene_blocks[gene_num] = []
        gene_blocks[gene_num].append(record)
    
    # 步骤4：处理每个基因区块并生成新的数据行
    result_lines = []
    
    # 按基因编号顺序处理
    for gene_num in sorted(gene_blocks.keys()):
        print(f"处理{prefix}{gene_num}区块...")
        
        # 获取当前区块的记录
        records = gene_blocks[gene_num]
        
        # 按起始位点排序
        sorted_records = sorted(records, key=lambda x: x['start'])
        
        # 为每条记录添加序号并创建新行
        for i, record in enumerate(sorted_records, 1):
            # 创建新的序列名称
            new_seqid = f"{prefix}{gene_num}g{i:05d}"  # 格式: 前缀<数字>g<五位数>
            
            # 构建新行
            new_line = [
                str(gene_num),          # 第一列: 基因编号
                new_seqid,              # 第二列: 新序列名称
                str(record['start']),   # 第三列: 起始位点
                str(record['end']),     # 第四列: 终止位点
                record['strand'],       # 第五列: 转录方向
                str(i),                 # 第六列: 序号
                record['attribute']     # 第七列: 原属性
            ]
            
            # 将新行添加到结果中
            result_lines.append("        ".join(new_line))
    
    # 步骤5：写入输出文件
    print(f"写入处理结果到: {output_file}")
    try:
        with open(output_file, 'w') as f:
            for line in result_lines:
                f.write(line + '\n')
        print(f"处理完成，共处理 {len(result_lines)} 条记录")
        return True
    except Exception as e:
        print(f"写入文件时出错: {e}")
        return False

# 主程序
if __name__ == "__main__":
    print("GFF3文件处理工具")
    print("-" * 50)
    
    while True:
        # 用户输入要处理的文件信息
        print("\n请输入文件信息")
        input_file = input("输入文件路径: ")
        
        # 检查输入文件是否存在
        if not os.path.exists(input_file):
            print(f"错误: 文件 '{input_file}' 不存在！")
            continue
        
        output_file = input("输出文件路径: ")
        prefix = input("基因ID前缀 (如Nsyl, Ntab, Ntom): ")
        
        # 处理文件
        success = extract_gff3(input_file, output_file, prefix)
        
        # 询问是否继续处理其他文件
        if success:
            choice = input("\n是否继续处理其他文件? (y/n): ")
            if choice.lower() != 'y':
                print("程序结束")
                break
        else:
            print("文件处理失败，请重试")
