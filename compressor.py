import subprocess

def Compress(data):
    p = subprocess.Popen(['node', './panzerdogs_compressor/compress.js', data], stdout=subprocess.PIPE)
    result_string = str(p.stdout.read(), 'UTF-8')
    result_string = result_string.replace('\n', '')
    return result_string

