#
# Collective Knowledge (program optimization)
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
line='****************************************************************'

welcome   = "Dear friends!\n\n" \
            "Computer systems become very inefficient" \
            " due to too many design and optimization choices available - " \
            " optimizing compilers are simply not keeping pace with all this complexity and rapidly evolving hardware and software." \
            " It is possible to speed up code from 15% to more than 10x while considerably reducing energy usage and code size" \
            " for many popular algorithms (DNN, vision processing, BLAS) using multi-objective autotuning." \
            " Unfortunately, it can be untolerably slow.\n\n" \
            "Therefore, we have developed this CK-based experimental workflow to crowdsource program and compiler autotuning"  \
            " across multiple hardware and environments kindly provided by volunteers.\n\n" \
            "NOTE: this program will send some anonymized info about your hardware and OS features" \
            " to the public Collective Knowledge Server to select unexplored optimization points" \
            " or validate previously found optimizations!\n\n" \
            "You can find more info about optimization crowdsourcing including results here:\n" \
            " * http://cTuning.org/crowdsource-optimization\n\n" \
            "We would like to sincerely thank you for participating in this community effort" \
            " and help us optimize computer systems to accelerate knowledge discovery and boost innovation " \
            " in science and technology while making our planet greener!\n\n" \
            "Finally, performance of some systems may be chaotic (due to internal adaptation such as in Intel Core processors)!\n" \
            "  For now, we skip such results and we will later add plugins for statistical comparison of empirical results from our past R&D\n"

form_name='ck_cresults_form'
onchange='document.'+form_name+'.submit();'

wscenario='scenario'
wprune='pruning'

fstats='stats.json'

iuoa='index'

key_prune='__web_prune__'

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
# test remote access

def log(i):
    """
    Input:  {
              file_name     - file name
              text          - text
              (skip_header) - if 'yes', do not add header
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              (path)       - path to log file
            }

    """

    import os

    fn=i['file_name']
    txt=i.get('text','')
    sh=i.get('skip_header','')

    r=ck.get_current_date_time({})
    if r['return']>0: return r

    s=''
    if sh!='yes': s+='********************************\n'+r['iso_datetime']+' ; '
    s+=txt

    # Prepare logging
    r=get_path({})
    if r['return']>0: return r

    px=r['path']

    path=os.path.join(px, fn)

    try:
       with open(path, "a") as f:
          f.write(s+'\n')
       f.close()
    except Exception as e: 
       return {'return':1, 'error':'problem logging ('+format(e)+')'}

    return {'return':0, 'path':path}

##############################################################################
# test remote access

def test(i):
    """
    Input:  {
              (email)      - optional email
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              status       - string with status
            }

    """

    import os

    o=i.get('out','')

    status="CK server works fine!";

    email=i.get('email','')

    r=log({'file_name':cfg['log_file_test'], 'text':email})
    if r['return']>0: return r

    if o=='con':
       ck.out(status)

    return {'return':0, 'status':status}

##############################################################################
# get path to internal/local/tmp crowdsourcing files

def get_path(i):
    """
    Input:  {
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import os

    rps=os.environ.get(cfg['env_key_crowdsource_path'],'').strip()
    if rps=='': 
       # Get home user directory
       from os.path import expanduser
       home = expanduser("~")

       # In the original version, if path to repos was not defined, I was using CK path,
       # however, when installed as root, it will fail
       # rps=os.path.join(work['env_root'],cfg['subdir_default_repos'])
       # hence I changed to <user home dir>/CK
       rps=os.path.join(home, cfg['crowdsource_path'])

    if not os.path.isdir(rps):
       os.makedirs(rps)

    return {'return':0, 'path':rps}

##############################################################################
# explore program optimizations

def explore(i):
    """
    Input:  {
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    ck.out('')
    ck.out('Command line: ')
    ck.out('')

    import json
    cmd=json.dumps(i, indent=2)

    ck.out(cmd)

    return {'return':0}

##############################################################################
# generate experiment pack for crowdsourcing in remote hardware (mobile phones or tablets)

def generate_for_remote(i):
    """
    Input:  {
              (email)             - email or person UOA
              (features)          - remote device features
              (features_uoa_list) - remote device features UOA list:
                                       * platform_uoa
                                       * platform_os_uoa
                                       * platform_cpu_uoa
                                       * platform_accelerator_uoa
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import os

    email=i.get('email','')
    ft=i.get('features','')
    if ft=='': ft={}

    # Logging
    r=ck.dumps_json({'dict':ft, 'skip_indent':'yes', 'sort_keys':'yes'})
    if r['return']>0: return r
    x=r['string']

    r=log({'file_name':cfg['log_file_generate'], 'text':email+'\n'+x+'\n'})
    if r['return']>0: return r

    # Prepare dummy pack
    desc='*** GCC compiler flag crowdtuning test for ARM ***'
    rcm='data.pgm tmp-output.pgm -c'
    calibrate='yes'
    bf0='a0.out'
    bf1='a1.out'

    p=os.path.join(work['path'],'ck-crowdsource-experiment-pack.zip')

    if not os.path.isfile(p):
       return {'return':1, 'error':'experiment pack file not found'}

    size=os.path.getsize(p) 

    r=ck.convert_file_to_upload_string({'filename':p})
    if r['return']>0: return r

    fx=r['file_content_base64']

    #MD5
    import hashlib
    md5=hashlib.md5(fx.encode()).hexdigest()

    return {'return':0, 'file_content_base64':fx, 
                        'size':size, 
                        'md5sum':md5,
                        'desc':desc,
                        'run_cmd_main':rcm,
                        'bin_file0':bf0,
                        'bin_file1':bf1,
                        'calibrate':calibrate,
                        'calibrate_max_iters':10,
                        'calibrate_time':10.0,
                        'repeat':5,
                        'ct_repeat':1
           }

##############################################################################
# submit results from remote device (for example, mobile phone)

def submit_from_remote(i):
    """
    Input:  {
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """


    import os

    email=i.get('email','')
    ft=i.get('features','')
    if ft=='': ft={}
    results=i.get('results','')
    if results=='': results={}

    # Logging
    r=ck.dumps_json({'dict':results, 'skip_indent':'yes', 'sort_keys':'yes'})
    if r['return']>0: return r
    x=r['string']

    r=ck.dumps_json({'dict':ft, 'skip_indent':'yes', 'sort_keys':'yes'})
    if r['return']>0: return r
    y=r['string']

    r=log({'file_name':cfg['log_file_results'], 'text':email+'\n'+x+'\n'+y+'\n'})
    if r['return']>0: return r

    status='Successfully recorded!'

    return {'return':0, 'status':status}

##############################################################################
# crowdsource program optimization

def crowdsource(i):
    """
    Input:  {
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    tags='crowdsource,experiments,program optimization'
    if i.get('local_autotuning','')=='yes': 
       tags='program optimization,autotuning'

    i['tags']=tags
    i['module_uoa']=cfg['module_deps']['experiment']

    return ck.access(i)

##############################################################################
# viewing entries as html

def show(i):
    """
    Input:  {
              scenario
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              html         - generated HTML
            }

    """

    import os

    h='<center>\n'
    h+='<h2>Aggregated results of crowdsourced experiments</h2>\n'

    # Check host URL prefix and default module/action
    url0=ck.cfg.get('wfe_url_prefix','')

    # However, if using CK server - automatically substitute server_host and port!
    if i.get('server_host','')!='':
       url0='http://'+i['server_host']
       if i.get('server_port','')!='':
          url0+=':'+str(i['server_port'])
       url0+='?'

    url00=url0
    if ck.cfg.get('wfe_url_prefix_subst','')!='': url00=ck.cfg['wfe_url_prefix_subst']

    url=url0
    action=i.get('action','')
    muoa=i.get('module_uoa','')

    hstyle=''

    url+='action=index&module_uoa=wfe&native_action='+action+'&'+'native_module_uoa='+muoa
    url1=url

    # Prepare query div ***************************************************************
    # Start form + URL (even when viewing entry)
    r=ck.access({'action':'start_form',
                 'module_uoa':cfg['module_deps']['wfe'],
                 'url':url1,
                 'name':form_name})
    if r['return']>0: return r
    h+=r['html']

    # Listing available crowdsourcing scenarios ...
    scenario=i.get('scenario','')

    ii={'action':'search',
        'module_uoa':cfg['module_deps']['module'],
        'add_meta':'yes',
        'add_info':'yes',
        'tags':'crowdsource,experiments,program optimization'}
    r=ck.access(ii)
    if r['return']>0: return r

    xls=r['lst']

    if len(xls)==0:
       h+='<b>Can\'t find any local expeimrent crowdsourcing scenarios ...</b>'
    else:
       ls=sorted(xls, key=lambda v: (int(v.get('meta',{}).get('priority',0)), v['data_uoa']))

       ii={'action':'convert_ck_list_to_select_data',
           'module_uoa':cfg['module_deps']['wfe'],
           'lst':ls, 
           'add_empty':'yes',
           'sort':'no',
           'value_uoa':scenario,
           'ignore_remote':'yes'}
       r=ck.access(ii)
       if r['return']>0: return r
       dls=r['data']
       if r.get('value_uid','')!='': scenario=r['value_uid']

       if scenario=='': scenario=ls[0]['data_uid']

       ii={'action':'create_selector',
           'module_uoa':cfg['module_deps']['wfe'],
           'data':dls,
           'name':wscenario,
           'onchange':onchange, 
           'skip_sort':'yes',
#           'style':'width:400px;',
           'selected_value':scenario}
       r=ck.access(ii)
       if r['return']>0: return r
       h+='Select crowdsourcing scenario: '+r['html']

       h+='</center>\n'

       h+='<p>\n'

       # Check scenario
       if scenario!='':
          # Load scenario
          ii={'action':'load',
              'module_uoa':cfg['module_deps']['module'],
              'data_uoa':scenario}
          r=ck.access(ii)
          if r['return']>0: return r
          ds=r['dict']

          pr=ds.get('prune_results',[])
          ipr=len(pr)
          if ipr>0:
             # Try to find index
             ii={'action':'load',
                 'module_uoa':scenario,
                 'data_uoa':iuoa}
             rx=ck.access(ii)
             if rx['return']==0:
                p=rx['path']

                mprune={}

                px=os.path.join(p, fstats)
                if os.path.isfile(px):
                   rx=ck.load_json_file({'json_file':px})
                   if rx['return']>0: return rx
                   dd=rx['dict']

                   mm=dd.get('meta',{})

                   h+='<center>\n'
                   h+='<div id="ck_box_with_shadow">\n'
                   h+='<center><small><b>Prune solutions:</b></small></center>\n'

                   h+='<table border="0" cellpadding="5" cellspacing="0">\n'
                   for q in pr:
                       qd=q.get('desc','')
                       qi=q.get('id','')

                       l=mm.get(qi,{})

                       kk=key_prune+qi
                       vv=i.get(kk,'')

                       if vv!='':
                          mprune[qi]=vv

                       dt=[{'name':'', 'value':''}]
                       for k in sorted(l):
                           dt.append({'name':k, 'value':k}) 

                       ii={'action':'create_selector',
                           'module_uoa':cfg['module_deps']['wfe'],
                           'data':dt,
                           'name':kk,
                           'onchange':onchange, 
                           'skip_sort':'yes',
                           'selected_value':vv}
                       r=ck.access(ii)
                       if r['return']>0: return r

                       h+=' <tr><td>'+qd+':</td><td>'+r['html']+'</td></tr>\n'

                   h+='</table>\n'
                   h+='</div>\n'
                   h+='<p>\n'
                   h+='</center>\n'

                # Prune
                ii={'action':'search',
                    'common_func':'yes',
                    'module_uoa': scenario,
                    'search_dict':{'meta':mprune},
                    'add_meta':'yes'
                   }
                r=ck.access(ii)
                if r['return']>0: return r
                rl=r['lst']

                if ipr==1:
                   rl=sorted(rl, key=lambda a: a.get('meta',{}).get('meta',{}).get(pr[0]['id'],''))
                elif ipr==2:
                   rl=sorted(rl, key=lambda a: (a.get('meta',{}).get('meta',{}).get(pr[0]['id'],''), \
                                                a.get('meta',{}).get('meta',{}).get(pr[1]['id'],'')))
                elif ipr>2:
                   rl=sorted(rl, key=lambda a: (a.get('meta',{}).get('meta',{}).get(pr[0]['id'],''), \
                                                a.get('meta',{}).get('meta',{}).get(pr[1]['id'],''), \
                                                a.get('meta',{}).get('meta',{}).get(pr[2]['id'],'')))

                irl=len(rl)
                if irl==0:
                   h+='<b>No solutions found!</b>'
                else:
#                   h+=str(len(rl))+' entries found!</b>'

                   if irl>100: 
                      h+=str(irl)+' entries found - showing first 100!</b>'
                      irl=100

                  # Check host URL prefix and default module/action
                   url0=ck.cfg.get('wfe_url_prefix','')
   
                   h+='<center>\n'
                   h+='<table class="ck_table" border="0">\n'

                   h+=' <tr style="background-color:#cfcfff;">\n'
                   h+='  <td><b>\n'
                   h+='   #\n'
                   h+='  </b></td>\n'
                   h+='  <td><b>\n'
                   h+='   <a href="'+url0+'wcid='+scenario+':">Solutions UID</a>\n'
                   h+='  </b></td>\n'
                   for k in pr:
                       qd=k.get('desc','')
                       qi=k.get('id','')

                       h+='  <td><b>\n'
                       h+='   '+qd+'\n'
                       h+='  </b></td>\n'
                   h+=' </tr>\n'

                   iq=0
                   for q in range(0, irl):
                       iq+=1

                       qq=rl[q]

                       duid=qq['data_uid']

                       dm=qq['meta'].get('meta',{})

                       h+='<tr>'
                       h+=' <td>'+str(iq)+'</td>'
                       h+=' <td><a href="'+url0+'wcid='+scenario+':'+duid+'">'+duid+'</a>\n'

                       for k in pr:
                           qd=k.get('desc','')
                           qi=k.get('id','')

                           h+='  <td>'
                           h+='   '+dm.get(qi,'')
                           h+='  </td>'
                       
                       h+='</tr>'

                   h+='</table>\n'
                   h+='</center>\n'

    h+='<p><center><a href="https://github.com/ctuning/ck/wiki/Advanced_usage_crowdsourcing">Related links</a></center>'

    return {'return':0, 'html':h}

##############################################################################
# add new solution

def add_solution(i):
    """
    Input:  {
              packed_solution     - new packed points
              scenario_module_uoa - scenario UID
              meta                - meta to search

              exchange_repo
              exchange_subrepo




              data_uoa
              (repo_uoa)
              (iterations)

              speedup
              pchoices1
              cmd1
              pchoices2
              cmd2
              choices
              platform_features
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import os

    o=i.get('out','')
    oo=''
    if o=='con': oo='con'

    ps=i.get('packed_solution','')
    ruoa=i.get('repo_uoa','')
    smuoa=i['scenario_module_uoa']
    meta=i['meta']

    er=i.get('exchange_repo','')
    esr=i.get('exchange_subrepo','')

    # Search if exists
    if o=='con': 
       ck.out('')
       ck.out('  Searching scenario solutions ...')

    ii={'action':'search',
        'common_func':'yes',
        'repo_uoa': ruoa,
        'module_uoa': smuoa,
        'search_dict':{'meta':meta},
        'add_meta':'yes'
       }
    r=ck.access(ii)
    if r['return']>0: return r
    rl=r['lst']
    et=r.get('elapsed_time','')
    if et!='' and o=='con':
       ck.out('      Elapsed time (s) :'+str(et))

    if len(rl)==0:
       ii['action']='add'
       ii['dict']={'meta':meta}
       r=ck.access(ii)
       if r['return']>0: return r
       duoa=r['data_uid']
    else:
       duoa=rl[0]['data_uid']

    if o=='con': 
       ck.out('  Loading and locking entry ('+duoa+') ...')

    # Loading existing info and locking
    ii['action']='load'
    ii['get_lock']='yes'
    ii['lock_expire_time']=120
    ii['data_uoa']=duoa
    r=ck.access(ii)
    if r['return']>0: return r
    duid=r['data_uid']

    p=r['path']
    lock_uid=r['lock_uid']

    d=r['dict']
    
    # Adding solution
    r=ck.gen_uid({})
    if r['return']>0: return r
    suid=r['data_uid'] # solution UID

    p1=os.path.join(p, suid)
    if not os.path.isdir(p1):
       os.makedirs(p1)

    # Prepare tmp file
    rx=ck.convert_upload_string_to_file({'file_content_base64':ps,
                                         'filename':''})
    if rx['return']>0: return rx
    fn=rx['filename']

    # Unzip
    rx=ck.unzip_file({'archive_file':fn,
                      'path':p1,
                      'overwrite':'yes',
                      'delete_after_unzip':'yes'})
    if rx['return']>0: return rx












    # Updating and unlocking entry *****************************************************
    if o=='con': 
       ck.out('  Updating entry and unlocking ...')

    ii={'action':'update',
        'common_func':'yes',
        'repo_uoa': ruoa,
        'module_uoa': smuoa,
        'data_uoa':duid,
        'ignore_update':'yes',
        'sort_keys':'yes',
        'dict':d,
        'substitute':'yes',
        'unlock_uid':lock_uid
       }
    r=ck.access(ii)
    if r['return']>0: return r

    # *************************************************************** Adding some stats
    # Search if exists
    if o=='con': 
       ck.out('')
       ck.out('  Reloading index entry for statistics and locking ...')

    ii={'action':'load',
        'common_func':'yes',
        'repo_uoa': ruoa,
        'module_uoa': smuoa,
        'data_uoa':iuoa,
        'get_lock':'yes',
        'create_if_not_found':'yes',
        'lock_expire_time':120
       }
    r=ck.access(ii)

    p=r['path']
    d=r['dict']
    lock_uid=r['lock_uid']

    # Try to load keys.json
    dd={}
    px=os.path.join(p, fstats)
    if os.path.isfile(px):
       rx=ck.load_json_file({'json_file':px})
       if rx['return']>0: return rx
       dd=rx['dict']

    mm=dd.get('meta',None)
    if mm==None:
       mm={}

    for q in meta:
        qq=meta[q]

        v=mm.get(q, None)
        if v==None:
           v={}

        v1=v.get(qq, None)
        if v1==None:
           v1={}

        vv=v1.get('touched',None)
        if vv==None: 
           vv=0
        vv=int(vv)
        vv+=1

        v1['touched']=vv

        v[qq]=v1

        mm[q]=v

    dd['meta']=mm

    # Saving stats
    rx=ck.save_json_to_file({'json_file':px, 'dict':dd})
    if rx['return']>0: return rx

    # Updating and unlocking entry *****************************************************
    if o=='con': 
       ck.out('  Updating entry and unlocking ...')

    ii={'action':'update',
        'common_func':'yes',
        'repo_uoa': ruoa,
        'module_uoa': smuoa,
        'data_uoa':iuoa,
        'ignore_update':'yes',
        'dict':d,
        'substitute':'yes',
        'unlock_uid':lock_uid
       }
    r=ck.access(ii)
    if r['return']>0: return r



    return {'return':0}

##############################################################################
# initialize experiment

def initialize(i):
    """
    Input:  {
              (host_os)                    - host OS (detect, if omitted)
              (target_os)                  - OS module to check (if omitted, analyze host)
              (device_id)                  - device id if remote (such as adb)

              (quiet)                      - do not ask questions, but select random ...
              (skip_welcome)               - if 'yes', do not print welcome header
              
              (skip_exchange)              - if 'yes', do not exchange platform info
                                            (development mode)

              (change_user)                - if yes', change user

              (local)                      - if 'yes', use local repo for exchange (local autotuning/benchmarking)
              (exchange_repo)              - which repo to record/update info (remote-ck by default)
              (exchange_subrepo)           - if remote, remote repo UOA

              (force_platform_name)        - if !='', use this for platform name
            }

    Output: {
              return           - return code =  0, if successful
                                             >  0, if error
              (error)          - error text if return > 0

              platform_info    - output of ck detect platform
            }

    """

    import copy
    import os

    # Setting output
    o=i.get('out','')
    oo=''
    if o=='con': oo='con'

    user=''

    # Params
    hos=i.get('host_os','')
    tos=i.get('target_os', '')
    tdid=i.get('device_id', '')

    exc='yes'
    se=i.get('skip_exchange','')
    if se=='yes': exc='no'

    cu=i.get('change_user','')

    er=i.get('exchange_repo','')
    esr=i.get('exchange_subrepo','')

    fpn=i.get('force_platform_name','')

    quiet=i.get('quiet','')

    sw=i.get('skip_welcome','')

    #**************************************************************************************************************
    # Welcome info
    if o=='con' and quiet!='yes' and sw!='yes':
       ck.out(line)
       ck.out(welcome)

       if quiet!='yes':
          r=ck.inp({'text':'Press Enter to continue'})

    # Prepare log
    r=log({'file_name':cfg['log_file_own'], 'text':''})
    if r['return']>0: return r
    p=r['path']

    if o=='con':
       ck.out(line)
       ck.out('Experimental results will be appeneded to a local log file: '+p)

       if quiet!='yes':
          ck.out('')
          r=ck.inp({'text':'Press Enter to continue'})

    #**************************************************************************************************************
    # Check if there is program crowdtuning configuration
    dcfg={}
    ii={'action':'load',
        'module_uoa':cfg['module_deps']['cfg'],
        'data_uoa':cfg['cfg_uoa']}
    r=ck.access(ii)
    if r['return']>0 and r['return']!=16: return r
    if r['return']!=16:
       dcfg=r['dict']

    user=dcfg.get('user_email','')

    if (user=='' and o=='con' and quiet!='yes') or cu!='':
       if cu=='':
          ck.out(line)
          r=ck.inp({'text':'If you would like to identify your contributions as well as participate in monthly prize draws, please enter your email: '})
          xuser=r['string'].strip()
       else:
          xuser=cu.strip()

       if xuser!=user:
          user=xuser
          dcfg['user_email']=user

          ii={'action':'update',
              'module_uoa':cfg['module_deps']['cfg'],
              'data_uoa':cfg['cfg_uoa'],
              'dict':dcfg}
          r=ck.access(ii)
          if r['return']>0: return r

    if user!='' and o=='con' and quiet!='yes':
       ck.out(line)
       ck.out('Your crowsourcing ID : '+user)

    #**************************************************************************************************************
    # Testing remote platform
    if se!='yes':
       ck.out(line)
       ck.out('Testing experiment crowdsourcing server ...')
       ck.out('')

       ii={'action':'test',
           'module_uoa':work['self_module_uid'],
           'out':'',
           'email':user,
           'repo_uoa':er}
       r=ck.access(ii)
       if r['return']>0: return r

       ck.out('  SUCCESS!')

    #**************************************************************************************************************
    # Detecting platforms and exchanging info with public Server
    if o=='con':
       ck.out(line)
       ck.out('Detecting your platform info and query public CK server and get latest optimization points ...')
       ck.out('')

    ii={'action':'detect',
        'module_uoa':cfg['module_deps']['platform'],
        'out':oo,
        'host_os':hos,
        'target_os':tos,
        'target_device_id':tdid,
        'exchange':exc,
        'exchange_repo':er,
        'exchange_subrepo':esr,
        'force_platform_name':fpn}
    rpp=ck.access(ii)
    if rpp['return']>0: return rpp

    hos=rpp['host_os_uoa']
    hosd=rpp['host_os_dict']

    tos=rpp['os_uoa']
    tosd=rpp['os_dict']
    tbits=tosd.get('bits','')

    hosz=hosd.get('base_uoa','')
    if hosz=='': hosz=hos
    tosz=tosd.get('base_uoa','')
    if tosz=='': tosz=tos

    remote=tosd.get('remote','')

    tdid=rpp['device_id']

    if hos=='':
       return {'return':1, 'error':'"host_os" is not defined or detected'}

    if tos=='':
       return {'return':1, 'error':'"target_os" is not defined or detected'}

    return {'return':0, 'platform_info':rpp}

##############################################################################
# perform program optimization

def run(i):
    """
    Input:  {
              (host_os)                    - host OS (detect, if omitted)
              (target_os)                  - OS module to check (if omitted, analyze host)
              (device_id)                  - device id if remote (such as adb)

              (quiet)                      - do not ask questions, but select random ...
              (skip_welcome)               - if 'yes', do not print welcome header
              
              (skip_exchange)              - if 'yes', do not exchange platform info
                                            (development mode)

              (change_user)                - if yes', change user

              (local)                      - if 'yes', use local repo for exchange (local autotuning/benchmarking)
              (exchange_repo)              - which repo to record/update info (remote-ck by default)
              (exchange_subrepo)           - if remote, remote repo UOA

              (local_autotuning)           - if 'yes', do not crowdtune, i.e. find local experiment and do not exchnage results

              (force_platform_name)        - if !='', use this for platform name

              (scenario)                   - module UOA of crowdsourcing scenario
              (scenario_cfg)               - cfg of a scenario

              (seed)                       - autotuning seed

              (program_tags)               - force selection of programs by tags

              (program_uoa)                - force program UOA
              (cmd_key)                    - CMD key
              (dataset_uoa)                - dataset UOA
              (dataset_file)               - dataset filename (if more than one inside one entry - suggest to have a UID in name)

              (iterations)                 - limit number of iterations, otherwise infinite (default=30)
                                             if -1, infinite (or until all choices are explored)

              (calibration_time)           - change calibration time (deafult 10 sec.)

              (repetitions)                - statistical repetitions of a given experiment

              (objective)                  - extension to flat characteristics (min,exp,mean,center) to tune on Pareto
                                             (default: min - to see what we can squeeze from a given architecture)

              (keep_tmp)                   - if 'yes', do not remove run batch

              (only_one_run)               - if 'yes', run scenario ones (useful for autotuning a given program)

              (ask_pipeline_choices)       - if 'yes', ask for each pipeline choice, otherwise random selection 

              (platform_info)              - detected platform info

              (experiment_meta)            - add meta when recording experiment

              (record_uoa)                 - use this UOA to recrod experiments instead of randomly generated ones
            
              (solution_conditions)        - list of conditions:
                                               ["first key", "extra key", "condition", value]
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import copy
    import os

    curdir=os.getcwd()

    # Setting output
    o=i.get('out','')
    oo=''
    if o=='con': oo='con'

    hos=i.get('host_os','')
    tos=i.get('target_os','')
    tdid=i.get('target_device_id','')

    pi=i.get('platform_info',{})

    scfg=i.get('scenario_cfg',{})

    la=i.get('local_autotuning','')

    program_tags=i.get('program_tags','').strip()
    program_uoa=i.get('program_uoa','')
    if program_uoa=='': program_uoa=i.get('data_uoa','')
    cmd_key=i.get('cmd_key','')
    dataset_uoa=i.get('dataset_uoa','')
    dataset_file=i.get('dataset_file','')

    sdeps=i.get('dependencies',{})

    apc=i.get('ask_pipeline_choices','')

    smuoa=i.get('scenario_module_uoa','')

    rep=i.get('repetitions','')

    iterations=i.get('iterations','')
    if iterations=='': iterations=30

    cat=i.get('calibration_time','')
    if cat=='': cat=10.0
    
    objective=i.get('objective','')
    if objective=='': objective='min'

    xobjective=''
    if objective!='':
       xobjective='#'+objective

    seed=i.get('seed','')

    sdesc=scfg.get('desc','')
    ssdesc=i.get('subscenario_desc','')

    ktmp=i.get('keep_tmp','')
    kexp=i.get('keep_experiments','')

    scon=scfg.get('solution_conditions',[])

    er=i.get('exchange_repo','')
    esr=i.get('exchange_subrepo','')

    repeat=i.get('repeat','')

    # Check (multi-objective) characteristics to process
    ok=scfg.get('original_keys',[])
    fk=scfg.get('frontier_keys',[])
    ik=scfg.get('improvements_keys',[])
    rk=scfg.get('record_keys',[])
    pk=scfg.get('print_extra_keys',[])

    threshold=scfg.get('reference_threshold','')
    if threshold=='': threshold=0.03

    # Update objective (min,max,exp) - if exp, need to add confidence interval
    #                                  otherwise we are not using points with high variation!          
    for l in range(0, len(ok)):
         ok[l]=ok[l].replace('$#obj#$',objective)

    for l in range(0, len(fk)):
         fk[l]=fk[l].replace('$#obj#$',objective)

    for l in range(0, len(ik)):
         ik[l]=ik[l].replace('$#obj#$',objective)

    for l in range(0, len(rk)):
         rk[l]=rk[l].replace('$#obj#$',objective)

    for l in range(0, len(pk)):
         pk[l]=pk[l].replace('$#obj#$',objective)

    #**************************************************************************************************************
    # Preparing pipeline with a temporary directory and random choices if not fixed (progs, datsets, etc)
    ii={'action':'pipeline',
        'module_uoa':cfg['module_deps']['program'],
        'host_os':hos,
        'target_os':tos,
        'target_device_id':tdid,
        'dependencies':sdeps,
        'force_resolve_deps':'yes',
        'program_tags':program_tags,
        'program_uoa':program_uoa,
        'cmd_key':cmd_key,
        'dataset_uoa':dataset_uoa,
        'dataset_file':dataset_file,
        'skip_local':'yes',
        'calibration_time':cat,
        'generate_rnd_tmp_dir':'yes', # to be able to run crowdtuning in parallel on the same machine ...
        'prepare':'yes',
        'out':oo}
    if apc!='yes':
       ii['random']='yes'
    r=ck.access(ii)
    if r['return']>0: return r

    ready=r['ready']
    unexpected=False
    if ready!='yes':
       x='   WARNING: didn\'t manage to prepare program optimization workflow'

       ck.out('')
       ck.out(x+' ...')

       rx=log({'file_name':cfg['log_file_own'], 'skip_header':'yes', 'text':x+'\n'})
    else:
       ################################################################################
       # Prepare (tmp) experiment entry
       eruoa0=i.get('record_repo','')

       # Continue
       del(r['return'])

       pipeline=r

       state=r['state']
       tmp_dir=state['tmp_dir']

       choices=r['choices']
       ft=r['features']

       prog_uoa=choices['data_uoa']
       cmd_key=choices.get('cmd_key','')
       dataset_uoa=choices.get('dataset_uoa','')
       dataset_file=choices.get('dataset_file','')

       cver=ft.get('compiler_version',{}).get('str','')

       meta=i.get('experiment_meta',{})
       meta['objective']=objective

       mmeta=copy.deepcopy(meta) # to add extra when recording local experiments (helper)
       mmeta['scenario_module_uoa']=smuoa
       mmeta['scenario_desc']=sdesc
       mmeta['subscenario_desc']=ssdesc

       mmeta['program_uoa']=prog_uoa
       mmeta['cmd_key']=cmd_key
       mmeta['dataset_uoa']=cmd_key
       mmeta['dataset_file']=dataset_file

       euoa0=i.get('record_uoa','')
       puid0=''
       found=False
       results00={}
       if la=='yes':
          if o=='con':
             ck.out('')
             ck.out('Searching if similar experiment already exists in your local repo ...')

          print (mmeta)

          # Try to find in local experiments by meta
          jj={'action':'get',
              'module_uoa':cfg['module_deps']['experiment'],
              'data_uoa':euoa0,
              'meta':mmeta,
              'flat_keys_list':ik,
              'load_json_files':['features_flat','flat','features']
             }
          rx=ck.access(jj)
          if rx['return']>0: return rx

          points=rx['points']
          if len(points)>0:
             # Search for reference/pemanent point 
             for q in points:
                 if q.get('features',{}).get('permanent','')=='yes':
                    found=True
                    repeat=q.get('features',{}).get('choices',{}).get('repeat','')
                    euoa0=q['data_uid']
                    puid0=q['point_uid']
                    break

             if found and o=='con':
                ck.out('')
                ck.out('  Found previous exploration ('+euoa0+'/'+puid0+') - restarting ...')

       if euoa0=='':
          rx=ck.gen_uid({})
          if rx['return']>0: return rx
          euoa0=rx['data_uid'] # Where to keep experiment

       lx= ' * Program:                  '+prog_uoa+'\n' \
           ' * CMD:                      '+cmd_key+'\n' \
           ' * Dataset:                  '+dataset_uoa+'\n' \
           ' * Dataset file:             '+dataset_file+'\n'

       if repeat!='':
          lx+=' * Kernel repetitions:       '+str(repeat)+'\n'

       lx+=' * Default compiler version: '+cver+'\n' \
           ' * Experiment UOA:           '+euoa0+'\n' \

       if o=='con':
          ck.out(line)
          ck.out('Prepared experiment:')
          ck.out('')
          ck.out(lx)

       lx=' ===============================================================================\n' \
          ' * Scenario:                 '+sdesc+'\n' \
          ' * Sub scenarion:            '+ssdesc+'\n' \
          ' * Number of iterations:     '+str(iterations)+'\n'+lx

       r=log({'file_name':cfg['log_file_own'], 'skip_header':'yes', 'text':lx})
       if r['return']>0: return r

       # Saving pipeline
       pipeline_copy=copy.deepcopy(pipeline)

       # Run with default optimization
       if o=='con':
          ck.out(line)
          ck.out('Running first experiment with default optimization:')
          ck.out('')

       pipeline=copy.deepcopy(pipeline_copy)
       pup0=scfg.get('experiment_0_pipeline_update',{})

       if rep!='': pup0['repetitions']=rep

       # ***************************************************************** FIRST EXPERIMENT
       ii={'action':'autotune',
           'module_uoa':cfg['module_deps']['pipeline'],
           'data_uoa':cfg['module_deps']['program'],
           'host_os':hos,
           'target_os':tos,
           'target_device_id':tdid,

           "pipeline":pipeline,

           "iterations":1,

           "choices_order":[ [] ],

           "tmp_dir":tmp_dir,

           "record":"yes",
           "record_uoa":euoa0,
           "record_repo":eruoa0,
           "record_permanent":'yes',

           "skip_record_pipeline":"yes",
           "skip_record_desc":"yes",

           "tags":"crowdtuning,tmp",

           "meta":mmeta,

           'out':oo
          }

       if len(rk)>0:
          ii['process_multi_keys']=rk

       r=ck.merge_dicts({'dict1':ii, 'dict2':pup0})
       if r['return']>0: return r
       ii=r['dict1']

       if 'pipeline_update' not in ii: ii['pipeline_update']={}
       ii['pipeline_update']['repeat']=repeat

       r=ck.access(ii)
       if r['return']>0: 
          rx=log({'file_name':cfg['log_file_own'], 'skip_header':'yes', 'text':'   FAILURE: '+r['error']+'\n'})
          return r

       lio=r['last_iteration_output']
       fail=lio.get('fail','')
       if fail=='yes':
          unexpected=True
          x='   WARNING: pipeline execution failed ('+lio.get('fail_reason','')+')'

          ck.out('')
          ck.out(x+' ...')

          rx=log({'file_name':cfg['log_file_own'], 'skip_header':'yes', 'text':x+'\n'})
       else:
          # get flat dict from last stat analysis to calculate improvements of all characteristics
          fdfi=r.get('last_stat_analysis',{}).get('dict_flat',{})

          state=lio.get('state',{})
          repeat=state.get('repeat','')
          ftmp_dir=state.get('cur_dir','')

          ri=r['recorded_info']
          points1=ri.get('points',[])
          ruid=ri['recorded_uid']       # UID of the default one

          if len(points1)==0:
             unexpected=True

             x='   WARNING: explored points were not recorded (possibly internal error)'

             ck.out('')
             ck.out(x+' ...')

             rx=log({'file_name':cfg['log_file_own'], 'skip_header':'yes', 'text':x+'\n'})
          else:
             # Check if need to run extra experiments
             # (for example when crowdsourcing program benchmarking or compiler bug detection,
             #  no need to run extra experiments)

             iii={'action':'get',
                  'module_uoa':cfg['module_deps']['experiment'],
                  'data_uoa':ruid,
                  'flat_keys_list':ik,
                  'load_json_files':['features_flat','flat','features']}

             # Load default point info
             r=ck.access(iii)
             if r['return']>0: 
                rx=log({'file_name':cfg['log_file_own'], 'skip_header':'yes', 'text':'   FAILURE: '+r['error']+'\n'})
                return r

             results1=r.get('points',{})

             # If local autotuning and appending to existing one,
             # check if still the same execution ...
             if la=='yes' and found:
                puid00=points1[0]

                rx=compare_results({'point0':puid0,
                                    'point1':puid00,
                                    'results':results1,
                                    'keys':ok,
                                    'threshold':threshold})
                if rx['return']>0: return rx
                diff=rx['different']

                if diff=='yes':
                   if o=='con':
                      ck.out('')
                      ck.out('Results differ: '+rx['report']+' ...')
                      ck.out('Deleting point '+puid00+' ...')

                   rx=ck.access({'action':'delete_points',
                                 'module_uoa':cfg['module_deps']['experiment'],
                                 'points':[{'module_uid':cfg['module_deps']['experiment'], 
                                            'data_uid':euoa0,
                                            'point_uid':puid00}],
                                 'out':oo})
                   if rx['return']>0: return rx

                   unexpected=True

                   x='   WARNING: reference points differ - can\'t continue ...'

                   ck.out('')
                   ck.out(x+' ...')

                   rx=log({'file_name':cfg['log_file_own'], 'skip_header':'yes', 'text':x+'\n'})

                   return {'return':0}
                else:
                   if o=='con':
                      ck.out('')
                      ck.out('Substituting reference point '+puid0+' ...')

                   rx=ck.access({'action':'delete_points',
                                 'module_uoa':cfg['module_deps']['experiment'],
                                 'points':[{'module_uid':cfg['module_deps']['experiment'], 
                                            'data_uid':euoa0,
                                            'point_uid':puid0}],
                                 'out':oo})
                   if rx['return']>0: return rx

                   # Recreating list of original points
                   points1=[]
                   for q in results1:
                       qq=q['point_uid']
                       if qq!=puid0:
                          points1.append(qq)

             # Continue autotuning

             results2={}
             points2=[]

             if scfg.get('skip_autotuning','')!='yes':
                # *************************************************************** PREPARE AUTOTUNING
                # Prepare autotuning
                pup1=scfg.get('experiment_1_pipeline_update',{})
                pup1['frontier_keys']=fk

                if rep!='': pup1['repetitions']=rep
                if seed!='': pup1['seed']=seed

                ################################################################################
                # Run autotuning
                if o=='con':
                   ck.out(line)
                   ck.out('Running multi-dimensional and multi-objective autotuning ...')
                   ck.out('')

                pipeline=copy.deepcopy(pipeline_copy)

                ii={'action':'autotune',

                    'module_uoa':cfg['module_deps']['pipeline'],
                    'data_uoa':cfg['module_deps']['program'],
                    'host_os':hos,
                    'target_os':tos,
                    'target_device_id':tdid,

                    "pipeline":pipeline,

                    "iterations":iterations,

                    "choices_order":[ [] ],

                    "tmp_dir":tmp_dir,
   
                    "tags":"crowdtuning,tmp",

                    "meta":mmeta,

                    'flat_dict_for_improvements':fdfi,

                    "record":"yes",
                    "record_uoa":euoa0,
                    "record_repo":eruoa0,

                    "skip_record_pipeline":"yes",
                    "skip_record_desc":"yes",

                    'out':oo
                   }

                if len(rk)>0:
                   ii['process_multi_keys']=rk

                r=ck.merge_dicts({'dict1':ii, 'dict2':pup1})
                if r['return']>0: return r
                ii=r['dict1']

                if 'pipeline_update' not in ii: ii['pipeline_update']={}
                ii['pipeline_update']['repeat']=repeat

                r=ck.access(ii)
                if r['return']>0: 
                   rx=log({'file_name':cfg['log_file_own'], 'skip_header':'yes', 'text':'   FAILURE: '+r['error']+'\n'})
                   return r

#               If no frontier, points will not be added, so will not use it
#                ri=r['recorded_info']
#                points2=ri['points']

                # Load updated point info
                r=ck.access(iii)
                if r['return']>0: return r
                results2=r.get('points',{})

                for k in results2:
                    kk=k.get('point_uid','')
                    if kk!='' and kk not in points2:
                       points2.append(kk)

             ################################################################################
             rp='New solution was not found ...'

             pif=pi.get('features',{})

             # Prepare meta
             plat_uid=pif.get('platform_uid','')
             plat_cpu_uid=pif.get('cpu_uid','')
             plat_os_uid=pif.get('os_uid','')
             plat_acc_uid=pif.get('acc_uid','')

             import json

             # Check if any older solution got updated
             if o=='con':
                ck.out(line)
                ck.out('Checking solutions for specific conditions:')
                ck.out('  Experiment UOA:     '+euoa0)
                ck.out('  Original solutions: '+json.dumps(points1))
                ck.out('  New solutions:      '+json.dumps(points2))

             ii={'action':'check',
                 'module_uoa':cfg['module_deps']['math.conditions'],
                 'original_points':points1,
                 'new_points':points2,
                 'results':results2,
                 'conditions':scon}
             if objective!='':
                ii['middle_key']=xobjective
             r=ck.access(ii)
             if r['return']>0: return r 

             gpoints=r['good_points']
             dpoints=r['points_to_delete']

             # Points that should be deleted
             if len(dpoints)>0:
                if o=='con':
                   ck.out('')
                   ck.out('       Following points will be deleted: '+json.dumps(dpoints))

                xdpoints=[]
                for q in dpoints:
                    found=False
                    for qq in results2:
                        if qq['point_uid']==q:
                           found=True
                           break
                    if found:
                       xdpoints.append(qq)

                # Attempt to delete non-optimal solutions
                rx=ck.access({'action':'delete_points',
                              'module_uoa':cfg['module_deps']['experiment'],
                              'points':xdpoints,
                              'out':oo})
                if rx['return']>0: return rx

             # Good points 
             report=''
             if len(gpoints)==0:
                report+='      New solutions were not found...\n'
             else:
                report+='      FOUND NEW SOLUTION(S)!\n'

                if len(ik)>0:
                   keys=[]
                   for x in ik:
                       keys.append(x)
                   for x in pk:
                       keys.append(x)

                   # Find size of keys
                   il=0
                   for k in keys:
                       if len(k)>il: il=len(k)

                   # Find point in results
                   for q in gpoints:
                       report+='        '+q+'\n'

                       qq={}
                       for e in results2:
                           if e.get('point_uid','')==q:
                              qq=e
                              break

                       if len(qq)>0:
                          for k in keys:
                              behavior=qq.get('flat',{})
                              choices=qq.get('features_flat',{})
                              ft=qq.get('features',{})

                              cdesc=pipeline.get('choices_desc',{})

                              dv=behavior.get(k,None)
                              if dv!=None:
                                 ix=len(k)

                                 y=''
                                 try:
                                    y=('%.3f' % dv)
                                 except Exception as e: 
                                    y=dv
                                    pass

                                 report+='          * '+ k+(' ' * (il-ix))+' : '+y+'\n' 

                if o=='con':
                   ck.out('')
                   ck.out(report)

                r=log({'file_name':cfg['log_file_own'], 'skip_header':'yes', 'text':report})

                if la!='yes':
                   # Packing new points
                   if o=='con':
                      ck.out('')
                      ck.out('       Packing solution(s) ...')

                   # Add original points and remove delete ones
                   ppoints=[]
                   for q in points2:
                       if q not in dpoints:
                          ppoints.append(q)

                   rx=ck.access({'action':'pack',
                                 'module_uoa':cfg['module_deps']['experiment'],
                                 'data_uoa':euoa0,
                                 'points':ppoints})
                   if rx['return']>0: return rx
                   ps=rx['file_content_base64']

                   if o=='con':
                      ck.out('')
                      ck.out('       Recording solution(s) ...')

                   # Adding solution
                   ii={'action':'add_solution',
                       'module_uoa':work['self_module_uid'],
                       'repo_uoa':er,
                       'remote_repo_uoa':esr,
                       'scenario_module_uoa':smuoa,
                       'meta':meta,
                       'packed_solution':ps,
                       'out':oo}
                   rx=ck.access(ii)
                   if rx['return']>0: return rx















          ################################################################################
          # Clean temporal directory and entry
          if ktmp!='yes':
             if o=='con':
                ck.out('')
                ck.out('Removing temporal directory '+ftmp_dir+' ...')
             import shutil
             os.chdir(curdir)
             try:
                shutil.rmtree(ftmp_dir, ignore_errors=True)
             except Exception as e: 
                if o=='con':
                   ck.out('')
                   ck.out('WARNING: can\'t fully erase tmp dir')
                   ck.out('')
                pass

          if kexp!='yes' and not unexpected:
             if o=='con':
                ck.out('')
                ck.out('Removing experiment entry '+euoa0+' ...')
#
             ii={'action':'rm',
                 'module_uoa':cfg['module_deps']['experiment'],
                 'data_uoa':euoa0,
                 'force':'yes'}
             r=ck.access(ii)
             # Skip return code
          else:
             if o=='con':
                ck.out('')
                ck.out('Note that you can:')
                ck.out('  * replay above experiments via "ck replay experiment:'+euoa0+' (--point={above solution UID})"')
                ck.out('  * plot graph for above experiments via "ck plot graph:'+euoa0+'"')

       if i.get('only_one_run','')=='yes':
          finish=True

    return {'return':0}

##############################################################################
# compare results (if similar or not)

def compare_results(i):
    """
    Input:  {
              results     - dict with results from experiments
              point0      - original point
              point1      - new point to compare
              keys        - keys to compare
              (threshold) - 0.03
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    report=''

    results=i['results']
    puid0=i['point0']
    puid1=i['point1']
    keys=i['keys']

    diff='no'

    t=i.get('threshold','')
    if t=='': t=0.03
    t=float(t)

    ch0={}
    for q in results:
        if q['point_uid']==puid0:
           ch0=q.get('flat',{})
           break

    ch1={}
    for q in results:
        if q['point_uid']==puid1:
           ch1=q.get('flat',{})
           break
       
    fine=True
    for k in keys:
        v0=ch0.get(k, None)
        v1=ch1.get(k, None)

        if (v0==None and v1!=None) or (v0!=None and v1==None):
           report='  Difference for "'+k+'" - v0!=v1'
           fine=False
           break
        else:
           if type(v0)==float or type(v0)==int or type(v0)==long:
              if not (type(v1)==float or type(v1)==int or type(v1)==long):
                 report='  Difference for "'+k+'" - types do not match'
                 fine=False
                 break
              else:
                 if v1==0:
                    report='  Difference for "'+k+'" - v1=0'
                    fine=False
                    break

                 d=float(v0)/float(v1)
                 if d<(1-t) or d>(1+t):
                    report='  key "'+k+'" variation out of normal ('+('%2.3f'%d)+')'
                    fine=False
                    break

           elif v0!=v1:
                report='  key "'+k+'" - v0!=v1'
                fine=False
                break

    if not fine: 
       diff='yes'

    return {'return':0, 'different':diff, 'report':report}
