import os 
import pathlib



TAB_1_MD = 'view/tab1.md'
TAB_2_MD = 'view/tab2.md'


MD_PATH_TAB_1 = str(pathlib.Path(__file__).parent.absolute()) + '/' + f'{TAB_1_MD}'
MD_PATH_TAB_2 = str(pathlib.Path(__file__).parent.absolute()) + '/' + f'{TAB_2_MD}'
