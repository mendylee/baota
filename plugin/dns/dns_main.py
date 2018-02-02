#coding: utf-8
# +-------------------------------------------------------------------
# | 宝塔Linux面板 x3
# +-------------------------------------------------------------------
# | Copyright (c) 2015-2017 宝塔软件(http://bt.cn) All rights reserved.
# +-------------------------------------------------------------------
# | Author: 黄文良 <287962566@qq.com>
# +-------------------------------------------------------------------

#+--------------------------------------------------------------------
#|   DNS云解析
#+--------------------------------------------------------------------
import sys;
sys.path.append('class/');
reload(sys);
import public,json,os,time,binascii,urllib,re,web;
class dns_main:
    __PDATA = None;
    __APIURL = 'https://www.bt.cn/api/Dns';
    __UPATH = 'data/userInfo.json';
    __userInfo = None;
    def __init__(self):
        pdata = {}
        data = {}
        if os.path.exists(self.__UPATH):
            self.__userInfo = json.loads(public.readFile(self.__UPATH));
            if self.__userInfo:
                pdata['access_key'] = self.__userInfo['access_key'];
                data['secret_key'] = self.__userInfo['secret_key'];
        else:
            pdata['access_key'] = 'test';
            data['secret_key'] = '123456';
        pdata['data'] = data;
        self.__PDATA = pdata;
   
    #发送到服务器
    def send_server(self,action):
        if self.__PDATA['access_key'] == 'test': return public.returnMsg(False,'请先绑定宝塔用户!');
        self.__PDATA['data'] = self.De_Code(self.__PDATA['data']);
        result = public.httpPost(self.__APIURL + '/' + action,self.__PDATA);
        return json.loads(result);
   
    #获取域名列表
    def get_domains(self,get):
        if not hasattr(get,'p'): get.p = '1';
        query = ''
        if hasattr(get,'query'): query = '&query='+get.query;
        data =  self.send_server('GetDomainList?limit=10&tojs=Domains.DomainListRequest&p='+get.p+query);
        return data;
    
    #创建域名
    def create_domain(self,get):
        self.__PDATA['domain'] = get.domain;
        return self.send_server('CreateDomain');
    
    #删除域名
    def remove_domain(self,get):
        self.__PDATA['domain'] = get.domain;
        return self.send_server('RemoveDomain');
    
    #锁定域名
    def lock_domain(self,get):
        self.__PDATA['domain'] = get.domain;
        return self.send_server('LockDomain');
    
    #解锁域名
    def unlock_domain(self,get):
        self.__PDATA['domain'] = get.domain;
        return self.send_server('UnlockDomain');
    
    #暂停域名
    def pause_domain(self,get):
        self.__PDATA['domain'] = get.domain;
        return self.send_server('PauseDomain');
    
    #启用域名
    def start_domain(self,get):
        self.__PDATA['domain'] = get.domain;
        return self.send_server('StartDomain');
    
    #修改域名备注
    def set_domain_ps(self,get):
        self.__PDATA['domain'] = get.domain;
        self.__PDATA['ps'] = get.ps;
        return self.send_server('SetDomainPs');
    
    #获取域名默认NS信息
    def get_domain_ns(self,get):
        self.__PDATA['domain'] = get.domain;
        return self.send_server('GetDomainNs');
    
    #获取域名操作日志
    def get_domain_logs(self,get):
        self.__PDATA['domainId'] = get.domainId;
        if not hasattr(get,'p'): get.p = '1';
        data =  self.send_server('GetDomainLog?limit=10&tojs=Domains.LogsListRequest&p='+get.p);
        return data;
    
    #获取实时QPS
    def get_qps_hour(self,get):
        self.__PDATA['domainId'] = get.domainId;
        data = self.send_server('GetQpsHour');
        return sorted(data.items(),key=lambda item:item[0]);
    
    #获取天 QPS
    def get_qps_day(self,get):
        self.__PDATA['domainId'] = get.domainId;
        data = self.send_server('GetQpsDay');
        return sorted(data.items(),key=lambda item:item[0]);
    
    #获取月 QPS
    def get_qps_year(self,get):
        self.__PDATA['domainId'] = get.domainId;
        data = self.send_server('GetQpsYear');
        return sorted(data.items(),key=lambda item:item[0]);
    
    #获取记录列表
    def get_record_list(self,get):
        self.__PDATA['domainId'] = get.domainId;
        if not hasattr(get,'p'): get.p = '1';
        query = ''
        if hasattr(get,'query'): query = '&query='+get.query;
        data =  self.send_server('GetRecordList?limit=10&tojs=Domains.AnalysisListRequest&p='+get.p + query);
        return data;
    
    #添加解析记录
    def create_record(self,get):
        self.__PDATA['domainId'] = get.domainId;
        self.__PDATA['type'] = get.type;
        self.__PDATA['viewId'] = get.viewId;
        self.__PDATA['host'] = get.host;
        self.__PDATA['value'] = get.value;
        self.__PDATA['ttl'] = get.ttl;
        self.__PDATA['mx'] = get.mx;
        self.__PDATA['remark'] = get.remark;
        return self.send_server('AddRecord');
    
    #添加高级解析记录
    def create_senior_record(self,get):
        self.__PDATA['domainId'] = get.domainId;
        self.__PDATA['type'] = get.type;
        self.__PDATA['viewId'] = get.viewId;
        self.__PDATA['host'] = get.host;
        self.__PDATA['value'] = get.value;
        self.__PDATA['ttl'] = get.ttl;
        self.__PDATA['mx'] = get.mx;
        self.__PDATA['remark'] = get.remark;
        self.__PDATA['ispId'] = get.ispId;
        self.__PDATA['areaId'] = get.areaId;
        return self.send_server('AddSeniorRecord');
    
    
    #删除解析记录
    def remove_record(self,get):
        self.__PDATA['domainId'] = get.domainId;
        self.__PDATA['recordId'] = get.recordId;
        return self.send_server('RemoveRecord');
    
    #暂停记录
    def pause_record(self,get):
        self.__PDATA['domainId'] = get.domainId;
        self.__PDATA['recordId'] = get.recordId;
        return self.send_server('PauseRecord');
    
    #启用记录
    def start_record(self,get):
        self.__PDATA['domainId'] = get.domainId;
        self.__PDATA['recordId'] = get.recordId;
        return self.send_server('StartRecord');
    
    #编辑记录
    def modify_record(self,get):
        self.__PDATA['domainId'] = get.domainId;
        self.__PDATA['recordId'] = get.recordId;
        if hasattr(get,'type'): self.__PDATA['type'] = get.type;
        if hasattr(get,'viewId'): self.__PDATA['viewId'] = get.viewId;
        if hasattr(get,'host'): self.__PDATA['host'] = get.host;
        if hasattr(get,'value'): self.__PDATA['value'] = get.value;
        if hasattr(get,'ttl'): self.__PDATA['ttl'] = get.ttl;
        if hasattr(get,'mx'): self.__PDATA['mx'] = get.mx;
        if hasattr(get,'remark'): self.__PDATA['remark'] = get.remark;
        return self.send_server('ModifyRecord');
    
    #编辑高级记录
    def modify_senior_record(self,get):
        self.__PDATA['domainId'] = get.domainId;
        self.__PDATA['recordId'] = get.recordId;
        if hasattr(get,'type'): self.__PDATA['type'] = get.type;
        if hasattr(get,'viewId'): self.__PDATA['viewId'] = get.viewId;
        if hasattr(get,'host'): self.__PDATA['host'] = get.host;
        if hasattr(get,'value'): self.__PDATA['value'] = get.value;
        if hasattr(get,'ttl'): self.__PDATA['ttl'] = get.ttl;
        if hasattr(get,'mx'): self.__PDATA['mx'] = get.mx;
        if hasattr(get,'remark'): self.__PDATA['remark'] = get.remark;
        if hasattr(get,'ispId'): self.__PDATA['ispId'] = get.ispId;
        if hasattr(get,'areaId'): self.__PDATA['areaId'] = get.areaId;
        return self.send_server('SeniormodifyRecord');
    
    #获取whois信息
    def get_domain_ns(self,get):
        try:
            import whois
            data = whois.whois(get.domain)
            if not data: return public.returnMsg(False,'获取NS信息失败!');
            result = [];
            for d in data['name_servers']: result.append(d.lower());
            return result
        except:
            return ['ns1.dns.com','ns2.dns.com'];
    
    #获取服务套餐列表
    def get_server_list(self,get):
        return self.send_server('GetServerList');
    
    #获取默认区域线路ID列表
    def get_areaview_list(self,get):
        return self.send_server('AreaviewList');
        
    #获取默认ISP线路ID列表
    def get_ispview_list(self,get):
        return self.send_server('IspviewList');
    
    #通过IP获取线路
    def get_ip_dist(self,get):
        return self.send_server('IpDist');
    
    #服务套餐NS查询
    def get_service_list(self,get):
        return self.send_server('GetServiceList');
    
    #加密数据
    def De_Code(self,data):
        pdata = urllib.urlencode(data);
        return binascii.hexlify(pdata);
    
    #解密数据
    def En_Code(self,data):
        result = urllib.unquote(binascii.unhexlify(data));
        return json.loads(result);

    