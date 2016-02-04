#
# Collective Knowledge: compiler flags crowdtuning (crowdsource autotuning via spare computers such as mobile devices)
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
compiler_choices='#choices#compiler_flags#'

line='================================================================'

fsummary='summary.json'

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
# prune compiler flags

def prune(i):
    """
    Input:  {
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    print ('prune compiler flags')

    ck.out('')
    ck.out('Command line: ')
    ck.out('')

    import json
    cmd=json.dumps(i, indent=2)

    ck.out(cmd)

    return {'return':0}

##############################################################################
# show results

def html_viewer(i):
    """      
    Input:  {
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    global cfg, work

    mcfg=i.get('module_cfg',{})
    if len(mcfg)>0: cfg=mcfg

    mwork=i.get('module_work',{})
    if len(mwork)>0: work=mwork

    import os

    ruoa=i.get('repo_uoa','')
    muoa=work['self_module_uoa']
    muid=work['self_module_uid']
    duoa=i.get('data_uoa','')

    # Load Entry
    r=ck.access({'action':'load',
                 'repo_uoa':ruoa,
                 'module_uoa':muoa,
                 'data_uoa':duoa})
    if r['return']>0: 
       return {'return':0, 'html':'<b>CK error:</b> '+r['error']+'!'}

    p=r['path']
    d=r['dict']
    duid=r['data_uid']

    h='<center>\n'
    h+='<H2>Solutions: '+cfg['desc']+'</H2>\n'
    h+='</center>\n'

    h+='<p>\n'

    h+='<table border="0" cellpadding="2" cellspacing="0">\n'
    x=muid
    if muoa!=muid: x+=' ('+muoa+')'
    h+='<tr><td><b>Scenario UID</b><td>'+x+'</td></tr>\n'
    h+='<tr><td><b>Data UID</b><td>'+duid+'</td></tr>\n'
    h+='<tr><td><td></td></tr>\n'

    pr=cfg.get('prune_results',[])
    mm=d.get('meta',{})
    for q in pr:
        qd=q.get('desc','')
        qi=q.get('id','')

        v=mm.get(qi,'')

        h+='<tr><td><b>'+qd+'</b><td>'+v+'</td></tr>\n'

    h+='</table>\n'

    h+='<p>\n'
    h+='<center>\n'

    # Load summary
    sols=[]

    psum=os.path.join(p, fsummary)
    if os.path.isfile(psum):
       rx=ck.load_json_file({'json_file':psum})
       if rx['return']>0: return rx
       sols=rx['dict']

    # List solutions
    if len(sols)==0:
       h+='<h2>No solutions found!</h2>\n'
    else:
       # Check host URL prefix and default module/action
       url0=ck.cfg.get('wfe_url_prefix','')

       h+='<table class="ck_table" border="0">\n'
       h+=' <tr style="background-color:#cfcfff;">\n'
       h+='  <td><b>\n'
       h+='   #\n'
       h+='  </b></td>\n'
       h+='  <td><b>\n'
       h+='   Solution UID\n'
       h+='  </b></td>\n'
       h+='  <td><b>\n'
       h+='   Explorations\n'
       h+='  </b></td>\n'
       h+='  <td><b>\n'
       h+='   Program\n'
       h+='  </b></td>\n'
       h+='  <td><b>\n'
       h+='   CMD\n'
       h+='  </b></td>\n'
       h+='  <td><b>\n'
       h+='   Dataset\n'
       h+='  </b></td>\n'
       h+='  <td><b>\n'
       h+='   Dataset file\n'
       h+='  </b></td>\n'
       h+='  <td><b>\n'
       h+='   Target OS\n'
       h+='  </b></td>\n'
       h+=' </tr>\n'

       # List
       num=0
       for q in sols: # already sorted by most "interesting" solutions (such as highest speedups)

           num+=1

           suid=q['solution_uid']
           iterations=q['iterations']

           choices=q['choices']

           program_uoa=choices.get('data_uoa','')
           cmd=choices.get('cmd_key','')
           dataset_uoa=choices.get('dataset_uoa','')
           dataset_file=choices.get('dataset_file','')
           target_os=choices.get('target_os','')

           speedup=''

           cmd1=''
           cmd2=''

           h+=' <tr>\n'
           h+='  <td valign="top">\n'
           h+='   '+str(num)+'\n'
           h+='  </td>\n'

           h+='  <td valign="top">\n'
           h+='   '+suid+'</a>\n'
           h+='  </td>\n'

           h+='  <td valign="top">\n'
           h+='   '+str(iterations)+'\n'
           h+='  </td>\n'

           h+='  <td valign="top">\n'
           h+='   <a href="'+url0+'wcid=program:'+program_uoa+'">'+program_uoa+'</a>\n'
           h+='  </td>\n'

           h+='  <td valign="top">\n'
           h+='   '+cmd+'\n'
           h+='  </td>\n'

           h+='  <td valign="top">\n'
           h+='   <a href="'+url0+'wcid=dataset:'+dataset_uoa+'">'+dataset_uoa+'</a>\n'
           h+='  </td>\n'

           h+='  <td valign="top">\n'
           h+='   '+dataset_file+'\n'
           h+='  </td>\n'

           h+='  <td valign="top">\n'
           h+='   <a href="'+url0+'wcid=os:'+target_os+'">'+target_os+'</a>\n'
           h+='  </td>\n'

           h+=' </tr>\n'

       h+='</table>\n'
    h+='</center>\n'

    return {'return':0, 'html':h}

##############################################################################
# crowdsource these experiments

def crowdsource(i):
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

              (scenario)                   - module UOA of crowdsourcing scenario

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

              (objective)                  - extension to flat characteristics (min,max,exp) to tune on Pareto
                                             (default: min - to see what we can squeeze from a given architecture)

              (keep_tmp)                   - if 'yes', do not remove run batch
              (keep_experiments)           - if 'yes', do not remove experiments entries

              (only_one_run)               - if 'yes', run scenario ones (useful for autotuning a given program)

              (ask_pipeline_choices)       - if 'yes', ask for each pipeline choice, otherwise random selection 

              (platform_info)              - reusing platform info
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    global cfg, work

    import copy

    mcfg=i.get('module_cfg',{})
    if len(mcfg)>0: 
       cfg=mcfg

    mwork=i.get('module_work',{})
    if len(mwork)>0: work=mwork

    # Setting output
    o=i.get('out','')
    oo=''
    if o=='con': oo='con'

    quiet=i.get('quiet','')

    er=i.get('exchange_repo','')
    if er=='': er=ck.cfg['default_exchange_repo_uoa']
    esr=i.get('exchange_subrepo','')
    if esr=='': esr=ck.cfg['default_exchange_subrepo_uoa']

    if i.get('local','')=='yes': 
       er='local'
       esr=''

    la=i.get('local_autotuning','')

    user=''

    # Initialize local environment for program optimization ***********************************************************
    pi=i.get('platform_info',{})
    if len(pi)==0:
       ii=copy.deepcopy(i)
       ii['action']='initialize'
       ii['module_uoa']=cfg['module_deps']['program.optimization']
       ii['exchange_repo']=er
       ii['exchange_subrepo']=esr
       r=ck.access(ii)
       if r['return']>0: return r

       pi=r['platform_info']
       user=r.get('user','')

    hos=pi['host_os_uoa']
    hosd=pi['host_os_dict']

    tos=pi['os_uoa']
    tosd=pi['os_dict']
    tbits=tosd.get('bits','')

    hosz=hosd.get('base_uoa','')
    if hosz=='': hosz=hos
    tosz=tosd.get('base_uoa','')
    if tosz=='': tosz=tos

    remote=tosd.get('remote','')

    tdid=pi['device_id']

    program_tags=i.get('program_tags','')
    if program_tags=='': program_tags=cfg['program_tags']

    # Check that has minimal dependencies for this scenario ***********************************************************
    sdeps=copy.deepcopy(cfg['deps'])
    if len(sdeps)>0:
       if o=='con':
          ck.out(line)
          ck.out('Resolving software dependencies required for this scenario ...')
          ck.out('')

       ii={'action':'resolve',
           'module_uoa':cfg['module_deps']['env'],
           'host_os':hos,
           'target_os':tos,
           'device_id':tdid,
           'deps':sdeps,
           'add_customize':'yes'}
       if quiet=='yes': 
          ii['random']='yes'
       else:
          ii['out']=oo
       rx=ck.access(ii)
       if rx['return']>0: return rx

       sdeps=rx['deps'] # Update deps (add UOA)

    cpu_name=pi.get('features',{}).get('cpu',{}).get('name','')
    compiler_soft_uoa=sdeps.get('compiler',{}).get('dict',{}).get('soft_uoa','')
    compiler_env=sdeps.get('compiler',{}).get('bat','')

    # Detect real compiler version ***********************************************************
    if o=='con':
       ck.out(line)
       ck.out('Detecting compiler version ...')

    ii={'action':'detect',
        'module_uoa':cfg['module_deps']['soft'],
        'data_uoa':compiler_soft_uoa,
        'host_os':hos,
        'target_os':tos,
        'target_device_id':tdid,
        'env':compiler_env}
    r=ck.access(ii)
    if r['return']>0: return r
    compiler_version=r['version_str']

    compiler='GCC '+compiler_version

    if o=='con':
       ck.out('')
       ck.out('* Compiler: '+compiler)
       ck.out('* CPU:      '+cpu_name)

    # Start preparing input to run program.optimization
    ii=copy.deepcopy(i)

    ii['action']='run'
    ii['module_uoa']=cfg['module_deps']['program.optimization']

    ii['host_os']=hos
    ii['target_os']=tos
    ii['target_device_id']=tdid
    ii['dependencies']=sdeps

    ii['scenario_cfg']=cfg

    ii['platform_info']=pi

    ii['program_tags']=program_tags

    ii['scenario_module_uoa']=work['self_module_uid']

    ii['experiment_meta']={'cpu_name':cpu_name,
                           'compiler':compiler}

    ii['exchange_repo']=er
    ii['exchange_subrepo']=esr

    ii['user']=user

    # Select sub-scenario ********************************************************************
    from random import randint
    ss=1 # num of scenarios

    sx=randint(1,ss)

    if sx==1 or la=='yes':
       # **************************************************************** explore random program/dataset
       sdesc='explore random program/cmd/data set'
       if o=='con':
          ck.out('')
          ck.out('  ****** Sub-scenario: '+sdesc+' ******')

       ii['subscenario_desc']=sdesc

       r=ck.access(ii)
       if r['return']>0: return r










    return {'return':0, 'platform_info':pi}
