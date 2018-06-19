import os
from subprocess import Popen, PIPE
import csv
import psutil


class GPUChecker(object):
    def __init__(self):
        pass

    @staticmethod
    def process_info(pid):
        p = psutil.Process(pid)
        info = {
            'status': p.status(),
            'user': p.username(),
            'children_num': len(p.children())
        }
        return info

    @staticmethod
    def _int_parser(digit):
        try:
            digit = int(digit)
        except ValueError:
            digit = float('nan')
        return digit

    @staticmethod
    def _float_parser(digit):
        try:
            digit = float(digit)
        except ValueError:
            digit = float('nan')
        return digit

    @staticmethod
    def getAPP():
        p = Popen(["nvidia-smi",
                   "--query-compute-apps=gpu_uuid,pid,process_name,used_memory",
                   "--format=csv,noheader,nounits"], stdout=PIPE)

        output = p.stdout.read().decode('UTF-8')[:-1]
        lines = output.split(os.linesep)
        reader = csv.reader(lines)
        app_query = [{
            'gpu_uuid':q[0],
            'pid': q[1],
            'process_name': q[2],
            'used_memory': q[3]}
            for q in reader
        ]

        return app_query

    @staticmethod
    def getGPU():
        p = Popen(["nvidia-smi",
                   "--query-gpu=uuid,index,utilization.gpu,name,memory.total",
                   "--format=csv,noheader,nounits"], stdout=PIPE)

        output = p.stdout.read().decode('UTF-8')[:-1]
        lines = output.split(os.linesep)
        reader = csv.reader(lines)

        gpu_query = {
            q[0]: {
                'index': q[1],
                'utilization.gpu': q[2],
                'gpu_name': q[3],
                'total_memory': q[4],
                'process': []
            }
            for q in reader
        }

        return gpu_query

    def checkGPU(self):
        gpu_dict = GPUChecker.getGPU()
        app_list = GPUChecker.getAPP()
        for app in app_list:
            gpu_dict[app['gpu_uuid']]['process'] += [app]

        return self._parser(gpu_dict)

    def _parser(self, data):
        string =  '\u250c' + \
                  '\u2500' * 7 + '\u252c' +\
                  '\u2500' * 14 + '\u252c' +\
                  '\u2500' * 9 + '\u252c' +\
                  '\u2500' * 11 + '\u252c' +\
                  '\u2500' * 23 + '\u252c' +\
                  '\u2500' * 10 +\
                  '\u2510' + '\n'

        string += '\u2502 GPU # \u2502 Memory Usage \u2502   PID   ' \
                  '\u2502 User Name \u2502      Process Name     \u2502  Status  \u2502\n'
        for uuid, val in data.items():
            string += '\u251c' + \
                      '\u2500' * 7 + '\u253c' +\
                      '\u2500' * 14 + '\u253c' +\
                      '\u2500' * 9 + '\u253c' +\
                      '\u2500' * 11 + '\u253c' +\
                      '\u2500' * 23 + '\u253c' +\
                      '\u2500' * 10 +\
                      '\u2524'
            string += '\n\u2502{:^7}\u2502{:^14}\u2502{:^9}\u2502{:^11}\u2502{:^23}\u2502{:^10}\u2502\n'.format(
                val['index'], '', '', '', '', ''
            )
            if val['process'] == []:
                string += '\u2502{:^7}\u2502{:^14}\u2502{:^9}\u2502{:^11}\u2502{:^23}\u2502{:^10}\u2502\n'\
                    .format('', '', '', 'Idle', '', '')
            for p in val['process']:
                process = psutil.Process(int(p['pid']))
                user = process.username()
                process_name = process.name()
                status = process.status()
                string += '\u2502{:^7}\u2502{:^14}\u2502{:^9}\u2502{:^11}\u2502{:^23}\u2502{:^10}\u2502\n'.format(
                    '', p['used_memory'], p['pid'], user if len(user) < 11 else user[:10],
                    process_name if len(process_name) < 23 else process_name[:22],
                    status if len(status) < 10 else status[:9],
                )
        string += '\u2514' + \
                  '\u2500' * 7 + '\u2534' +\
                  '\u2500' * 14 + '\u2534' +\
                  '\u2500' * 9 + '\u2534' +\
                  '\u2500' * 11 + '\u2534' +\
                  '\u2500' * 23 + '\u2534' +\
                  '\u2500' * 10 +\
                  '\u2518' + '\n'
        return string

if __name__ == '__main__':
    checker = GPUChecker()
    print(checker.checkGPU())


