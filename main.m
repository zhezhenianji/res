clear; clc;close all;
excel                    ='乱序版-样本银行专利数据2012-2023.xlsx';
start = 1021; finale = 1360;
[pretreatment, combined] = dataprocessing(excel,start,finale);
% apitest        = call_deepseek_api(2,'hello world')%1-V3, 2-R1 %测试api
label1                   = prompt1(combined);
label2                   = prompt2(combined);
labeltxt                 = {'label1','label2'};
labeldata                = num2cell([label1(:,1),label2]);
label                    = [labeltxt;labeldata];
dealtreatment            = [pretreatment,label];


