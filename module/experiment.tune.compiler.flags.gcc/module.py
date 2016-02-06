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

              html
              (style)      - styles - useful for plotting JavaScript-based graphs
            }

    """

    import os
    global cfg, work

    mcfg=i.get('module_cfg',{})
    if len(mcfg)>0: cfg=mcfg

    mwork=i.get('module_work',{})
    if len(mwork)>0: work=mwork

    st=''

    url0=ck.cfg.get('wfe_url_prefix','')

    ap=i.get('all_params',{})

    ruoa=i.get('repo_uoa','')
    muoa=work['self_module_uoa']
    muid=work['self_module_uid']
    duoa=i.get('data_uoa','')

    ik=cfg['improvements_keys']

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

    h+='<H2>Distinct solutions: '+cfg['desc']+'</H2>\n'
    h+='</center>\n'

    h+='<p>\n'

    h+='<table border="0" cellpadding="4" cellspacing="0">\n'
    x=muid
    if muoa!=muid: x+=' ('+muoa+')'
    h+='<tr><td><b>Scenario UID</b><td>'+x+'</td></tr>\n'
    h+='<tr><td><b>Data UID</b><td>'+duid+'</td></tr>\n'
    h+='<tr><td><td></td></tr>\n'

    pr=cfg.get('prune_results',[])
    mm=d.get('meta',{})
    obj=mm.get('objective','')

    for k in pr:
        qd=k.get('desc','')
        qi=k.get('id','')
        qr=k.get('ref_uid','')
        qm=k.get('ref_module_uoa','')

        x=mm.get(qi,'')
        if x!='' and qm!='' and qr!='':
           xuid=mm.get(qr,'')
           if xuid!='':
              x='<a href="'+url0+'wcid='+qm+':'+xuid+'">'+x+'</a>'

        h+='<tr><td><b>'+qd+'</b><td>'+x+'</td></tr>\n'

    h+='<tr><td><td></td></tr>\n'

    kk=0
    for kx in range(0, len(ik)):
        k=ik[kx]
        k1=k.replace('$#obj#$',obj)
        ik[kx]=k1

        kk+=1

        h+='<tr><td><b>Improvement key IK'+str(kk)+'</b><td>'+k1+'</td></tr>\n'

    ik0=ik[0] # first key to sort

    h+='</table>\n'

    h+='<p>\n'
    h+='<center>\n'

    # graph
    graph={"0":[]}

    # Load summary
    sols=[]

    psum=os.path.join(p, fsummary)
    if os.path.isfile(psum):
       rx=ck.load_json_file({'json_file':psum})
       if rx['return']>0: return rx
       sols=rx['dict']

    h+='<p>\n'
    h+='$#graph#$\n'
    h+='<p>\n'

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

       for k in range(0, len(ik)):
           h+='  <td><b>\n'
           h+='   IK'+str(k+1)+'\n'
           h+='  </b></td>\n'

       h+='  <td><b>\n'
       h+='   Solution choices\n'
       h+='  </b></td>\n'
       h+='  <td><b>\n'
       h+='   Reference choices\n'
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
       iq=-1
       iq1=0

       res={}
       sres=[]
       ires=0

       while iq1<len(sols): # already sorted by most "interesting" solutions (such as highest speedups)
           if iq!=iq1:
              num+=1

              iq+=1
              q=sols[iq]

              suid=q['solution_uid']

              res={}
              ref_res={}
              sres=[]
              ires=0

              # Try to load all solutions
              p1=os.path.join(p, suid)

              try:
                 dirList=os.listdir(p1)
              except Exception as e:
                  None
              else:
                  for fn in dirList:
                      if fn.startswith('ckp-') and fn.endswith('.flat.json'):
                         uid=fn[4:-10]

                         px=os.path.join(p1, fn)
                         rx=ck.load_json_file({'json_file':px})
                         if rx['return']>0: return rx
                         d1=rx['dict']

                         px=os.path.join(p1,'ckp-'+uid+'.features_flat.json')
                         if rx['return']>0: return rx
                         d2=rx['dict']

                         x={'flat':d1, 'features_flat':d2}

                         px=os.path.join(p1, 'ckp-'+uid+'.features.json')
                         rx=ck.load_json_file({'json_file':px})
                         if rx['return']>0: return rx
                         dx=rx['dict']

                         if dx.get('permanent','')=='yes':
                            ref_res==x
                         else:
                            res[uid]=x
                         
                  rr=list(res.keys())
                  sres=sorted(rr, key=lambda v: (float(res[v].get('flat',{}).get(ik0,0.0))), reverse=True)

           rr={}
           if ires<len(sres):
              rr=res.get(sres[ires],{})
              ires+=1

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

              ss='S'+str(num)
              h+=' <tr>\n'
              h+='  <td valign="top">\n'
              if ires<2:

                 h+='   '+ss+'\n'
              h+='  </td>\n'

              h+='  <td valign="top">\n'
              if ires<2:
                 h+='   '+suid+'\n'
              h+='  </td>\n'

              for k in range(0, len(ik)):
                  h+='  <td>\n'
                  dv=rr.get('flat',{}).get(ik[k],'')

                  # Add to graph (first dimension and first solution)
                  if k==0 and ires<2:
                     graph['0'].append([ss,dv])

                  y=''
                  try:
                     y=('%.2f' % dv)
                  except Exception as e: 
                     y=dv
                     pass

                  if dv!='':
                     if dv>1.0:
                        y='<span style="color:#bf0000">'+y+'</span>'
                     elif dv!=0:
                        y='<span style="color:#0000bf">'+y+'</span>'
                  

                  h+=str(y)+'\n'
                  h+='  </td>\n'


              h+='  <td><b>\n'
              h+='   \n'
              h+='  </b></td>\n'
              h+='  <td><b>\n'
              h+='   \n'
              h+='  </b></td>\n'

              h+='  <td valign="top">\n'
              if ires<2:
                 h+='   '+str(iterations)+'\n'
              h+='  </td>\n'

              h+='  <td valign="top">\n'
              if ires<2:
                 h+='   <a href="'+url0+'wcid=program:'+program_uoa+'">'+program_uoa+'</a>\n'
              h+='  </td>\n'

              h+='  <td valign="top">\n'
              if ires<2:
                 h+='   '+cmd+'\n'
              h+='  </td>\n'

              h+='  <td valign="top">\n'
              if ires<2:
                 h+='   <a href="'+url0+'wcid=dataset:'+dataset_uoa+'">'+dataset_uoa+'</a>\n'
              h+='  </td>\n'

              h+='  <td valign="top">\n'
              if ires<2:
                 h+='   <a href="'+url0+'action=pull&common_func=yes&cid=dataset:'+dataset_uoa+'&filename='+dataset_file+'">'+dataset_file+'</a>\n'
              h+='  </td>\n'

              h+='  <td valign="top">\n'
              if ires<2:
                 h+='   <a href="'+url0+'wcid=os:'+target_os+'">'+target_os+'</a>\n'
              h+='  </td>\n'

              h+=' </tr>\n'

           else:
              iq1+=1

       h+='</table>\n'
    h+='</center>\n'

    h+='<p>&nbsp;<p>\n'

    rx=ck.access({'action':'links',
                  'module_uoa':cfg['module_deps']['program.optimization']})
    if rx['return']>0: return rx
    h+=rx['html']

    # Plot graph
    hg=''
    ftmp=''

    if len(graph['0'])>0:
       ii={'action':'plot',
           'module_uoa':cfg['module_deps']['graph'],

           "table":graph,

           "ymin":0,

           "ignore_point_if_none":"yes",

           "plot_type":"d3_2d_bars",

           "display_y_error_bar":"no",

           "title":"Powered by Collective Knowledge",

           "axis_x_desc":"Distinct optimization solutions",
           "axis_y_desc":"Max speedup (IK1)",

           "plot_grid":"yes",

           "d3_div":"ck_interactive",

           "image_width":"900",
           "image_height":"400"}

       # Trick to save to file (for interactive/live articles)
       if ap.get('fgg_save_graph_to_file','')=='yes':
          import copy
          iii=copy.deepcopy(ii)
          iii["substitute_x_with_loop"]="yes"
          iii["plot_type"]="mpl_2d_bars" 
          if 'ymin' in iii: del(iii['ymin'])
          if 'ymax' in iii: del(iii['ymax'])

          # Prepare batch file
          rx=ck.gen_tmp_file({'prefix':'tmp-', 'suffix':'.json'})
          if rx['return']>0: return rx
          ftmp=rx['file_name']

          rx=ck.save_json_to_file({'json_file':ftmp, 'dict':iii, 'sort_keys':'yes'})
          if rx['return']>0: return rx

       r=ck.access(ii)
       if r['return']==0:
          x=r.get('html','')
          if x!='':
             st=r.get('style','')

             hg='<div id="ck_box_with_shadow" style="width:920px;">\n'
             if ftmp!='':
                hg+='<center><b>Note: graph info has been saved to file '+ftmp+' for interactive publications</b></center>'
             hg+=' <div id="ck_interactive" style="text-align:center">\n'
             hg+=x+'\n'
             hg+=' </div>\n'
             hg+='</div>\n'

    h=h.replace('$#graph#$', hg)

    return {'return':0, 'html':h, 'style':st}

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

    plat_uids={}
    pft=pi.get('features',{})
    for q in pft:
        if q.endswith('_uid'):
           plat_uids[q]=pft[q]

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

    ii['experiment_meta_extra']=plat_uids

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
