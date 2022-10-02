from main_class import start
import time
from misc.get_dollar import get_cur_value

def main():
    DOCUMENT_ID = '1cWCWfbttC0H-3iC_RMGGp5FsRtBWyc6xxnGB1C5QB_0' # ID of a document 
    start_time = time.time()
    start(DOCUMENT_ID)
    end_time = time.time()
    print(f"{((end_time - start_time) * 1_000)} milliseconds elapsed")


if __name__ == "__main__":
    # main()
    main()