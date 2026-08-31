# -*- coding: utf-8 -*-
# 本资源来源于互联网公开渠道，仅可用于个人学习爬虫技术。
# 严禁将其用于任何商业用途，下载后请于 24 小时内删除，搜索结果均来自源站，本人不承担任何责任。

from base.spider import Spider
from Crypto.Cipher import AES
from urllib.parse import quote, unquote, urljoin, urlparse
import re, sys, time, json, random, base64, hashlib, urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.path.append('..')

class Spider(Spider):
    headers,play_header,host,play_domain,encrypt_domain,proxyurl = {
        'User-Agent': "okhttp/4.9.0",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'log-header': "I am the log request header.",
        'app_id': "",
        'channel_code': "",
        'cur_time': "",
        'device_id': "",
        'mob_mfr': "huawei",
        'mobmodel': "DCO-AL00",
        'package_name': "",
        'sign': "",
        'sys_platform': "2",
        'sysrelease': "12",
        'token': "",
        'version': "40000"
    },{'User-Agent': 'Mozi'},'','','',''

    def init(self, extend=''):
        try:
           
            ext = json.loads(extend.strip())
            host = ext.get('host').rstrip('/')
            if not re.match(r'^https?://[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*(:\d+)?/?$', host): return None
            appid = ext.get('app_id').strip()
            deviceid = ext.get('deviceid').strip()
            version_code = ext.get('versionCode').strip()
            channel = ext.get('UMENG_CHANNEL').strip()
            package_name = ext.get('package_name').strip()
            self.encrypt_domain = ext.get('EncryptDomain').strip()
            if not(appid and deviceid and version_code and channel and package_name and self.encrypt_domain): return None
            if not self.is_valid_android_id(deviceid): return None
            self.headers['app_id'] = appid
            self.headers['channel_code'] = channel
            self.headers['device_id'] = deviceid
            self.headers['version'] = version_code
            self.headers['package_name'] = package_name
            try:
                self.proxyurl = f'{self.getProxyUrl(True)}&type=xiaocao'
            except Exception:
                self.proxyurl = 'http://127.0.0.1:9978/proxy?do=py&type=xiaocao'
            self.login(host)
        except Exception:
            return

    def homeContent(self, filter):
        if not self.host: return None
        result = {"class": [], "filters": {}}
        headers = self.headers.copy()
        headers['cur_time'] = self.timestamp()
        headers['sign'] = self.sign(headers['cur_time'])
        response = self.post(f'{self.host}/api/type/get_list', data='', headers=headers, verify=False).text
        data = json.loads(self.decrypt(response))
        #classes = [{'type_id': i['id'], 'type_name': i['name']} for i in data.get('result', [])]
        #if not any(i['type_id'] == 31 for i in classes):
        #    classes.append({'type_id': 31, 'type_name': '短剧'})
        for item in data['result']:  # 注意你的数据是 result 列表
            type_id = item['id']
            type_name = item['name']
        
           
            # 添加到 class
            result['class'].append({"type_id": type_id, "type_name": type_name})
            """
            # 构建筛选项（模仿参考代码）
            filter_items = []
            # 定义 name 映射（将 msg 中的 name 转为显示名称）
            name_mapping = {'type': '类型', 'area': '地区', 'year': '年份', 'sort': '排序'}
        
            for msg_item in item.get('msg', []):
                filter_name = msg_item['name']   # type, area, year, sort
                values = msg_item['data']        # 已经是列表
                if not values:
                    continue
                # 构造 value_list（参考代码中每个选项是 {"n": value, "v": value}）
                value_list = [{"n": v, "v": v} for v in values]
                # 显示名称
                display_name = name_mapping.get(filter_name, filter_name)
                # key 处理：sort 映射为 by（参考代码那样）
                key = 'class' if filter_name == 'type' else filter_name
                
                filter_items.append({"key": key, "name": display_name, "value": value_list})
        
            # 只有有筛选项才添加到 filters
            if filter_items:
                result["filters"][str(type_id)] = filter_items
            """
        return result
        #return {'class': classes}

    def homeVideoContent(self):
        if not self.host: return None
        headers = self.headers.copy()
        headers['cur_time'] = self.timestamp()
        headers['sign'] = self.sign(headers['cur_time'])
        try:
            response = self.post(f'{self.host}/api/channel/get_list', data='', headers=headers,verify=False).text
            data = self.decrypt(response)
            result = json.loads(data)['result']
            classes, videos, recommend_id = [], [], ''
            for i in result:
                if isinstance(i, dict):
                    if i.get('channel_name') == '推荐':
                        recommend_id = i.get('id')
                        break
            headers['cur_time'] = self.timestamp()
            headers['sign'] = self.sign(headers['cur_time'])
        except Exception:
            recommend_id = '324'
        payload2 = {
            'psize': "100",
            'channel_id': recommend_id,
            'pn': "1"
        }
        response2 = self.post(f'{self.host}/api/channel/get_info',data=payload2, headers=headers, verify=False).text
        data2 = self.decrypt(response2)
        result2 = json.loads(data2)['result']
        for item in result2:
            if not isinstance(item, dict):
                continue
            for block in item.get('block_list', []):
                if not isinstance(block, dict):
                    continue
                for vod in block.get('vod_list', []):
                    if vod['type_pid'] == 1:
                        remark = f"评分：{vod['vod_douban_score']}"
                    elif vod['type_pid'] != 2 and vod['type_pid'] != 4 and vod['type_pid'] != 31:
                        remark = vod['collection_new_title']
                        if vod['type_pid'] == 3:
                            remark = self.remove_invalid_episode(remark)
                    else:
                        remark = f"{vod['vod_serial']}集全" if vod.get('vod_isend') == 1 else f"更新至{vod['vod_serial']}集"
                    videos.append({
                        'vod_id': vod['id'],
                        'vod_name': vod['vod_name'],
                        'vod_pic': vod['vod_pic'],
                        'vod_remarks': remark,
                        'vod_year': vod['vod_year']
                    })
        return {'list': videos}

    def categoryContent(self, tid, pg, filter, extend):
        if not self.host: return None
        headers = self.headers.copy()
        headers['cur_time'] = self.timestamp()
        headers['sign'] = self.sign(headers['cur_time'])
        payload = {
            'area': "",
            'year': "",
            'type_id': tid,
            'sort': "",
            'type': "",
            'pn': pg
        }
        response = self.post(f'{self.host}/api/search/screen', data=payload, headers=headers, verify=False).text
        data = json.loads(self.decrypt(response))
        videos = []
        for i in data.get('result',[]):
            if i['type_pid'] == 1:
                remark = f"评分：{i['vod_douban_score']}"
            elif i['type_pid'] != 2 and i['type_pid'] != 4 and i['type_pid'] != 31:
                remark = i['collection_new_title']
                if i['type_pid'] == 3:
                    remark = self.remove_invalid_episode(remark)
            else:
                remark = f"{i['vod_serial']}集全" if i.get('vod_isend') == 1 else f"更新至{i['vod_serial']}集"
            videos.append({
                'vod_id': i['id'],
                'vod_name': i['vod_name'],
                'vod_pic': i['vod_pic'],
                'vod_remarks': remark,
                'vod_year': i['vod_year']
            })
        return {'list': videos, 'page': pg}

    def remove_invalid_episode(self, content):
        pattern = r'第(.*?)集'
        def replace_match(match):
            middle_content = match.group(1)
            return middle_content
        processed_content = re.sub(pattern, replace_match, content)
        return processed_content

    def searchContent(self, key, quick, pg='1'):
        if not self.host: return None
        headers = self.headers.copy()
        headers['cur_time'] = self.timestamp()
        headers['sign'] = self.sign(headers['cur_time'])
        payload = {'kw': key,'pn': pg}
        response = self.post(f'{self.host}/api/search/result', data=payload, headers=headers, verify=False).text
        data = json.loads(self.decrypt(response))
        videos = []
        for i in data.get('result',[]):
            if i['type_pid'] == 1:
                remark = f"评分：{i['vod_douban_score']}"
            elif i['type_pid'] != 2 and i['type_pid'] != 4 and i['type_pid'] != 31:
                remark = i['collection_new_title']
                if i['type_pid'] == 3:
                    remark = self.remove_invalid_episode(remark)
            else:
                vod_serial = i['vod_serial']
                remark = f"{i['vod_tag']},短剧" if i['type_pid'] == 31 else f"{vod_serial}集全" if i.get('vod_isend') == 1 else f"更新至{vod_serial}集"
            videos.append({
                'vod_id': i['id'],
                'vod_name': i['vod_name'],
                'vod_pic': i['vod_pic'],
                'vod_remarks': remark,
                'vod_year': i['vod_year']
            })
        return {'list': videos, 'page': pg}

    def detailContent(self, ids):
        if not self.host: return None
        headers = self.headers.copy()
        headers['cur_time'] = self.timestamp()
        headers['sign'] = self.sign(headers['cur_time'])
        payload = {
            'sig': '',
            'nc_token': '',
            'code': '',
            'phone': '',
            'vod_id': ids[0],
            'session_id': ''
        }
        response = self.post(f'{self.host}/api/video/result', data=payload, headers=headers, verify=False).text
        data = self.decrypt(response)
        # 部分影片/异常影片的 result 可能不含 vod_collection 或 result 本身为空, 全部兜底, 避免详情页整页崩溃
        result = (json.loads(data) or {}).get('result') or {}
        play_urls = []
        for i in (result.get('vod_collection') or []):
            if isinstance(i, dict):
                play_urls.append(f"{i.get('title','')}${i.get('vod_id','')}@{i.get('id','')}@{i.get('cur_time','')}@{i.get('vod_token','')}")
        video = {
            'vod_id': result.get('id', ids[0] if ids else ''),
            'vod_name': result.get('vod_name', ''),
            'vod_pic': result.get('vod_pic', ''),
            'vod_remarks': result.get('remarks', ''),
            'vod_year': result.get('vod_year', ''),
            'vod_area': result.get('vod_area', ''),
            'vod_actor': result.get('vod_actor', ''),
            'vod_director': result.get('vod_director', ''),
            'vod_content': result.get('vod_blurb', ''),
            'vod_play_from': '小草' if play_urls else '',
            'vod_play_url': '#'.join(play_urls),
            'type_name': result.get('vod_tag', '')
        }
        return {'list': [video]}

    def playerContent(self, flag, id, vipflags):
        vod_id, collection_id, cur_time, vod_token  = id.split('@', 3)
        headers = self.headers.copy()
        headers['cur_time'] = self.timestamp()
        headers['sign'] = self.sign(headers['cur_time'])
        payload = {
            'collection_id': collection_id,
            'sig': "",
            'nc_token': "",
            'code': "",
            'phone': "",
            'vod_id': vod_id,
            'session_id': "",
            'vod_token': vod_token,
            'cur_time': cur_time
        }
        response = self.post(f'{self.host}/api/video/collection', data=payload, headers=headers, verify=False).text
        data = self.decrypt(response)
        result = json.loads(data).get('result', {}) or {}
        ck_raw = result.get('ck')
        try:
            ck = base64.b64decode(ck_raw).decode('utf-8') if isinstance(ck_raw, str) else ''
        except Exception:
            ck = ck_raw if isinstance(ck_raw, str) else ''
        vod_url = result.get('vod_url', '')
        check_url = result.get('check_page_url')
        if not vod_url:
            return {'jx': '0', 'parse': '0', 'url': '', 'header': self.play_header}
        url = check_url or self.proxyurl + '&url=' + quote(f"{vod_url}?{ck}", safe='')
        return {'jx': '0', 'parse': '0', 'url': url, 'header': self.play_header}

    def localProxy(self, params):
        if params['type'] == "xiaocao":
            return self.xiaocao_m3u8_proxy(params)
        return None

    def login(self, host):
        if self.headers['token'] and self.host: return
        headers = self.headers.copy()
        headers['cur_time'] = self.timestamp()
        headers['sign'] = self.sign(headers['cur_time'])
        payload = {
            'invited_by': '',
            'ua': 'Mozilla/5.0 (Linux; Android 12; 23116PN5BC Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/101.0.4951.61 Safari/537.36',
            'is_install': '0'
        }
        response = self.post(f'{host}/api/public/init', data=payload, headers=headers, verify=False).text
        data = self.decrypt(response)
        result = json.loads(data)['result']
        self.headers['token'] = result['user_info']['token']
        self.host = result['sys_conf']['api_url'].rstrip('/')
        if not (self.headers['token'] or self.play_domain or self.play_domain):
            self.host = ''

    def sign(self, cur_time):
        return self.md5(f"zD9[bM4~sF4~uY2){self.headers['device_id']}{cur_time}").upper()

    def md5(self, str):
        md5_hash = hashlib.md5()
        md5_hash.update(str.encode('utf-8'))
        return md5_hash.hexdigest()

    def xiaocao_m3u8_proxy(self, params):
        url = unquote(params['url'])
        if params.get('format') == "ts":
            data = {"Location": url + self.hls_sign(url), "Content-Length": "0"}
            return [302, "text/html; charset=utf-8", None, data]
        else:
            data = self.xiaocao_modify_m3u8(url)
            return [200, "application/vnd.apple.mpegurl", data]

    def xiaocao_modify_m3u8(self, raw_url):
        ck = raw_url.split('?')[1]
        m3u8_url = raw_url + self.hls_sign(raw_url)
        m3u8_content = self.fetch(m3u8_url, headers=self.play_header, verify=False).text
        content = m3u8_content if m3u8_content is not None else self.m3u8_content
        if content is None: raise ValueError("M3U8为空")
        parsed = urlparse(raw_url)
        base = f"{parsed.scheme}://{parsed.netloc}{parsed.path.rsplit('/', 1)[0]}/"
        output_lines = []
        for line in content.splitlines():
            stripped_line = line.strip()
            if stripped_line and not stripped_line.startswith('#'):
                if not stripped_line.startswith(('http://', 'https://')):
                    full_url = urljoin(base, stripped_line)
                else:
                    full_url = stripped_line
                signed_url = self.proxyurl + f'&format=ts&url=' + quote(full_url + '&' + ck,safe='')
                output_lines.append(signed_url)
            else:
                output_lines.append(line)
        return '\n'.join(output_lines)

    def decrypt(self, base64_ciphertext):
        try:
            ciphertext = base64.b64decode(base64_ciphertext)
            cipher = AES.new('aZ9$kU5%qI7=yC2=zH2#gM0@pX7^wF3a'.encode('utf-8'), AES.MODE_CBC, 'hY2&tN3]kF7,dL7='.encode('utf-8'))
            plaintext_bytes = cipher.decrypt(ciphertext)
            padding_len = plaintext_bytes[-1]
            plaintext_bytes = plaintext_bytes[:-padding_len]
            return plaintext_bytes.decode('utf-8')
        except Exception as e:
            raise Exception(f"解密失败: {str(e)}")

    def get_url_path(self, url):
        parsed_url = urlparse(url)
        return parsed_url.path

    def hls_sign(self, url):
        hex_time = self.hex_time()
        if '?' in url: url = url.split('?')[0]
        data = self.encrypt_domain + self.get_url_path(url) + hex_time
        return f"&wsSecret={self.md5(data)}&wsTime={hex_time}"

    def is_valid_android_id(self, android_id):
        if not isinstance(android_id, str):
            return False
        pattern = r'^[0-9a-f]{16}$'
        return bool(re.fullmatch(pattern, android_id))

    def random_device_id(self):
        chars = '0123456789abcdef'
        android_id = ''.join(random.choice(chars) for _ in range(16))
        return android_id

    def timestamp(self):
        return str(int(time.time() * 1000))

    def hex_time(self):
        return hex(int(time.time()))[2:]

    def getName(self):
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def destroy(self):
        pass