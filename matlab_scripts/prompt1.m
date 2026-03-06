function  label1=prompt1(combined)
label1  = zeros(length(combined) * 20,2) ;
prompt1 = ['假如你是一名研究银行金融科技创新的学术领域专家，银行的20个专利文本，' ...
    '请分析其内容后，以金融科技创新为依据，判断专利质量高低，在0-1的区间内进行打分，' ...
    '形成表格，注意分数需要有一定的区分性表格列为，专利编号，质量评分，' ...
    '按专利编号升序排列'];%高质量专利
totaltime = 0;
k = [];
for j = 1:size(combined, 1)
    tic;
    prompt1      = combined{j} + newline + prompt1;
    %scores      = rand(20, 1);%测试
    response     = call_deepseek_api(1, prompt1);
    scores       = regexp(response, '(?<=\|)\s*(\d+\.\d+)\s*(?=\|)', 'tokens');
    scores       = str2double([scores{:}])';
    binaryscores = double(scores > 0.8); %门槛0.8
    %0.3-0.5边界
    [binaryscores,scores,k]=validbinaryscoresfound(binaryscores,scores,j,k);
    for i = 1:20
        rowidx           = (j - 1)*20 + i ;
        label1(rowidx,1) = binaryscores(i) ;
        label1(rowidx,2) = scores(i) ;
    end
    singleime  = toc;
    totaltime  = totaltime + singleime;
    fprintf('第 %d 次，总共 %d 次\n', j, size(combined, 1));
    fprintf('单次用时: %.4f 秒\n'   , singleime);
    fprintf('累计用时: %.4f 秒\n'   , totaltime);
end
  fprintf('第 %d 次未能找到binaryScores。\n', k);
end
function [binaryscores,scores,k]=validbinaryscoresfound(binaryscores,scores,j,k)
maxattempts            = 5;
attempt                = 0;
validbinaryscoresfound = false;
while ~validbinaryscoresfound && attempt < maxattempts
    attempt = attempt + 1;
    %scores      = rand(20, 1);%测试
    response = call_deepseek_api(2, prompt1);
    scores = regexp(response, '(?<=\|)\s*(\d+\.\d+)\s*(?=\|)', 'tokens');
    scores = str2double([scores{:}]);   
    binaryscores = double(scores > 0.8);
    numones      = sum(binaryscores);
    if numones   >= 6 && numones <= 10
        validbinaryscoresfound = true;
    end
end
if ~validbinaryscoresfound
    k = [k; j];
end
end
