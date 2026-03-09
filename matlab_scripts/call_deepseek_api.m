function deepseek_response = call_deepseek_api(modelnum,prompt)
%modelnum 1-V3, 2-R1
api_url = 'https://api.deepseek.com/v1/chat/completions';
api_key = 'sk-799';
headers = matlab.net.http.HeaderField(...
    'Content-Type', 'application/json',...
    'Authorization', ['Bearer ' api_key]);
options = weboptions(...
    'HeaderFields', headers,...
    'ContentType', 'json',...
    'Timeout', 30);
modellist = {'deepseek-chat','deepseek-reasoner'};
request_body = struct(...
    'model', modellist{modelnum},...
    'messages', {{struct('role', 'user', 'content', prompt)}},...
    'temperature', 0.7);
json_body = jsonencode(request_body);
try
    response = webwrite(api_url, json_body, options);
    if isfield(response, 'choices') && ~isempty(response.choices)
        deepseek_response = response.choices(1).message.content;
    else
        deepseek_response = 'Error: No response content found';
    end
catch ME
    if contains(ME.message, '401')
        error('认证失败: 1.检查API密钥 2.确认账号状态');
    elseif contains(ME.message, '400')
        error('请求格式错误: %s', ME.message);
    elseif contains(ME.message, '429')
        error('请求超限: 1.检查套餐额度 2.降低请求频率');
    else
        error('API请求失败: %s', ME.message);
    end
end

end
