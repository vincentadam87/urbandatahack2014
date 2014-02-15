import os

DATA_DIR = os.path.join(os.path.dirname(os.getcwd()), 'data')
ANTI_SOCIAL_FN = os.path.join(DATA_DIR, 'WCC_CleansingAntiSocialBehaviour.csv')
LICENSING_FN = os.path.join(DATA_DIR, 'WCC_Licensing.csv')

def read_file(fn):
    with open(fn, 'r') as _file:
        for row in _file:
            print row

if __name__ == '__main__':
    read_file(ANTI_SOCIAL_FN)

