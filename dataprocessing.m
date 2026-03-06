function [pretreatment, combined] = dataprocessing(excel,start,finale)
if exist('pretreatment.mat', 'file')
    load pretreatment
    disp('已加载 pretreatment');
else
    if ~evalin('base', 'exist(''pretreatment'', ''var'')')
        [data,txt]       = xlsread(excel,1);
        label            = {'code','bank','claim'};
        pretxt           = txt(start:finale, [8, 2, 11]);%'专利申请号'、'原始企业名称'、'主权项'
        pretreatment     = [label;pretxt];
        newcolumn        = cell(length(pretreatment), 1);
        cycledata        = mod(0:length(pretreatment)-2, 20) + 1;
        newcolumn(2:end) = num2cell(cycledata(:));
        newcolumn{1}     = "ind";
        leftpart         = pretreatment(:, 1:2); rightpart = pretreatment(:, 3:end);
        pretreatment     = [leftpart, newcolumn ,rightpart];
        count            = (length(pretreatment)-1)/20;
        combined         = cell(count, 1);
        for j = 1:count
            grouptext = "";
            for i = 1:20
                rowidx    = (j - 1)*20 + i + 1;
                id        = pretreatment{rowidx, 3};
                text      = pretreatment{rowidx, 4};
                line      = "第" + id + "条: " + text;
                grouptext = grouptext + newline + line;
            end
            combined{j}   = grouptext;
        end
        save('pretreatment.mat', 'pretreatment','combined');
        disp('pretreatment 不存在，已创建并保存。');
    else
        disp('pretreatment 已存在，跳过创建。');
    end
end









