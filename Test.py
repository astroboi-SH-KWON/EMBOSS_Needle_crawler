from selenium import webdriver
from time import clock
import time


import Util
import LogicPrep
import Logic
############### start to set env ################
WEB_DRV_PATH = "C:/Users/terry/chromedriver.exe"

WORK_DIR = "D:/000_WORK/YuGooSang_KimHuiKwon/20200609/WORK_DIR/"
INPUT_EXCEL = "switching NGS analysis_Input.xlsx"
INPUT_TXT = ["gDNA_0609_test.txt"]

TARGET_URL = "https://www.ebi.ac.uk/Tools/psa/emboss_needle/"
############### end setting env  ################
OPT = webdriver.ChromeOptions()
OPT.add_argument("start-maximized")
WEB_DRV = webdriver.Chrome(chrome_options=OPT, executable_path=WEB_DRV_PATH)

def main():
    util = Util.Utils()
    logic_prep = LogicPrep.LogicPreps(WEB_DRV, TARGET_URL)
    logic = Logic.Logics()

    for input_file in INPUT_TXT:
        needle_result_list = []
        input_list = util.read_tb_txt(WORK_DIR + input_file)

        for val_arr in input_list:
            final_idx = val_arr[1]
            asequence = val_arr[3]  # NGS read
            bsequence = val_arr[4]  # Reference
            logic_prep.go_to_url(TARGET_URL)
            logic_prep.input_data_by_id("pn_stype", "dna")
            logic_prep.input_data_by_id("asequence", asequence)
            logic_prep.input_data_by_id("bsequence", bsequence)

            logic_prep.scroll_down()
            logic_prep.get_by_xpath("//div[@id='jd_submitButtonPanel']/input[@type='submit']", False).click()

            # print(WEB_DRV.current_url)
            logic_prep.go_to_url(WEB_DRV.current_url)
            logic_prep.get_by_xpath("//pre[@id='alignmentContent']", False)
            crwl_txt = logic_prep.get_by_xpath("//pre[@id='alignmentContent']", False).text

            a_seq_name, crwl_txt_arr = logic.extract_data(crwl_txt)
            # print(crwl_txt_arr)

            logic.add_needle_result(final_idx, a_seq_name, crwl_txt_arr, needle_result_list)

        util.make_excel(WORK_DIR + "crawler_output/result_" + input_file.replace(".txt", ""), needle_result_list)



def test():
    logic_prep = LogicPrep.LogicPreps(WEB_DRV, TARGET_URL)

    a_seq_name = "EMBOSS_001"
    b_seq_name = "EMBOSS_001"

    crwl_txt_arr = [
     'EMBOSS_001         1 TATATATCTTGTGGAAAGGACGAAACACCGGACAACCTCTACCTCCGCAG     50',
     '                     ||||||||||||||||||||||||||||||||||||||||||||||||||',
     'EMBOSS_001         1 TATATATCTTGTGGAAAGGACGAAACACCGGACAACCTCTACCTCCGCAG     50',
     'EMBOSS_001        51 --------------------------------------------------     50',
     '                                                                       ',
     'EMBOSS_001        51 TTTTAGAGCTAGAAATAGCAAGTTAAAATAAGGCTAGTCCGTTATCAACT    100',
     'EMBOSS_001        51 --------------------------------------------------     50',
     '                                                                       ',
     'EMBOSS_001       101 TGAAAAAGTGGCACCGAGTCGGTGCCACATGGCACGGTGCGGAGGTAGAG    150',
     'EMBOSS_001        51 -------TTTATTTTGCTATCTCTATACTAGTTTCGTGACAACCTCTACC     93',
     '                            |||.|||||||||||||||||||||||||||||||||||||||',
     'EMBOSS_001       151 GTTGTCATTTTTTTTGCTATCTCTATACTAGTTTCGTGACAACCTCTACC    200',
     'EMBOSS_001        94 TCCGCACGGTGCCATGTGAGTACAAAGCTTGGCGTACCGCGATCTCTACT    143',
     '                     ||||||||||||||||||||||||||||||||||||||||||||||||||',
     'EMBOSS_001       201 TCCGCACGGTGCCATGTGAGTACAAAGCTTGGCGTACCGCGATCTCTACT    250',
     'EMBOSS_001       144 CTACCACTTGTACTTCAGCGGTCAGCTTACTCGACTTAA    182',
     '                     |||||||||||||||||||||||||||||||||||||||',
     'EMBOSS_001       251 CTACCACTTGTACTTCAGCGGTCAGCTTACTCGACTTAA    289']

    idx = crwl_txt_arr[0][len(a_seq_name):].index("1")
    a_seq = ""
    needle = ""
    b_seq = ""
    for i in range(len(crwl_txt_arr)):
        tmp_str = crwl_txt_arr[i][len(a_seq_name) + idx + 2:]
        if i % 3 == 0:
            a_seq += tmp_str.split(" ")[0]
        elif i % 3 == 1:
            needle += tmp_str
        else:
            b_seq += tmp_str.split(" ")[0]

    print(a_seq)
    print(needle)
    print(b_seq)
    print(str(len(a_seq)))
    print(str(len(needle)))
    print(str(len(b_seq)))





start_time = clock()
print("start >>>>>>>>>>>>>>>>>>")
main()
# test()
print("::::::::::: %.2f seconds ::::::::::::::" % (clock() - start_time))