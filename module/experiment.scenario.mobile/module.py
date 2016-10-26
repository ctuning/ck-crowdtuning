#
# Collective Knowledge (experiment scenarios to be executed on Android during crowdsourcing)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Grigori Fursin, Grigori.Fursin@cTuning.org, http://fursin.net
#

cfg={}  # Will be updated by CK (meta description of this module)
work={} # Will be updated by CK (temporal data)
ck=None # Will be updated by CK (initialized CK kernel) 

# Local settings

##############################################################################
# Initialize module

def init(i):
    """

    Input:  {}

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """
    return {'return':0}

##############################################################################
# get scenarios depending on user's mobile device features

def get(i):
    """
    Input:  {
              (data_uoa)
              (repo_uoa)

              (platform_features)
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              scenarios    - list of scenarios and related files
            }

    """

    pf=i.get('platform_features',{})

    abi=pf.get('cpu',{}).get('cpu_abi','')

    os_name=pf.get('os',{}).get('name','')
    os_ver=[]
    j=os_name.find(' ')
    if j>0:
        os_ver=os_name[j+1:].strip().split('.')

    duoa=i.get('data_uoa','')
    ruoa=i.get('repo_uoa','')

    r=ck.access({'action':'search',
                 'module_uoa':work['self_module_uid'],
                 'data_uoa':duoa,
                 'repo_uoa':ruoa,
                 'add_meta':'yes'})
    if r['return']>0: return r

    lst=r['lst']

    nlst=[]

    # Prepare URL from CK server
    rx=ck.access({'action':'form_url_prefix',
                  'module_uoa':'wfe',
                  'host':i.get('host',''), 
                  'port':i.get('port',''), 
                  'template':i.get('template','')})
    if rx['return']>0: return rx
    url0=rx['url']

    for q in lst:
        add=True

        meta=q['meta']

        sabi=meta.get('supported_abi',[])
        if abi!='' and abi not in sabi:
            add=False

        if add:
            min_os_ver=meta.get('min_os_ver',[])
            # TBD: need to check all digits
            if len(min_os_ver)>0 and len(os_ver)>0 and os_ver[0]<min_os_ver[0]:
                add=False

        if add:
            ff=meta.get('files',[])

            # Go through files and update
            nff=[]
            for f in ff:
                sabi=f.get('limit_abi',[])
                if len(sabi)==0 or abi=='' or abi in sabi:
                    url=f.get('url','')
                    if url=='':
                        path=f.get('path','')
                        fn=f.get('filename','')
                        url=url0+'action=pull&common_action=yes&cid='+q['module_uoa']+':'+q['data_uid']+'&filename='+path+'/'+fn

                    f['url']=url
                    nff.append(f)

            meta['files']=nff

            nlst.append(q)

#    ck.save_json_to_file({'json_file':'/tmp/xyz888.json','dict':nlst})

    return {'return':0, 'scenarios':nlst}
