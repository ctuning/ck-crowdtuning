#
# Collective Knowledge (compiler flags crowdtuning (crowdsource autotuning via spare computers such as mobile devices))
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
fsol='s-'

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
# Crowd-tune compiler flags

def crowdtune(i):
    """
    Input:  {
              (host_os)              - host OS (detect, if omitted)
              (target_os)            - OS module to check (if omitted, analyze host)
              (device_id)            - device id if remote (such as adb)
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import time
    import sys

    o=i.get('out','')

    start_time=time.time()

    sys.stdout.flush()

    sdi=i.get('skip_device_init','')
    sca=i.get('skip_clean_after','')


    ###############################################################################################################
    if o=='con':
       ck.out('Checking OS/arch parameters ...')

    # Check host/target OS/CPU
    hos=i.get('host_os','')
    tos=i.get('target_os','')
    tdid=i.get('device_id','')

    # Get some info about platforms
    ii={'action':'detect',
        'module_uoa':cfg['module_deps']['platform.os'],
        'host_os':hos,
        'target_os':tos,
        'device_id':tdid,
        'skip_device_init':sdi}
    r=ck.access(ii)
    if r['return']>0: return r

    hos=r['host_os_uid']
    hosx=r['host_os_uoa']
    hosd=r['host_os_dict']

    tos=r['os_uid']
    tosx=r['os_uoa']
    tosd=r['os_dict']

    bhos=hosd.get('base_uid','')
    if bhos=='': bhos=hos
    bhosx=hosd.get('base_uoa','')
    if bhosx=='': bhosx=hosx
    btos=tosd.get('base_uid','')
    if btos=='': btos=tos
    btosx=tosd.get('base_uoa','')
    if btosx=='': btosx=tosx


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
# process crowdtuning results

def process(i):
    """
    Input:  {
              platform_info
              pipeline
              frontier_keys
              experiment_uoa
              points1
              result1
              points2
              result2
              record_repo_uoa
              record_subrepo_uoa
              (iterations)
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              report       - report to print or add to log
            }

    """

    o=i.get('out','')
    oo=''
    if o=='con': oo='con'

    pif=i.get('platform_info',{}).get('features',{})
    pipeline=i.get('pipeline',{})
    fk=i.get('frontier_keys',[])
    euoa=i.get('experiment_uoa','')
    points1=i.get('points1',[])
    result1=i.get('result1',[])
    points2=i.get('points2',[])
    result2=i.get('result2',[])

    iterations=i.get('iterations','')

    rp='Better solution was not found ...'

    # Prepare meta
    plat_uid=pif.get('platform_uid','')
    plat_cpu_uid=pif.get('cpu_uid','')
    plat_os_uid=pif.get('os_uid','')
    plat_acc_uid=pif.get('acc_uid','')

    # Check if any older solution got updated
    new=False
    if len(points2)>0: # check that not empty at all
       for q in points1:
           if q not in points2:
              new=True
              break

    # Process solution
    if new:
       if len(result1)>0 and len(result2)>0 and len(fk)>0:
          kt=fk[0]

          r1=result1[0]
          r2=result2[0]

          behavior1=r1.get('flat',{})
          choices1=r1.get('features_flat',{})
          ft1=r1.get('features',{})
          behavior2=r2.get('flat',{})
          choices2=r2.get('features_flat',{})
          ft2=r2.get('features',{})

          cver=behavior1.get('##features#compiler_version#str#min','') # Compiler version

          cdesc=pipeline.get('choices_desc',{})

          dv1=r1['flat'].get(kt,None)
          dv2=r2['flat'].get(kt,None)

          if dv1!=None and dv2!=None and dv2!=0:
             speedup=dv1/dv2
          
             r=rebuild_cmd({'choices':choices1,
                            'choices_order':ft1.get('choices_order',[]),
                            'choices_desc':cdesc})
             if r['return']>0: return r

             pchoices1=r['pruned_choices'] # only flags
             cmd1=r['cmd']

             r=rebuild_cmd({'choices':choices2,
                            'choices_order':ft2.get('choices_order',[]),
                            'choices_desc':cdesc})
             if r['return']>0: return r

             pchoices2=r['pruned_choices'] # only flags
             cmd2=r['cmd']

             rp='\n' \
                '   Better solution FOUND (Speedup = '+('%.2f' % speedup)+')\n' \
                '    * Opt1:    '+cmd1+'\n' \
                '    * Opt2:    '+cmd2+'\n' \

             # Add new solution (possibly remotely)
             ruoa=i.get('record_repo_uoa','')
             rruoa=i.get('record_subrepo_uoa','')

             r=ck.access({'action':'add_solution',
                          'module_uoa':work['self_module_uoa'],
                          'repo_uoa': ruoa,
                          'data_uoa':cver,
                          'remote_repo_uoa': rruoa,
                          'iterations':iterations,
                          'speedup':speedup,
                          'pchoices1':pchoices1,
                          'cmd1':cmd1,
                          'pchoices2':pchoices2,
                          'cmd2':cmd2,
                          'choices':choices2,
                          'platform_features':pif,
                          'out':oo})
             if r['return']>0: return r

    return {'return':0, 'report':rp}

##############################################################################
# rebuild compiler cmd from choices

def rebuild_cmd(i):
    """
    Input:  {
               choices       - dict of choices
               choices_order - choices order
               choices_desc  - dict of choices desc
            }

    Output: {
              return         - return code =  0, if successful
                                           >  0, if error
              (error)        - error text if return > 0

              cmd            - compiler command line
              pruned_choices - leave only compiler flags
            }

    """

    cmd=''
    pc={}

    choices=i.get('choices',{})
    corder=i.get('choices_order',[])
    cdesc=i.get('choices_desc',{})

    for q in sorted(corder):
        if q.startswith('##'):
           q1='##choices'+q[1:]
           v=choices.get(q1, None)
           d=cdesc.get(q, None)

           if v!=None:
              if cmd!='': cmd+=' '
              cmd+=v

              pc[q1]=v

    return {'return':0, 'cmd':cmd, 'pruned_choices':pc}

##############################################################################
# add new solution

def add_solution(i):
    """
    Input:  {
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

    # Prepare everything here
    speedup=i.get('speedup','')
    pchoices1=i.get('pchoices1','')
    cmd1=i.get('cmd1','')
    pchoices2=i.get('pchoices2','')
    cmd2=i.get('cmd2','')
    choices=i.get('choices','')
    pif=i.get('platform_features',{})

    platform_name=pif.get('platform',{}).get('name','')
    os_name=pif.get('os',{}).get('name_short','')
    cpu_name=pif.get('cpu',{}).get('name','')
    acc_name=pif.get('acc',{}).get('name','')

    cpu_uid=pif.get('cpu_uid','')
    
    # Check if exists (with lock)
    ruoa=i.get('repo_uoa','')
    duoa=i.get('data_uoa','')

    if o=='con': 
       ck.out('  Searching solutions ('+duoa+') ...')

    ii={'action':'search',
        'common_func':'yes',
        'repo_uoa': ruoa,
        'module_uoa': work['self_module_uoa'],
        'data_uoa':duoa
       }
    r=ck.access(ii)
    if r['return']>0: return r
    rl=r['lst']

    if len(rl)==0:
       ii['action']='add'
       r=ck.access(ii)
       if r['return']>0: return r

    if o=='con': 
       ck.out('  Loading and locking entry ('+duoa+') ...')

    # Loading existing info and locking
    ii['action']='load'
    ii['get_lock']='yes'
    ii['lock_expire_time']=120
    r=ck.access(ii)
    if r['return']>0: return r
    duid=r['data_uid']

    p=r['path']
    lock_uid=r['lock_uid']

    d=r['dict']

    explored=d.get('explored_points','')
    if explored=='' or explored==None: explored=0
    explored=int(explored)

    iterations=i.get('iterations','')
    if iterations=='' or iterations==None: iterations=1

    explored+=int(iterations)

    d['explored_points']=explored

    # Check if dir for a CPU exists
    p1=os.path.join(p, cpu_uid)
    if not os.path.exists(p1):
       os.mkdir(p1)

    # For now generate unique solution (later reuse)
    r=ck.gen_uid({})
    if r['return']>0: return r
    suid=r['data_uid']

    sp=os.path.join(p1, fsol+suid+'.json')

    sd={}

    sd['features_flat']=choices
    sd['speedup']=speedup
    sd['choices1']=pchoices1
    sd['choices2']=pchoices2
    sd['cmd1']=cmd1
    sd['cmd2']=cmd2

    sd['misc_features']={}
    sd['misc_features']['platform_name']=platform_name
    sd['misc_features']['os_name']=os_name
    sd['misc_features']['cpu_name']=cpu_name
    sd['misc_features']['acc_name']=acc_name

    r=ck.save_json_to_file({'json_file':sp, 'dict':sd})
    if r['return']>0: return r

    # Updating and unlocking entry *****************************************************
    if o=='con': 
       ck.out('  Updating entry and unlocking ...')

    ii={'action':'update',
        'common_func':'yes',
        'repo_uoa': ruoa,
        'module_uoa': work['self_module_uoa'],
        'data_uoa':duid,
        'ignore_update':'yes',
        'sort_keys':'yes',
        'dict':d,
        'substitute':'yes',
        'unlock_uid':lock_uid
       }
    r=ck.access(ii)
    if r['return']>0: return r

    return {'return':0}

##############################################################################
# show results

def show(i):
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

    h='<table class="ck_table" border="0">\n'

    # Check host URL prefix and default module/action
    url0=ck.cfg.get('wfe_url_prefix','')

    h+=' <tr style="background-color:#cfcfff;">\n'
    h+='  <td><b>\n'
    h+='   #\n'
    h+='  </b></td>\n'
    h+='  <td><b>\n'
    h+='   <a href="'+url0+'wcid='+work['self_module_uoa']+':">CK UID</a>\n'
    h+='  </b></td>\n'
    h+='  <td><b>\n'
    h+='   Compiler\n'
    h+='  </b></td>\n'
    h+='  <td><b>\n'
    h+='   Version\n'
    h+='  </b></td>\n'
    h+='  <td><b>\n'
    h+='   Explorations\n'
    h+='  </b></td>\n'
    h+='  <td><b>\n'
    h+='   CPU\n'
    h+='  </b></td>\n'
    h+='  <td><b>\n'
    h+='   Speedup\n'
    h+='  </b></td>\n'
    h+='  <td><b>\n'
    h+='   Solution UID\n'
    h+='  </b></td>\n'
    h+='  <td><b>\n'
    h+='   Better flags\n'
    h+='  </b></td>\n'
    h+='  <td><b>\n'
    h+='   Default flags\n'
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
    ruoa=i.get('repo_uoa','')
    muoa=work['self_module_uid']
    duoa=i.get('data_uoa','')

    ii={'action':'search',
        'module_uoa':muoa,
        'repo_uoa':ruoa,
        'data_uoa':duoa,
        'add_meta':'yes'}
    r=ck.access(ii)
    if r['return']>0: return r

    lst=r['lst']

    ynum=''
    yduid=''
    ycomp=''
    ycver=''
    yexplored=''
    ycpu=''

    num=0
    for q in sorted(lst, key = lambda x: (x['data_uoa'])):

        num+=1

        duoa=q['data_uoa']
        duid=q['data_uid']

        p=q['path']

        meta=q['meta']
        ft=meta.get('features',{})

        comp='GCC'
        cver=duoa

        explored=meta.get('explored_points','')

        cpu=''
        platforms=''

        # List CPUs
        for cpu in os.listdir(p):
            p1=os.path.join(p,cpu)
            if os.path.isdir(p1) and cpu!=ck.cfg['subdir_ck_ext']:
               # List solutions
               for s in os.listdir(p1):
                   p2=os.path.join(p1,s)
                   if os.path.isfile(p2) and s.startswith(fsol) and s.endswith('.json'):
                      r=ck.load_json_file({'json_file':p2})
                      if r['return']>0: return r
                      d=r['dict']

                      suid=s[len(fsol):-5]

                      choices=d.get('features_flat',{})

                      program_uoa=choices.get('##choices#data_uoa','')
                      cmd=choices.get('##choices#cmd_key','')
                      dataset_uoa=choices.get('##choices#dataset_uoa','')
                      dataset_file=choices.get('##choices#dataset_file','')
                      target_os=choices.get('##choices#target_os','')

                      speedup=''
                      xspeedup=d.get('speedup','')
                      if xspeedup!='': speedup=('%.2f' % xspeedup)

                      cmd1=d.get('cmd1','')
                      cmd2=d.get('cmd2','')

                      h+=' <tr>\n'
                      h+='  <td valign="top">\n'
                      if str(num)!=ynum: 
                         ynum=str(num)
                         h+='   '+ynum+'\n'
                      h+='  </td>\n'

                      h+='  <td valign="top">\n'
                      if duid!=yduid:
                         yduid=duid
                         h+='   <a href="'+url0+'wcid='+work['self_module_uoa']+':'+yduid+'">'+yduid+'</a>\n'
                      h+='  </td>\n'

                      h+='  <td valign="top">\n'
                      if comp!=ycomp:
                         ycomp=comp
                         h+='   '+ycomp+'\n'
                      h+='  </td>\n'

                      h+='  <td valign="top">\n'
                      if cver!=ycver:
                         ycver=cver
                         h+='   '+ycver+'\n'
                      h+='  </td>\n'

                      h+='  <td valign="top">\n'
                      if str(explored)!=yexplored:
                         yexplored=str(explored)
                         h+='   '+yexplored+'\n'
                      h+='  </td>\n'

                      h+='  <td valign="top">\n'
                      if cpu!=ycpu:
                         ycpu=cpu
                         h+='   <a href="'+url0+'wcid='+cfg['module_deps']['platform.cpu']+':'+ycpu+'">'+ycpu+'</a>\n'
                      h+='  </td>\n'

                      h+='  <td valign="top">\n'
                      h+='   '+speedup+'\n'
                      h+='  </td>\n'

                      h+='  <td valign="top">\n'
                      h+='   '+suid+'\n'
                      h+='  </td>\n'

                      h+='  <td valign="top">\n'
                      h+='   '+cmd2+'\n'
                      h+='  </td>\n'

                      h+='  <td valign="top">\n'
                      h+='   '+cmd1+'\n'
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

    return {'return':0, 'html':h}
