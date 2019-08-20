import os
import glob
import re
import requests
import datetime
import time

mode = 1

markets = {
    1: "加密货币美元"
    }

patterns = {
    1: r'<tr>.+?title="([^><"]+)"><a\shref="/crypto/([^><"]+).+?boundblank="">([^><"]+)</a></td>.+?class="pid-(\d+)-last".+?</tr>'
    }

html_path={
    1: "HTML\\.*加密货币*.htm*"
    }
'''
#HTML 1: 加密货币美元
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
