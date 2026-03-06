import pandas  as pd
from tqdm import tqdm
import time
import numpy as np
import requests
import json
import akshare as ak
from playwright.sync_api import sync_playwright
import pywencai

pd.set_option('future.no_silent_downcasting', True)

SAVE_PATH = r"C:\Users\25766\Desktop\code\python\stock\login_state.json"

def res(hdate, qdate):
    news = []
    for h, q, i in tqdm(zip(hdate, qdate,range(len(hdate))), total=len(hdate)):
        # for _, row in tqdm(new.iloc[0:1].iterrows(), total=1):
        print(f"正在处理 q={q}")
        try:
               
                st    = "200"
                sb    = qqrenqz(q,st)
                sb    = sb.query('1<人气')
                sb    = sb.iloc[:, [0,1,2,3,4]]
                st    = "1000"
                eb    = qqrenqz(h,st)
                eb    = eb.iloc[:, [0,5,6,7]]
                df    = sb.merge(eb,on='股票简称',how='left')
                new   = df

                time.sleep(1)
                new['日期']   = q
                news.append(new) 
        except Exception as e:
                print(f"处理 q={q}时出错: {e}")
                error_df = pd.DataFrame([{'错误信息': str(e), '日期': q}])
                news.append(error_df)
    news_df = pd.concat(news, axis=0, ignore_index=True) if news else pd.DataFrame()
    return news_df

def qqrenqz(qdate, st):
    date          = "2026-" + qdate.replace('.', '-')
    url           ="https://apphis.longhuvip.com/w1/api/index.php"
    headers       = {
        "User-Agent": "lhb/5.18.5 (com.kaipanla.www; build:2; iOS 16.3.1) Alamofire/4.9.1",
        "Accept": "*/*"}
    data           = {
        "a": "HisRankingInfo_W8",      
        "c": "HisStockRanking",    
        "PhoneOSNew": "1",                    
        "VerSion": "5.21.0.2", 
        "Date" : date,                                 
        "apiv": "w42",
        "Order":"1",
        "st":st,
        "Isst":"1",
        "index":"0",
        "Type":"42",#6zf.42q
        "FilterMotherboard":"0",
        "Filter":"1",
        "Ratio":"6",#6q1bai
        "FilterBJS":"1",
        "FilterTIB":"1",
        "FilterGem":"1"
        }
    response          = requests.post(url, data=data,headers=headers)
    raw_list          = response.json().get("list", [])  
    raw_df            = pd.DataFrame(raw_list) 
    df                = pd.DataFrame()
    df['code']        = raw_df.iloc[:, 0]
    df['股票简称']     = raw_df.iloc[:, 1]
    df['人气']        = raw_df.iloc[:, 58]/10000
    df['板数']         = raw_df.iloc[:, 23]
    df['标签']         = raw_df.iloc[:, 39]
    # df['成交额']         = raw_df.iloc[:, 7]/100000000
    # df['市值']         = raw_df.iloc[:, 10]/100000000
    # df['概念']         = raw_df.iloc[:, 4]
    # df['区间']         = raw_df.iloc[:, 20]
    # df['竞价']         = raw_df.iloc[:, 36]
    # df['涨幅']         = raw_df.iloc[:, 54]
    df                = df.replace('', np.nan) 
    df                = df.dropna(subset=['板数'])
    # df = df[df['板数'] == '首板']
    # df   = df.query('人气>1').sort_values(by='人气', ascending=False)
    # df.insert(1, '人气序号', range(1, len(df) + 1))
    return raw_df 

def qrenqz(qdate, st):
    date          = "2025-" + qdate.replace('.', '-')
    url           ="https://apphis.longhuvip.com/w1/api/index.php"
    headers       = {
    "User-Agent": "lhb/5.18.5 (com.kaipanla.www; build:2; iOS 16.3.1) Alamofire/4.9.1",
    "Accept": "*/*"}
    data           = {
    "Order":"1",
    "TSZB":"0",
    "a": "ZhiShuStockList_W8",      
    "c": "ZhiShuRanking",    
    "PhoneOSNew": "1",                    
    "VerSion": "5.21.0.2", 
    "Date" : date,                                 
    "apiv": "w42",
    "old":"1",
    "st":st,
    "IsZZ":"0",
    "index":"0",
    "Token":"0",
    "IsKZZType":"0",
    "TSZB_Type":"0",
    "Type":"42",
    "UserID":"0",
    "PlateID":"801900",
    }
    # response = requests.post(url, data=data,headers=headers,verify=False)
    response          = requests.post(url, data=data,headers=headers)
    raw_list          = response.json().get("list", [])  
    raw_df            = pd.DataFrame(raw_list)
    df                = pd.DataFrame()
    df['股票简称']     = raw_df.iloc[:, 1]
    # df['人气']        = raw_df.iloc[:, 58]/10000
    # df['板数']         = raw_df.iloc[:, 23]
    # df['概念']         = raw_df.iloc[:, 4]
    df['区间']         = raw_df.iloc[:, 20].apply(pd.to_numeric, errors='coerce')
    df['涨幅']         = raw_df.iloc[:, 54].apply(pd.to_numeric, errors='coerce')
    df['竞价']         = df['涨幅']-df['区间'] 
    # df                = df.replace('', np.nan) 
    # df                = df.dropna(subset=['板数'])
    # df.insert(1, '序号', range(1, len(df) + 1))
    # jr                = df.query('3<人气').sort_values(by='人气', ascending=False)
    return df
  
def ban_shu(df):
    
    df   = df.query('人气>1').sort_values(by='人气', ascending=False)
    col3 = df['板数'].copy()
    col3 = col3.str.replace('连', '', regex=False)
    col3 = col3.str.replace(r'\d+天', '', regex=True)
    col3 = col3.str.replace('首板', '1板', regex=False)
    col3 = col3.str.extract(r'(\d+)板')[0]  
    nums = pd.to_numeric(col3, errors='coerce')
    valid_mask = nums.between(1, 15, inclusive='both') 
    df_clean = df[valid_mask].copy()
    df_clean['板数'] = nums[valid_mask].astype(int)
    return df_clean

def zt(qdate):
    query = f"{qdate}涨停"
    res   = pywencai.get(query=query, sort_order='asc', loop=True)
    res['market_code'] = pd.to_numeric(res['market_code'], errors='coerce')
    res   = res[res['market_code'].isin([17, 33])]
    df    = res.iloc[:, [1,9,16,19]]
    return df

def jqka(df, qdate):
    shang = df[df["code"].str.startswith(("60", "68"))]
    shen  = df[df["code"].str.startswith(("00", "30"))]
    def fetch_data(df, market_id, context, qdate):
        results = []
        target_date = f"2026-{qdate.replace('.', '-')}"
        for _, row in tqdm(df.iterrows(), total=len(df), desc=f"Market {market_id}"):
            daima = row['code']
            url = f"https://flow.10jqka.com.cn/app/anomaly_analysis/history?marketId={market_id}&thsHqCode={daima}&client_userid=Bc8wb&back_source=hyperlink&share_hxapp=isc&fontzoom=no"
            page = context.new_page()
            try:
                page.goto(url, timeout=60000)
                page.wait_for_load_state("networkidle", timeout=30000) 
                reasons_items = page.locator('div.reason-item')
                count = reasons_items.count()
                for i in range(count):
                    item = reasons_items.nth(i)
                    date_locator = item.locator('div.time')
                    date = date_locator.text_content().strip()
                    if date == target_date:
                        # print(f"找到目标日期 {target_date} 的相关信息:")
                        keywords = item.locator('.keywords').text_content().strip()
                        details = item.locator('.reason').last.text_content().strip()
                        # print("关键词:", keywords)
                        # print("详细内容:", details)

                results.append({
                    'code': daima,
                    '股票简称': row['股票简称'],
                    'ths标题': keywords,
                    'ths内容': details,
                })
            except Exception as e:
                print(f"抓取失败 {daima}: {e}")
                results.append({
                    'code': daima,
                    '股票简称': row['股票简称'],
                    'ths标题': None,
                    'ths内容': None,
                })
            finally:
                page.close()
                time.sleep(1)  
        return results
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='msedge', headless=True)
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36..."
        )
        results.extend(fetch_data(shen, market_id=33, context=context,qdate=qdate))
        results.extend(fetch_data(shang, market_id=17, context=context,qdate=qdate))

        context.close()
        browser.close()
    df = pd.DataFrame(results)
    output_path = r"C:\Users\25766\Desktop\code\python\stock\ths.xlsx"
    df.to_excel(output_path, index=False, engine='openpyxl')
    print(f"📊 数据已保存到: {output_path}") 
    return df

def kaipanla(df,qdate):
    def kpl(stock_id):
        params = {
                "Index": "0",
                "PhoneOSNew": "2",
                "StockID": stock_id,
                "VerSion": "5.18.0.5",
                "a": "GetDayZhangTing",
                "apiv": "w39",
                "c": "HisLimitResumption",
                "st": "20"}

        headers = {
                "User-Agent": "lhb/5.18.5 (com.kaipanla.www; build:2; iOS 16.3.1) Alamofire/4.9.1",
                "Accept": "*/*"}

        response = requests.get(
            "https://apphis.longhuvip.com/w1/api/index.php",params = params,headers = headers)
        raw_json = response.json()

        news_df = pd.DataFrame([
            {"GNSM": item.get("GNSM"), "Date": item.get("Date")}
            for item in raw_json.get("List", [])
            if isinstance(item, dict)])
        news_df["Date"] = pd.to_datetime(news_df["Date"], errors="coerce").dt.strftime("%m.%d")
        return news_df
    
    def fetch_data(df, qdate):
        results = []
        for _, row in tqdm(df.iterrows(), total=len(df)):
            daima = row['code']
            try:
                dff = kpl(daima)
                target_row = dff[dff['Date'] == qdate]
                details    = target_row['GNSM'].values[0]
                results.append({
                        'code': daima,
                        '股票简称': row['股票简称'],
                        'kpl内容': details,})
            except Exception as e:
                print(f"抓取失败 {daima}: {e}")
                results.append({
                    'code': daima,
                    '股票简称': row['股票简称'],
                    'kpl内容': None, })
            finally:
                time.sleep(1)  
        return results
    results = fetch_data(df, qdate)
    df = pd.DataFrame(results)
    output_path = r"C:\Users\25766\Desktop\code\python\stock\kpl.xlsx"
    df.to_excel(output_path, index=False, engine='openpyxl')
    print(f"📊 数据已保存到: {output_path}") 
    return df

def jygs(qdate):  
    qdate = qdate.replace('.', '-')
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='msedge', headless=True)
        context = browser.new_context(
                  viewport={"width": 1920, "height": 1080},
                  user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...")
        url = f"https://www.jiuyangongshe.com/action/2026-{qdate}"
        SAVE_PATH = r"C:\Users\25766\Desktop\code\python\stock\login_state.json"
        # storage = context.storage_state()
        # with open("login_state.json", "w", encoding="utf-8") as f:json.dump(storage, f, ensure_ascii=False, indent=2)
        with open(SAVE_PATH, "r", encoding="utf-8") as f: storage_state = json.load(f)
        context = browser.new_context(storage_state=storage_state)
        page = context.new_page()
        page.goto(url, timeout=600000)
        page.wait_for_load_state("networkidle", timeout=300000) 
        page.wait_for_selector("text=全部异动解析", timeout=100000)
        page.click("text=全部异动解析")
        page.wait_for_selector("text=展开板块", timeout=100000)
        expand_buttons = page.query_selector_all("text=展开板块")
        print(f"找到 {len(expand_buttons)} 个“展开板块”按钮")
        for i, btn in enumerate(expand_buttons):
            try:
                if btn.is_visible():
                    # print(f"点击第 {i+1} 个按钮")
                    btn.click()
            except Exception as e:
                print(f"点击第 {i+1} 个按钮失败: {e}")
        page.wait_for_selector(".shrink.fs15-bold", state="attached", timeout=10000)
        page.wait_for_selector("a.color-444", state="attached", timeout=10000)
        page.wait_for_function(
            "() => Array.from(document.querySelectorAll('a.color-444')).some(a => a.textContent.includes('1、'))",
        timeout=15000)
        items = page.query_selector_all("ul > li:has(.shrink.fs15-bold)")
        names = []
        contents = []
        for item in items:
            name_el = item.query_selector(".shrink.fs15-bold")
            content_el = item.query_selector("a.color-444")
            if name_el and content_el:
                names.append(name_el.text_content().strip())
                contents.append(content_el.text_content().strip())
        browser.close()
        df = pd.DataFrame({"股票简称": names,"jygs": contents})
        df = df.drop_duplicates().reset_index(drop=True)
        print(f"数据行数: {len(df)}")
        output_path = r"C:\Users\25766\Desktop\code\python\stock\jygs.xlsx"
        df.to_excel(output_path, index=False, engine='openpyxl')
        print(f"📊 数据已保存到: {output_path}") 
    return df

def date_sel():
    df             = ak.tool_trade_date_hist_sina()
    dates          = pd.to_datetime(df['trade_date'])
    trading        = dates[dates.dt.year == 2025]
    start_date     = '2025-12-01'
    selected_dates = trading[trading >= start_date]
    dates          =  selected_dates.dt.strftime('%m.%d').tolist()#  '01.02'
    # dates          = dates[160:]
    hdate          = dates[1:]
    qdate          = dates[:-1]
#  qdate = (
#     '01.05','01.06','01.07','01.08','01.09',
#     '01.12','01.13','01.14','01.15','01.16',
#     '01.19')
# hdate = (
#     '01.06','01.07','01.08','01.09',
#     '01.12','01.13','01.14','01.15','01.16',
#     '01.19','01.20')
# new= res(hdate, qdate)
    return hdate, qdate

def jygs_state(qdate):
    URL = f"https://www.jiuyangongshe.com/action/2026-{qdate}"
    SAVE_PATH = r"C:\Users\25766\Desktop\code\python\stock\login_state.json"
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='msedge',headless=False)
        context = browser.new_context(
                    viewport={"width": 1920, "height": 1080},
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...")
        page   = context.new_page()
        page.goto(URL)
        print("请手动扫码登录韭研公社...")
        input(">>> 登录完成后，请按 Enter 键...")
        context.storage_state(path=SAVE_PATH)
        print(f"✅ 完整登录状态已保存到 {SAVE_PATH}")
        browser.close()
        
def hz(qdate):  
    df_zt   = zt(qdate)
    df_ths  = jqka(df_zt, qdate)
    df_kpl  = kaipanla(df_zt, qdate)
    df_jygs = jygs(qdate)
    path_jygs = r"C:\Users\25766\Desktop\code\python\stock\jygs.xlsx"
    df_jygs   = pd.read_excel(path_jygs)
    path_ths  = r"C:\Users\25766\Desktop\code\python\stock\ths.xlsx"
    df_ths    = pd.read_excel(path_ths)
    path_kpl  = r"C:\Users\25766\Desktop\code\python\stock\kpl.xlsx"
    df_kpl    = pd.read_excel(path_kpl)
    df        = (df_jygs
        .merge(df_ths,  on='股票简称', how='left')
        .merge(df_kpl, on='股票简称', how='left')
        .merge(df_zt,  on='股票简称', how='left'))
    df = df.iloc[:, [0,1,3,4,6,7,8]]
    df = df.iloc[:, [0,1,3,4]]
    output_path = fr"C:\Users\25766\Desktop\论文\iCloudDrive\{qdate}hz.xlsx"
    df.to_excel(output_path, index=False, engine='openpyxl')
    print(f"📊 数据已保存到: {output_path}")  
    return df
       
qdate   = '03.05'
st      = "100"
huiz   = hz(qdate)



