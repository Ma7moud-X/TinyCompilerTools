from parser import Parser
from scanner import Scanner

input_filepath = './test.txt'
output_filepath = './output.txt'
p = Scanner(input_filepath, output_filepath)
tokens = p.scan_file()

parser = Parser(tokens)
parser.parse()