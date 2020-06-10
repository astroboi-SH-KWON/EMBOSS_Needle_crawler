from selenium import webdriver
from time import clock


import Util
import LogicPrep
import Logic
############### start to set env ################
WEB_DRV_PATH = "C:/Users/terry/chromedriver.exe"

WORK_DIR = "D:/000_WORK/YuGooSang_KimHuiKwon/20200609/WORK_DIR/"
INPUT_EXCEL = "switching NGS analysis_Input.xlsx"
INPUT_TXT = ["gDNA_0609.txt", "Plasmid_0609.txt"]

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

            logic_prep.go_to_url(WEB_DRV.current_url)
            logic_prep.get_by_xpath("//pre[@id='alignmentContent']", False)
            crwl_txt = logic_prep.get_by_xpath("//pre[@id='alignmentContent']", False).text

            a_seq_name, crwl_txt_arr = logic.extract_data(crwl_txt)

            logic.add_needle_result(final_idx, a_seq_name, crwl_txt_arr, needle_result_list)

        util.make_excel(WORK_DIR + "first_excel_output/result_" + input_file.replace(".txt", ""), needle_result_list)

start_time = clock()
print("start >>>>>>>>>>>>>>>>>>")
main()
print("::::::::::: %.2f seconds ::::::::::::::" % (clock() - start_time))