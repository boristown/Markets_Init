import os
import glob
import re
import datetime
import time

mode = 1

markets = {
    1: "加密货币美元"
    }

patterns = {
    1: r'<tr>.+?title="([^><"]+)"><a\shref=".+?/crypto/([^><"]+).+?boundblank="">([^><"]+)</a></td>.+?title="([^><"]+)">.+?class="pid-(\d+)-last".+?</tr>'
    }

html_path = {
    1: "HTML\\*数字货币*.htm*"
    }

'''
#HTML 1: 加密货币美元
<tr>
        <td class="rank icon">1</td>
        <td class="flag"><i class="cryptoIcon c_bitcoin middle"></i></td>
        <td class="left bold elp name cryptoName first js-currency-name" title="Bitcoin"><a href="https://cn.investing.com/crypto/bitcoin" target="_blank" boundblank="">比特币</a></td>
        <td class="left noWrap elp symb js-currency-symbol" title="BTC">BTC</td>
        <td class="price js-currency-price"><a class="pid-1057391-last" href="https://cn.investing.com/crypto/currency-pairs?c1=189&amp;c2=12" target="_blank" boundblank="">10,859.6</a></td>
        <td class="js-market-cap" data-value="195042217484.97">$195.04B</td>
        <td class="js-24h-volume" data-value="16076563170.418">$16.08B</td>
        <td class="js-total-vol">32.03%</td>
        <td class="js-currency-change-24h greenFont pid-1057391-pcp">+5.42%</td>
        <td class="js-currency-change-7d redFont">-4.25%</td>
        </tr>
<tr>
<tr>
        <td class="rank icon">3</td>
        <td class="flag"><i class="cryptoIcon c_ripple middle"></i></td>
        <td class="left bold elp name cryptoName first js-currency-name" title="XRP"><a href="/crypto/ripple" target="_blank" boundblank="">瑞波币</a></td>
        <td class="left noWrap elp symb js-currency-symbol" title="XRP">XRP</td>
        <td class="price js-currency-price"><a class="pid-1057392-last" href="/crypto/currency-pairs?c1=197&amp;c2=12" target="_blank" boundblank="">0.27881</a></td>
        <td class="js-market-cap" data-value="12026861831.964">$12.03B</td>
        <td class="js-24h-volume" data-value="1207563829.5458">$1.21B</td>
        <td class="js-total-vol">2.41%</td>
        <td class="js-currency-change-24h redFont pid-1057392-pcp">-0.99%</td>
        <td class="js-currency-change-7d redFont">-6.50%</td>
</tr>
'''

dirs = glob.glob( html_path[mode] )

for file_path in dirs:
    print( file_path )
    file = open( file_path, "r", encoding="utf-8" )
    file_str = file.read()
    symbols_match = re.finditer(patterns[mode],file_str,re.S)
    for symbol_match in symbols_match:
        print(symbol_match.group(1))
        print(symbol_match.group(2))
        print(symbol_match.group(3))
        print(symbol_match.group(4))
        print(symbol_match.group(5))