import time

class Logics:
    def __init__(self):
        self.tmp = ""

    """
    :param crwl_txt
        ########################################
        # Program: needle
        # Rundate: Wed 10 Jun 2020 07:21:44
        # Commandline: needle
        #    -auto
        #    -stdout
        #    -asequence emboss_needle-I20200610-072303-0479-94999719-p1m.asequence
        #    -bsequence emboss_needle-I20200610-072303-0479-94999719-p1m.bsequence
        #    -datafile EDNAFULL
        #    -gapopen 10.0
        #    -gapextend 0.5
        #    -endopen 10.0
        #    -endextend 0.5
        #    -aformat3 pair
        #    -snucleotide1
        #    -snucleotide2
        # Align_format: pair
        # Report_file: stdout
        ########################################
        
        #=======================================
        #
        # Aligned_sequences: 2
        # 1: EMBOSS_001
        # 2: EMBOSS_001
        # Matrix: EDNAFULL
        # Gap_penalty: 10.0
        # Extend_penalty: 0.5
        #
        # Length: 293
        # Identity:     271/293 (92.5%)
        # Similarity:   271/293 (92.5%)
        # Gaps:          18/293 ( 6.1%)
        # Score: 1282.5
        # 
        #
        #=======================================
        
        EMBOSS_001         1 AATATATCTTGTGGAAAGGACGAAACACCG--CATACTCGGGCGC-----     43
                             .|||||||||||||||||||||||||||||  ||| .||   |||     
        EMBOSS_001         1 TATATATCTTGTGGAAAGGACGAAACACCGCCCAT-TTC---CGCAAGAA     46
        
        EMBOSS_001        44 --CGGGGTGTTTTAGAGCTAGAAATAGCAAGTTAAAATAAGGCTAGACCG     91
                               |     ||||||||||||||||||||||||||||||||||||||.|||
        EMBOSS_001        47 AAC-----GTTTTAGAGCTAGAAATAGCAAGTTAAAATAAGGCTAGTCCG     91
        
        EMBOSS_001        92 TTATCAACTTGAAAAAGTGGCACCGAGTCGGTGCACATGCCAGGTGGACG    141
                             |||||||||||||||||||||||||||||||||||||||||||||.||||
        EMBOSS_001        92 TTATCAACTTGAAAAAGTGGCACCGAGTCGGTGCACATGCCAGGTAGACg    141
        
        EMBOSS_001       142 AGTTTTCTTGCTTTTTTTGATACTCTGTCTGTACTACAACGCCCATTTCC    191
                             ||||||||||||||||||||||||||||||||||||||||||||||||||
        EMBOSS_001       142 AGTTTTCTTGCTTTTTTTGATACTCTGTCTGTACTACAACGCCCATTTCC    191
        
        EMBOSS_001       192 GCAAGAAAACTGGTCTACCTGGCATGTTCAGCTTGGCGTACCGCGATCTC    241
                             ||||||||||||||||||||||||||||||||||||||||||||||||||
        EMBOSS_001       192 GCAAGAAAACTGGTCTACCTGGCATGTTCAGCTTGGCGTAcCgcGATCTC    241
        
        EMBOSS_001       242 TACTCTACCACTTGTACTTCAGCGGTCAGCTTACTCGACTTAA    284
                             |||||||||||||||||||||||||||||||||||||||||||
        EMBOSS_001       242 TACTCTACCACTTGTACTTCAGCGGTCAGCTTACTCGACTTAA    284
        
        
        #---------------------------------------
        #---------------------------------------
    """
    def extract_data(self, crwl_txt):
        crwl_txt_a_seq_name = crwl_txt[crwl_txt.index("# 1:") + len("# 1:"):]
        a_seq_name = crwl_txt_a_seq_name[:crwl_txt_a_seq_name.index("\n")]
        print("a_seq_name : " + a_seq_name)
        crwl_txt_b_seq_name = crwl_txt_a_seq_name[crwl_txt_a_seq_name.index("# 2:") + len("# 2:"):]
        b_seq_name = crwl_txt_b_seq_name[:crwl_txt_b_seq_name.index("\n")]
        print("b_seq_name : " + b_seq_name)

        crwl_txt_c = crwl_txt_b_seq_name[crwl_txt_b_seq_name.index("#=======================================") + len(
            "#======================================="):].replace("#---------------------------------------", "")
        crwl_txt_arr = crwl_txt_c.split("\n")

        return a_seq_name, self.filter_out_null_el_in_list(crwl_txt_arr)

    def filter_out_null_el_in_list(self, txt_arr):
        try:
            for i in range(len(txt_arr)):
                txt_arr.remove('')
        except:
            print("no blank element")
            return txt_arr

    def add_needle_result(self, final_idx, a_seq_name, crwl_txt_arr, needle_result_list):
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
        return needle_result_list.append([final_idx, a_seq, needle, b_seq])



