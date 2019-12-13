import logging
import argparse
import fileinput
from decimal import Decimal

def validate(clm_type_aggr,trail_rec):
    calc_clm_type_aggrs={}
    aggrs=trail_rec.split(";")
    i=0
    for aggr in aggrs:
        if len(aggr)== 2:
            i_amt= Decimal(aggrs[i+1])
            i_count=int(aggrs[i+2])
            calc_clm_type_aggrs[aggr]=(i_amt,i_count)
        i=i+1
    if str(clm_type_aggr)==str(calc_clm_type_aggrs):
        print("matched")
    else:
        print("mismatched")
    print("file_aggrs: {0}".format(str(calc_clm_type_aggrs)))
    print("calc_aggrs: {0}".format(str(clm_type_aggr)))

def aggr_data(clm_type_aggr,clm_type_cd,clm_pd_amt):
   if clm_type_cd in clm_type_aggr:
       lst=list(clm_type_aggr[clm_type_cd])
       t_clm_amt = lst[0]
       clm_count = lst[1]
       clm_count = clm_count + 1
       t_clm_amt = t_clm_amt + clm_pd_amt
       upd_aggr=(t_clm_amt,clm_count)
       clm_type_aggr[clm_type_cd]=upd_aggr
   else:
       print("adding claim type {0}".format(clm_type_cd))
       clm_type_aggr[clm_type_cd]=(clm_pd_amt,1)
   return clm_type_aggr
if __name__ == "__main__":
    print ("this is main")
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_name",type=str,help="name of the NCH file to be validated",required=True)
    args=parser.parse_args()
    file_name = args.file_name
    clm_type_aggr={}
    prev_rec=""
    for line in fileinput.input(file_name):
        prev_rec = str(line)
        #print("first char of line {0}".format(line[:1]))
        awsmetadata = ""
        if((line[9:11]) == "72" or (line[9:11]) == "71" or (line[9:11]) == "81" or (line[9:11])=="82") and line[:1] =="+":
            paid_amt = line[241:254]
            #print("is 70 or 80")
           #print("clm_type_cd {0}".format(line[9:11]))
            #print(paid_amt)
            clm_type_aggr = aggr_data(clm_type_aggr, line[9:11], Decimal(paid_amt))
        elif (line[9:11]) >= "00" and (line[9:11]) <="99" and line[:1] =="+":
            #print('not 70 or 80')
            paid_amt = line[244:257]
            #print(paid_amt)
            #print("clm_type_cd {0}".format(line[9:11]))
            clm_type_aggr= aggr_data(clm_type_aggr,line[9:11],Decimal(paid_amt))
        elif (line[7:8]) == "S" :
            print("Trailer record")
        elif (line[7:8])  == "D":
            print("Header record")
        else:
            print("none of the above")
            print(line)
            validate(clm_type_aggr, prev_rec)
