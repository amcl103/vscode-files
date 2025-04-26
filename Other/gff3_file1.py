# 定义一个处理gff3的函数
# input_file (str): 输入 GFF3 文件的路径
# output_file (str): 输出文件的路径
def extract_gff3(input_file, output_file):
    """
    读取输入的 GFF3 文件，并将包含 'transcript' 的行中，
    按照要求提取第 1、3、4、5、7、9 列，然后对最后一列使用 split 进行分割，
    最后写入输出文件。
    """
    # 打开输入文件进行读取'r'
    with open(input_file, 'r') as infile:
        # 打开输出文件进行写入，模式 'w' 会覆盖原文件
        with open(output_file, 'w') as outfile:
            # 遍历文件中的每一行
            for line in infile:
                # 跳过 GFF3 注释行（以 '##' 开头）
                if line.startswith('##'):
                    continue

                # 检查当前行是否包含 'transcript'
                if 'transcript' in line:
                    # 使用制表符分割该行，得到字段列表
                    fields = line.split('\t')
                    
                        # 提取第 1、3、4、5、7、9 列（索引分别为 0, 2, 3, 4, 6, 8）
                    selected_columns = [fields[i] for i in [0, 2, 3, 4, 6, 8]]
                        
                        # 对最后一列（第9列）使用 split 进行分割一次，分隔符为分号 ';'
                    split_files = selected_columns[-1].removeprefix('ID=').split(';',1)
                        
                    selected_columns[-1] = '\t'.join(split_files)
                    selected_columns[-1] = split_files[0]
                        
                        # 将处理后的各列数据接成一行,自定义间隔长度并写入文件
                    output_line = "          ".join(selected_columns)   
                    outfile.write(output_line + "\n")
                   

# 应用
input_file = 'text_files/ntom.gff3'
output_file = 'text_files/new_ntom.txt'

extract_gff3(input_file, output_file)

print("处理完成！")
