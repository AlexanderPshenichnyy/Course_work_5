from configparser import ConfigParser
import os

# Tinkoff, Озон, Сбер, RBT, Самокат, Спортмастер, REDMOND, Комус, 2ГИС, Табрис
employer_ids = [78638, 2180, 3529, 49105, 2460946, 2343, 61826, 5694, 64174, 59645]


JSON_DATA_DIR = os.path.join('data')
JSON_FILE_NAME = 'data.json'



def config(filename="database.ini", section="postgresql"):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    if parser.has_section(section):
        params = parser.items(section)
        db = dict(params)
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db