import mysql.connector
import os
import glob
import re
import datetime
import time
import mypsw

mode = 3

markets_type = {
    1: "加密货币",
    2: "全球股指",
    3: "商品期货"
    }

patterns = {
    ##HTML 1: 加密货币美元
    #<tr>
    #        <td class="rank icon">1</td>
    #        <td class="flag"><i class="cryptoIcon c_bitcoin middle"></i></td>
    #        <td class="left bold elp name cryptoName first js-currency-name" title="Bitcoin"><a href="https://cn.investing.com/crypto/bitcoin" target="_blank" boundblank="">比特币</a></td>
    #        <td class="left noWrap elp symb js-currency-symbol" title="BTC">BTC</td>
    #        <td class="price js-currency-price"><a class="pid-1057391-last" href="https://cn.investing.com/crypto/currency-pairs?c1=189&amp;c2=12" target="_blank" boundblank="">10,859.6</a></td>
    #        <td class="js-market-cap" data-value="195042217484.97">$195.04B</td>
    #        <td class="js-24h-volume" data-value="16076563170.418">$16.08B</td>
    #        <td class="js-total-vol">32.03%</td>
    #        <td class="js-currency-change-24h greenFont pid-1057391-pcp">+5.42%</td>
    #        <td class="js-currency-change-7d redFont">-4.25%</td>
    #        </tr>
    #<tr>
    #<tr>
    #        <td class="rank icon">3</td>
    #        <td class="flag"><i class="cryptoIcon c_ripple middle"></i></td>
    #        <td class="left bold elp name cryptoName first js-currency-name" title="XRP"><a href="/crypto/ripple" target="_blank" boundblank="">瑞波币</a></td>
    #        <td class="left noWrap elp symb js-currency-symbol" title="XRP">XRP</td>
    #        <td class="price js-currency-price"><a class="pid-1057392-last" href="/crypto/currency-pairs?c1=197&amp;c2=12" target="_blank" boundblank="">0.27881</a></td>
    #        <td class="js-market-cap" data-value="12026861831.964">$12.03B</td>
    #        <td class="js-24h-volume" data-value="1207563829.5458">$1.21B</td>
    #        <td class="js-total-vol">2.41%</td>
    #        <td class="js-currency-change-24h redFont pid-1057392-pcp">-0.99%</td>
    #        <td class="js-currency-change-7d redFont">-6.50%</td>
    #</tr>
    1: r'<tr>.+?title="([^><"]+)"><a\shref=".+?/crypto/([^><"]+).+?boundblank="">([^><"]+)</a></td>.+?title="([^><"]+)">.+?class="pid-(\d+)-last".+?</tr>',
    
    ##HTML 2: 全球股指
    #<tr>
	#    <td class="flag">
    #    <span title="中国" class="ceFlags China">&nbsp;</span></td>
	#    <td class="bold left plusIconTd noWrap elp"><a title="上证指数" href="/indices/shanghai-composite" target="_blank" boundblank="">上证指数</a><span class="alertBellGrayPlus js-plus-icon genToolTip oneliner" data-tooltip="创建提醒" data-name="上证指数" data-id="40820"></span></td>
    #    <td class="pid-40820-last">2,880.00</td>
    #    <td class="pid-40820-high">2,892.08</td>
	#    <td class="pid-40820-low">2,875.00</td>
	#    <td class="bold pid-40820-pc redFont">-3.09</td>
	#    <td class="bold pid-40820-pcp redFont">-0.11%</td>
	#    <td class="pid-40820-time" data-value="1566287837">15:57:17</td>
	#    <td class="icon"><span class="redClockIcon">&nbsp;</span></td>
    #</tr>
    #<tr>
	#    <td class="flag"><span title="中国" class="ceFlags China">&nbsp;</span></td>
	#    <td class="bold left plusIconTd noWrap elp"><a title="道琼斯上海指数" href="/indices/dj-shanghai" target="_blank" boundblank="">道沪指数</a><span class="alertBellGrayPlus js-plus-icon genToolTip oneliner" data-tooltip="创建提醒" data-name="道琼斯上海指数" data-id="954522"></span></td>
    #                <td class="pid-954522-last">415.78</td>
    #    		    <td class="pid-954522-high">417.32</td>
	#    <td class="pid-954522-low">415.00</td>
	#    <td class="bold pid-954522-pc redFont">-0.44</td>
	#    <td class="bold pid-954522-pcp redFont">-0.11%</td>
	#    <td class="pid-954522-time" data-value="1566287819">15:56:59</td>
	#    <td class="icon"><span class="redClockIcon">&nbsp;</span></td>
    #</tr>
    2: r'<tr>.+?<a\stitle="([^><"]+)"\shref=".+?/indices/([^><"]+).+?boundblank="">([^><"]+)</a>.+?data-name="([^><"]+)"\sdata-id="(\d+)".+?</tr>',
    #<tr>
    #	<td class="flag"><span title="" class="ceFlags gold">&nbsp;</span></td>
    #	<td class="bold left plusIconTd noWrap elp"><a title="黄金期货" href="/commodities/gold" target="_blank" boundblank="">黄金</a><span class="alertBellGrayPlus js-plus-icon genToolTip oneliner" data-tooltip="创建提醒" data-name="黄金期货 (F)" data-id="8830"></span></td>
	#    <td class="left noWrap">2019年12月 </td>
    #    <td class="pid-8830-last">1,511.25</td>
    #    <td class="pid-8830-high">1,512.45</td>
   	#    <td class="pid-8830-low">1,503.10</td>
   	#    <td class="bold redFont pid-8830-pc">-0.35</td>
   	#    <td class="bold redFont pid-8830-pcp">-0.02%</td>
   	#    <td class="pid-8830-time" data-value="1566290438">16:40:38</td>
   	#    <td class="icon"><span class="greenClockIcon">&nbsp;</span></td>
    #</tr>
    3: r'<tr>.+?<a\stitle="([^><"]+)"\shref=".+?/commodities/([^><"]+).+?boundblank="">([^><"]+)</a>.+?data-name="([^><"]+)"\sdata-id="(\d+)".+?</tr>'
    }

html_path = {
    1: "HTML\\*数字货币*.htm*",
    2: "HTML\\*股指*.htm*",
    3: "HTML\\*商品期货*.htm*"
    }

base_currency_en = {
    1: "USD",
    2: "",
    3: "USD"
    }

base_currency_zh = {
    1: "美元",
    2: "",
    3: "美元",
    }

dirs = glob.glob( html_path[mode] )

insert_val = []
insert_dict = {}

for file_path in dirs:
    print( file_path )
    file = open( file_path, "r", encoding="utf-8" )
    time.sleep(1)
    file_str = file.read()
    symbols_match = re.finditer(patterns[mode],file_str,re.S)
    for symbol_match in symbols_match:
        symbol_dict = {}
        symbol_alias1 = str(symbol_match.group(1)).upper().replace("-","").replace(" ","").replace("&","").replace("/","").replace("AMP;","")
        symbol_alias2 = str(symbol_match.group(2)).upper().replace("-","").replace(" ","").replace("&","").replace("/","").replace("AMP;","")
        symbol_alias3 = str(symbol_match.group(3)).upper().replace("-","").replace(" ","").replace("&","").replace("/","").replace("AMP;","")
        symbol_alias4 = str(symbol_match.group(4)).upper().replace("-","").replace(" ","").replace("&","").replace("/","").replace("AMP;","")
        symbol_id = symbol_match.group(5)
        symbol_dict[symbol_alias1] = symbol_alias1
        symbol_dict[symbol_alias2] = symbol_alias2
        symbol_dict[symbol_alias3] = symbol_alias3
        symbol_dict[symbol_alias4] = symbol_alias4

        for symbol_alias in symbol_dict:
            if symbol_alias not in insert_dict:
                insert_val.append((
                        symbol_alias,
                        str(symbol_id),
                        markets_type[mode]
                        ))
                insert_dict[symbol_alias] = symbol_alias
            if base_currency_en[mode]:
                symbol_alias_curr_en = symbol_alias+base_currency_en[mode]
                if symbol_alias_curr_en not in insert_dict:
                    insert_val.append((
                            symbol_alias_curr_en,
                            str(symbol_id),
                            markets_type[mode]
                            ))
                    insert_dict[symbol_alias_curr_en] = symbol_alias_curr_en
            if base_currency_zh[mode]:
                symbol_alias_curr_zh = symbol_alias+base_currency_zh[mode]
                if symbol_alias_curr_zh not in insert_dict:
                    insert_val.append((
                            symbol_alias_curr_zh,
                            str(symbol_id),
                            markets_type[mode]
                            ))
                    insert_dict[symbol_alias_curr_zh] = symbol_alias_curr_zh

mydb = mysql.connector.connect(
    host=mypsw.wechatadmin.host, 
    user=mypsw.wechatadmin.user, 
    passwd=mypsw.wechatadmin.passwd, 
    database=mypsw.wechatadmin.database, 
    auth_plugin='mysql_native_password')

mycursor = mydb.cursor()

#插入或更新记录
insert_sql = "INSERT INTO symbol_alias ("  \
    "SYMBOL_ALIAS, SYMBOL, MARKET_TYPE" \
    ") VALUES (" \
    "%s, %s, %s)"

mycursor.executemany(insert_sql, insert_val)
mydb.commit()    # 数据表内容有更新，必须使用到该语句
print(mycursor.rowcount, "记录更新成功。")
