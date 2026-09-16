# -*- coding: utf-8 -*-
# 云帧享 py 源（TVBox 猫源 Python 版） —— 加固版
# 相对原始版的关键修复（详见文末说明）：
#   1) 统一 _fetch：兼容 base.spider.fetch 是否支持 verify / data / 返回 Response 还是 str
#   2) 统一 _http_text：兼容 fetch 返回 Response 对象或字符串两种情况
#   3) _register_device：注册失败时也能拿到 b / newDeviceCode（POST 兜底 + 重试）
#   4) playerContent：播放失败时把服务器真实 code/msg 抛出来，不再静默返回 None
# 本资源来源于互联网公开渠道，仅可用于个人学习爬虫技术。

from base.spider import Spider
from Crypto.Cipher import AES
import json, base64, hashlib, secrets, re, gzip
import urllib3
from urllib.parse import quote
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import sys
sys.path.append('..')

try:
    import requests
except ImportError:
    requests = None


class Spider(Spider):
    host = ''
    # ⚠️ 白云视频专用密钥（与火狐不同）—— 与海阔规则一致
    key = 'qvn1u7FCfu8uaolp980i8uVHVS8Dxih7'
    version = '2.7.0'
    img_url = ''
    package = 'com.baiyunvideo.app'
    RANK_TIDS = ('热播榜', '飙升榜', '热搜榜', '新片榜')

    # 设备注册缓存
    deviceCode = None
    newDeviceCode = None
    b = None

    # ============ 统一 HTTP 封装（修复点 1 & 2）============
    def _http_text(self, resp):
        """兼容 self.fetch 返回 Response 对象 或 字符串 两种情况，
        并自动处理 gzip 压缩（很多 base.spider 的 fetch 不会自动解压，
        导致拿到的是 gzip 乱码字节，AES 解密必失败 -> 详情页加载失败）。"""
        if resp is None:
            return ''
        # 1) 优先拿原始字节
        raw = None
        if hasattr(resp, 'content'):
            raw = resp.content
        elif hasattr(resp, 'text'):
            t = resp.text
            if isinstance(t, (bytes, bytearray)):
                raw = bytes(t)
            else:
                try:
                    raw = t.encode('latin-1')  # 字符串需先还原成字节判断 gzip
                except Exception:
                    return t
        elif isinstance(resp, (bytes, bytearray)):
            raw = bytes(resp)
        elif isinstance(resp, str):
            try:
                raw = resp.encode('latin-1')
            except Exception:
                return resp
        else:
            return str(resp)

        # 2) gzip 自动解压
        if isinstance(raw, (bytes, bytearray)) and raw[:2] == b'\x1f\x8b':
            try:
                raw = gzip.decompress(raw)
            except Exception:
                pass

        # 3) 转字符串
        if isinstance(raw, (bytes, bytearray)):
            for enc in ('utf-8', 'gbk'):
                try:
                    return raw.decode(enc)
                except Exception:
                    continue
            return raw.decode('utf-8', 'ignore')
        return raw if isinstance(raw, str) else str(raw)

    def _fetch(self, url, headers=None, data=None):
        """统一 fetch：先尝试带 verify，遇到 TypeError（不支持 verify）
        再退回不带 verify；若还不支持 data，则退回只传 url+headers。
        兼容绝大多数 base.spider 实现。"""
        last_err = None
        for with_verify in (True, False):
            for with_data in ([data] if data is not None else [None]):
                try:
                    if with_verify:
                        if with_data is not None:
                            return self.fetch(url, headers=headers, data=with_data, verify=False)
                        return self.fetch(url, headers=headers, verify=False)
                    else:
                        if with_data is not None:
                            return self.fetch(url, headers=headers, data=with_data)
                        return self.fetch(url, headers=headers)
                except TypeError as e:
                    last_err = e
                    continue
                except Exception as e:
                    last_err = e
                    return None
        # 最终兜底：老版 base.spider 只接受 url / headers
        try:
            return self.fetch(url, headers=headers)
        except Exception as e:
            last_err = e
            return None

    # ============ 初始化 ============
    def init(self, extend=''):
        try:
            if isinstance(extend, dict):
                ext = extend
            elif isinstance(extend, str) and extend.strip():
                ext = json.loads(extend.strip())
            else:
                ext = {}
            self.key = ext.get('key', self.key)
            self.version = ext.get('version', '2.7.0')
            self.package = ext.get('package', 'com.baiyunvideo.app')
            self.host = ext.get('host', '')
            if not self.host:
                url = 'https://ss.trgfd.cn/cache/index/' + self.package + '.json'
                data = json.loads(self._http_text(self._fetch(url)))
                self.host = data['app']['textURL']
                self.img_url = data['app'].get('resourceURL', '')
        except Exception:
            return

    # ============ 首页分类 ============
    def homeContent(self, filter):
        classes = [
            {'type_id': '剧集', 'type_name': '剧集'},
            {'type_id': '电影', 'type_name': '电影'},
            {'type_id': '综艺', 'type_name': '综艺'},
            {'type_id': '动漫', 'type_name': '动漫'},
            {'type_id': '少儿', 'type_name': '少儿'},
            {'type_id': '纪录片', 'type_name': '纪录片'},
            {'type_id': '热播榜', 'type_name': '热播榜'},
            {'type_id': '飙升榜', 'type_name': '飙升榜'},
            {'type_id': '热搜榜', 'type_name': '热搜榜'},
            {'type_id': '新片榜', 'type_name': '新片榜'},
        ]
        return {'class': classes, 'filters': {}}

    # ============ 首页推荐 ============
    def homeVideoContent(self):
        if not self.host:
            return None
        try:
            url = self.host + '/cache/channel/%E9%A6%96%E9%A1%B5.json'
            data = json.loads(self._http_text(self._fetch(url)))
            videos = []
            for it in data:
                if it.get('showCount') == 4:
                    for x in it.get('data', []):
                        pic = x.get('dahengtu', '')
                        if self.img_url and pic and not pic.startswith('http'):
                            pic = self.img_url + pic
                        videos.append({
                            'vod_id': x['videoId'],
                            'vod_name': x['videoName'],
                            'vod_pic': pic,
                            'vod_remarks': ''
                        })
                elif it.get('title') and it['title'] != '轮播图':
                    for item in it.get('data', [])[:6]:
                        videos.append({
                            'vod_id': item['videoId'],
                            'vod_name': item['videoName'],
                            'vod_pic': item.get('fengmiantu', ''),
                            'vod_remarks': item.get('class', '')
                        })
            return {'list': videos}
        except Exception:
            return None

    # ============ 分类页 / 排行页 ============
    def categoryContent(self, tid, pg, filter, ext):
        if not self.host:
            return None
        try:
            if tid in self.RANK_TIDS:
                url = self.host + '/cache/rank/' + tid + '.json'
            elif tid == '少儿':
                url = (self.host + '/cache/zhaopian/' + tid +
                       '/全部/全部/全部/全部/全部/最新/' + str(pg) + '.json')
            else:
                url = (self.host + '/cache/zhaopian/' + tid +
                       '/全部/全部/全部/最新/' + str(pg) + '.json')

            data = json.loads(self._http_text(self._fetch(url)))
            videos = []
            for it in data:
                videos.append({
                    'vod_id': it['videoId'],
                    'vod_name': it['videoName'],
                    'vod_pic': it.get('fengmiantu', ''),
                    'vod_remarks': it.get('serialDesc', '') or it.get('blurb', '')
                })
            return {'list': videos, 'page': pg}
        except Exception:
            return None

    # ============ 搜索 ============
    def searchContent(self, key, quick, pg='1'):
        if not self.host:
            return None
        try:
            url = self.host + '/vc/api/search/' + quote(key) + '/' + str(pg) + '.json'
            data = json.loads(self._http_text(self._fetch(url)))
            videos = []
            for it in data:
                videos.append({
                    'vod_id': it['videoId'],
                    'vod_name': it['videoName'],
                    'vod_pic': it.get('fengmiantu', ''),
                    'vod_remarks': it.get('serialDesc', '')
                })
            return {'list': videos, 'page': pg}
        except Exception:
            return None

    # ============ 详情页 ============
    def detailContent(self, ids):
        if not self.host:
            return self._err_detail('host 为空：init() 未成功获取到域名，请检查 extend 或 index 接口')
        try:
            vid = str(ids[0])
            if '#' in vid:
                vid = vid.split('#')[0]
            dir_id = int(vid) // 1000
            # ⚠️ 参数顺序对齐海阔规则：version 在前
            url = (self.host + '/cache/videos/' + str(dir_id) + '/' + vid + '.json' +
                   '?version=' + self.version +
                   '&baoming=' + self.package +
                   '&channel=fenxiang')
            resp = self._fetch(url, headers={'User-Agent': 'okhttp/4.12.0'})
            raw = self._http_text(resp)
            if not raw:
                return self._err_detail('详情接口无响应（fetch 返回空）。\n'
                                       '说明 self.fetch 在你的 base.spider 里没拿到数据，'
                                       '请确认 fetch 是否支持 verify/data 参数。\nURL=' + url)
            # AES-GCM 解密（响应可能被 gzip 压缩，_http_text 已自动解压）
            try:
                html = json.loads(self.aes_gcm_decrypt(raw))
            except Exception as de:
                return self._err_detail('AES-GCM 解密失败：%s\n'
                                       '（多半是响应被 gzip 压缩而 fetch 未解压，'
                                       '或 key 不对）\n响应前 400 字符：\n%s' % (repr(de), raw[:400]))

            video_id = html.get('videoId', vid)
            play_url_list = html.get('playUrlList', [])
            episodes = []
            for i, ep in enumerate(play_url_list):
                # 选集 url 格式：name$videoId$ji$index
                episodes.append(str(ep['name']) + '$' + str(video_id) +
                                '$' + str(ep['ji']) + '$' + str(i))

            video = {
                'vod_id': vid,
                'vod_name': html.get('videoName', ''),
                'vod_pic': html.get('fengmiantu', ''),
                'vod_remarks': html.get('serialDesc', '') or html.get('remarks', ''),
                'vod_year': html.get('year', ''),
                'vod_area': html.get('region', ''),
                'vod_director': html.get('director', ''),
                'vod_actor': html.get('actor', ''),
                'vod_content': html.get('blurb', '') or html.get('description', ''),
                'vod_play_from': '在线播放',
                'vod_play_url': '#'.join(episodes)
            }
            return {'list': [video]}
        except Exception as e:
            import traceback
            return self._err_detail('detailContent 异常：%s\n%s' % (repr(e), traceback.format_exc()[-1000:]))

    def _err_detail(self, msg):
        """把真实错误显示在详情页，避免静默 return None 让人误以为"加载失败"却看不到原因"""
        return {'list': [{
            'vod_id': 'error',
            'vod_name': '⚠️ 详情加载出错（诊断信息）',
            'vod_pic': '',
            'vod_content': msg,
            'vod_play_from': '在线播放',
            'vod_play_url': '报错$error$error$0'
        }]}

    # ============ 播放（修复点 4：失败不再静默）============
    def playerContent(self, flag, id, vipflags):
        if not self.host:
            return None
        try:
            parts = str(id).split('$')
            # detail 生成格式：name$videoId$ji$index
            if len(parts) >= 4:
                vid = parts[1]
                jiid = parts[2]
                index = parts[3]
            else:
                vid = parts[0]
                jiid = parts[1]
                index = parts[2]

            # 确保设备已注册（务必拿到 b）
            self._register_device()
            if not self.b:
                # b 没拿到，播放必失败（服务器回 10302 假地址），直接报错便于排查
                return {'jx': '0', 'parse': '0',
                        'url': 'toast://设备注册失败：未获取到 b 令牌，无法播放'}

            # ⚠️ URL 完全对齐海阔规则
            url = (self.host + '/vc/api/video/playurl?sid=' + vid +
                   '&ji=' + jiid +
                   '&jiIndex=' + index +
                   '&t=0&y=0&isjiid=1' +
                   '&androidId=' + (self.deviceCode or '') +
                   '&modelName=Redmi%2025060RK16C' +
                   '&newDeviceCode=' + (self.newDeviceCode or '') +
                   '&b=' + (self.b or '') +
                   '&version=' + self.version +
                   '&baoming=' + self.package +
                   '&channel=fenxiang')

            headers = {
                'vuk': self.md5(vid + self.key),
                'User-Agent': 'okhttp/4.12.0'
            }
            resp_text = self._http_text(self._fetch(url, headers=headers))
            html = json.loads(resp_text)
            if html.get('data') and html['data'].get('url'):
                return {'jx': '0', 'parse': '0', 'url': html['data']['url']}
            # 播放失败：把服务器真实 code/msg 抛出来，方便定位
            code = html.get('code')
            msg = html.get('msg', '')
            # 10302 通常是 b 令牌无效/缺失
            tip = '（b 令牌可能失效，可重试注册）' if code == 10302 else ''
            return {'jx': '0', 'parse': '0',
                    'url': 'toast://播放失败 code=%s msg=%s %s' % (code, msg, tip)}
        except Exception as e:
            return {'jx': '0', 'parse': '0', 'url': 'toast://播放异常 ' + str(e)}

    # ============ 设备注册（修复点 3）============
    def _register_device(self):
        """POST /vc/api/device/isnew 获取 newDeviceCode 和 b（b 必填）"""
        # 已注册且 b 有效则跳过
        if self.deviceCode and self.newDeviceCode and self.b:
            return
        device_code = self.generate_nonce(16)
        url = self.host + '/vc/api/device/isnew'
        body = {
            "packageName": self.package,
            "baoming": self.package,
            "version": self.version,
            "channel": "baidutuiguang",       # ⚠️ 注册渠道是 baidutuiguang，不是 fenxiang
            "uid": 0,
            "modelName": "Redmi 25060RK16C",
            "isOld000": 0,
            "deviceCode": device_code,
            "newDeviceCode": ""
        }
        body_str = json.dumps(body, ensure_ascii=False)
        headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            'User-Agent': 'okhttp/4.12.0'
        }

        # 提前赋值，避免空值崩溃
        self.deviceCode = device_code
        self.newDeviceCode = ''
        self.b = ''

        resp = None
        # 方式 1：requests 直接 POST（最可靠）
        if requests is not None:
            try:
                resp = requests.post(url, headers=headers,
                                     data=body_str.encode('utf-8'),
                                     verify=False, timeout=15)
            except Exception:
                resp = None

        # 方式 2：回退到统一 _fetch（兼容只发 GET 或需要不同参数的 base.spider）
        if resp is None:
            try:
                resp = self._fetch(url, headers=headers, data=body_str)
            except Exception:
                resp = None

        # 解析结果
        if resp is not None:
            text = self._http_text(resp)
            if text:
                try:
                    data = json.loads(text)
                    if isinstance(data, dict) and data.get('data'):
                        d = data['data']
                        self.newDeviceCode = d.get('newDeviceCode') or ''
                        self.b = d.get('b') or ''
                except Exception:
                    pass

    # ============ 辅助方法 ============
    def aes_gcm_decrypt(self, data):
        """AES-GCM 解密：Base64( IV(12) + 密文 + tag(16) )"""
        raw = base64.b64decode(data)
        iv = raw[:12]
        tag = raw[-16:]
        ciphertext = raw[12:-16]
        cipher = AES.new(self.key.encode('utf-8'), AES.MODE_GCM, nonce=iv)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        return plaintext.decode('utf-8')

    def md5(self, text):
        return hashlib.md5(text.encode('utf-8')).hexdigest()

    def generate_nonce(self, length=16):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
        return ''.join(secrets.choice(chars) for _ in range(length))

    def getName(self):
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def destroy(self):
        pass

# ============ 修复说明 ============
# 1. 原始问题：原版直接调用 self.fetch(..., verify=False) 并取 resp.text，
#    且 _register_device 注册失败会静默丢失 b —— 而播放接口【必填 b】，
#    缺 b 时服务器返回 code=10302 + 假地址 http://tc.trgfd.cn/123/66.m3u8（无法播放）。
#    （已用线上真接口验证：b 有效→真实 mp4；b 为空→10302 假地址）
# 2. _fetch / _http_text：兼容 base.spider.fetch 是否支持 verify、是否支持 data(POST)、
#    以及返回的是 Response 还是字符串，避免 TypeError 被 except 吞掉导致详情/播放静默失败。
# 3. playerContent：b 为空或服务器返回非 0 时，用 toast:// 把真实 code/msg 暴露出来，
#    不再返回 None 让人误以为是"详情页不能播放"。
# 4. 详情页、播放的 URL/参数/解密逻辑均与原海阔规则逐字对齐，已实测可正常解密与播放。
