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
            " * http://cTuning.org/crowdsource-optimization\n" \
            "We would like to sincerely thank you for participating in this community effort" \
            " and help us optimize computer systems to accelerate knowledge discovery and boost innovation " \
            " in science and technology while making our planet greener!\n" \

form_name='ck_cresults_form'
fscenario='scenario'
onchange='document.'+form_name+'.submit();'

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
              (host_os)                    - host OS (detect, if omitted)
              (target_os)                  - OS module to check (if omitted, analyze host)
              (device_id)                  - device id if remote (such as adb)

              (quiet)                      - do not ask questions, but select random ...
              
              (skip_exchange)              - if 'yes', do not exchange platform info
                                            (development mode)

              (change_user)                - if yes', change user

              (local)                      - if 'yes', use local repo for exchange (local autotuning/benchmarking)
              (exchange_repo)              - which repo to record/update info (remote-ck by default)
              (exchange_subrepo)           - if remote, remote repo UOA

              (force_platform_name)        - if !='', use this for platform name

              (scenario)                   - module UOA of crowdsourcing scenario

              (program_tags)               - force selection of programs by tags

              (program_uoa)                - force program UOA
              (cmd_key)                    - CMD key
              (dataset_uoa)                - dataset UOA
              (dataset_file)               - dataset filename (if more than one inside one entry - suggest to have a UID in name)

              (iterations)                 - limit number of iterations, otherwise infinite (default=30)
                                             if -1, infinite (or until all choices are explored)

              (calibration_time)           - change calibration time (deafult 10 sec.)

              (objective)                  - extension to flat characteristics (min,max,exp) to tune on Pareto
                                             (default: min - to see what we can squeeze from a given architecture)

              (keep_tmp)                   - if 'yes', do not remove run batch
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import copy
    import os

    # Setting output
    o=i.get('out','')
    oo=''
    if o=='con': oo='con'

    curdir=os.getcwd()

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
    if er=='': er=ck.cfg['default_exchange_repo_uoa']
    esr=i.get('exchange_subrepo','')
    if esr=='': esr=ck.cfg['default_exchange_subrepo_uoa']

    if i.get('local','')=='yes': 
       er='local'
       esr=''

    fpn=i.get('force_platform_name','')

    quiet=i.get('quiet','')

    kt=i.get('keep_tmp','')

    scenario=i.get('crowdsourcing_scenario_uoa','')

    iterations=i.get('iterations','')
    if iterations=='': iterations=30

    cat=i.get('calibration_time','')
    if cat=='': cat=10.0
    
    objective=i.get('objective','')
    if objective=='': objective='min'

    #**************************************************************************************************************
    # Welcome info
    if o=='con' and quiet!='yes':
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
       ck.out('Info and results of crowdsourced experiments will be appeneded to a local log file: '+p)

       if quiet!='yes':
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
       ck.out('Testing public crowdsourcing server ...')
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

    #**************************************************************************************************************
    finish=False
    sit=0
    sdeps={}

    while not finish:
       sit+=1

       # Selecting scenario
       if o=='con':
          ck.out(line)
          ck.out('Scenario iteration: '+str(sit))

          if scenario=='':
             ck.out('')
             ck.out('Detecting available crowdsourcing scenarios ...')

             ii={'action':'search',
                 'module_uoa':cfg['module_deps']['module'],
                 'data_uoa':scenario,
                 'add_meta':'yes',
                 'add_info':'yes',
                 'tags':'program optimization, crowdsource'}
             r=ck.access(ii)
             if r['return']>0: return r

             lst=r['lst']

             if len(lst)==0:
                return {'return':1, 'error':'no local crowdsourcing scenarios related to program optimization found'}  
             elif len(lst)==1:
                scenario=lst[0].get('data_uid','')
             else:
                zss=sorted(lst, key=lambda v: (int(v.get('meta',{}).get('priority',0)), v['data_uoa']))

                if quiet=='yes':
                   scenario=zss[0]['data_uid']
                else:
                   ck.out('')
                   ck.out('More than one scenario found for program optimization:')
                   ck.out('')
                   zz={}
                   iz=0
                   for z1 in zss:
                       z=z1['data_uid']
                       zu=z1['data_uoa']

                       zux=z1.get('info',{}).get('data_name','')
                       if zux!='': zu=zux

                       zs=str(iz)
                       zz[zs]=z

                       ck.out(zs+') '+zu+' ('+z+')')

                       iz+=1

                   ck.out('')
                   rx=ck.inp({'text':'Select scenario number you want to participate in (or Enter to select 0): '})
                   x=rx['string'].strip()
                   if x=='': x='0'

                   if x not in zz:
                      return {'return':1, 'error':'scenario number is not recognized'}

                   scenario=zz[x]
             
          # Print selected scenario
          ii={'action':'load',
              'module_uoa':cfg['module_deps']['module'],
              'data_uoa':scenario}
          rs=ck.access(ii)
          if rs['return']>0: return rs
          ds=rs['dict']
          sdesc=rs.get('data_name','')

          if i.get('program_tags','')!='':
             program_tags=i['program_tags']
          else:
             program_tags=ds.get('program_tags','')

          program_uoa=i.get('program_uoa','')
          if program_uoa=='':
             program_uoa=i.get('data_uoa','')
          cmd_key=i.get('cmd_key','')
          dataset_uoa=i.get('dataset_uoa','')
          dataset_file=i.get('dataset_file','')

          ck.out('')
          ck.out('Experiment crowdsourcing scenario: '+sdesc) 

          #**************************************************************************************************************
          # Resolving needed deps for this scenario
          if len(sdeps)==0:
             sdeps=ds.get('deps',{})

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
                if quiet!='yes': ii['out']=oo
                rx=ck.access(ii)
                if rx['return']>0: return rx

                sdeps=rx['deps'] # Update deps (add UOA)












          #**************************************************************************************************************
          # Preparing pipeline with a temporary directory and random selection
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
              'random':'yes',
              'skip_local':'yes',
              'calibration_time':cat,
              'generate_rnd_tmp_dir':'yes', # to be able to run crowdtuning in parallel on the same machine ...
              'prepare':'yes',
              'out':oo}
          r=ck.access(ii)
          if r['return']>0: return r

          ready=r['ready']
          if ready!='yes':
             ck.out('WARNING: didn\'t manage to prepare program optimization workflow')
          else:
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
             
             lx=' * Program:                  '+prog_uoa+'\n' \
                ' * CMD:                      '+cmd_key+'\n' \
                ' * Dataset:                  '+dataset_uoa+'\n' \
                ' * Dataset file:             '+dataset_file+'\n' \
                ' * Default compiler version: '+cver+'\n' \

             if o=='con':
                ck.out(line)
                ck.out('Prepared experiment:')
                ck.out('')
                ck.out(lx)

             lx=' ===============================================================================\n' \
                ' * Crowdsourcing scenario:   '+sdesc+'\n' \
                ' * Number of iterations:     '+str(iterations)+'\n'+lx

             r=log({'file_name':cfg['log_file_own'], 'skip_header':'yes', 'text':lx})
             if r['return']>0: return r

             # Saving pipeline
             pipeline_copy=copy.deepcopy(pipeline)





             ################################################################################
             # Prepare tmp experiment entry
             r=ck.gen_uid({})
             if r['return']>0: return r
             euoa0=r['data_uid'] # Where to keep experiment

             # Run with default optimization
             if o=='con':
                ck.out(line)
                ck.out('Running first experiment with default optimization:')
                ck.out('')

             pipeline=copy.deepcopy(pipeline_copy)
             pup0=ds.get('experiment_0_pipeline_update',{})

             # Check (multi-objective) characteristics to process
             fk=ds.get('frontier_keys',[])

             # Update objective (min,max,exp) - if exp, need to add confidence interval
             #                                  otherwise we are not using points with high variation!          
             for l in range(0, len(fk)):
                  fk[l]=fk[l]+'#'+objective

             pup0['frontier_keys']=fk

             # Call CK
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

                 "tags":"crowdtuning,tmp",

                 'out':oo
                }

             r=ck.merge_dicts({'dict1':ii, 'dict2':pup0})
             if r['return']>0: return r
             ii=r['dict1']

             # Decide how to check characteristics 
             # (min, max, exp)

             r=ck.access(ii)
             if r['return']>0: return r

             lio=r['last_iteration_output']
             fail=lio.get('fail','')
             if fail=='yes':
                ck.out('')
                ck.out('WARNING: pipeline execution failed ('+lio.get('fail_reason','')+') ...')
                ck.out('         Will try another experiment ...')
             else:
                state=lio.get('state',{})
                repeat=state.get('repeat','')
                ftmp_dir=state.get('cur_dir','')

                ri=r['recorded_info']
                points1=ri.get('points',[])
                ruid=ri['recorded_uid']

                if len(points1)==0:
                   ck.out('')
                   ck.out('WARNING: explored points were not recorded (possibly internal error) ...')
                   ck.out('         Will try another experiment ...')
                else:
                   # Check if need to run extra experiments
                   # (for example when crowdsourcing program benchmarking or compiler bug detection,
                   #  no need to run extra experiments)

                   iii={'action':'get',
                        'module_uoa':cfg['module_deps']['experiment'],
                        'data_uoa':ruid,
                        'flat_keys_list':fk,
                        'load_json_files':['features_flat','flat','features']}

                   # Load default point info
                   r=ck.access(iii)
                   if r['return']>0: return r
                   result1=r.get('points',{})
                   result2={}
                   points2=[]

                   if ds.get('skip_experiment_1','')!='yes':
                      ################################################################################
                      # Prepare autotuning
                      pup1=ds.get('experiment_1_pipeline_update',{})
                      pup1['frontier_keys']=fk

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

                          "record":"yes",
                          "record_uoa":euoa0,

                          'out':oo
                         }

                      r=ck.merge_dicts({'dict1':ii, 'dict2':pup1})
                      if r['return']>0: return r
                      ii=r['dict1']

                      if 'pipeline_update' not in ii: ii['pipeline_update']={}
                      ii['pipeline_update']['repeat']=repeat

                      r=ck.access(ii)
                      if r['return']>0: return r

                      ri=r['recorded_info']
                      points2=ri['points']

                      # Load updated point info
                      r=ck.access(iii)
                      if r['return']>0: return r
                      result2=r.get('points',{})

                   ################################################################################
                   # Process results by scenario
                   ii={'action':'process',
                       'module_uoa':scenario,
                       'pipeline':pipeline_copy,
                       'experiment_uoa':ruid,
                       'frontier_keys':fk,
                       'points1':points1,
                       'result1':result1,
                       'points2':points2,
                       'result2':result2}
                   r=ck.access(ii)
                   if r['return']>0: return r
                   
                   report=r.get('report','')

                   if report!='':
                      r=log({'file_name':cfg['log_file_own'], 'skip_header':'yes', 'text':report})
                      if r['return']>0: return r

                      if o=='con':
                         ck.out(report)









                ################################################################################
                # Clean temporal directory and entry
                if kt!='yes':
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

#                   if o=='con':
#                      ck.out('')
#                      ck.out('Removing experiment entry '+euoa0+' ...')
#
#                   ii={'action':'rm',
#                       'module_uoa':cfg['module_deps']['experiment'],
#                       'data_uoa':euoa0,
#                       'force':'yes'}
#                   r=ck.access(ii)
                   # Skip return code

          raw_input('xyz')


    return {'return':0}

##############################################################################
# show results via web service

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
        'tags':'program optimization, crowdsource'}
    r=ck.access(ii)
    if r['return']>0: return r

    xls=r['lst']
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

    ii={'action':'create_selector',
        'module_uoa':cfg['module_deps']['wfe'],
        'data':dls,
        'name':fscenario,
        'onchange':onchange, 
        'skip_sort':'yes',
        'style':'width:400px;'}
    if scenario!='': ii['selected_value']=scenario
    r=ck.access(ii)
    if r['return']>0: return r
    h+='Select crowdsourcing scenario: '+r['html']

    h+='</center>\n'

    # Check scenario
    if scenario!='':
       h+='<p>\n'
       h+='<div id="ck_box_with_shadow">\n'


       h+='</div>\n'

    return {'return':0, 'html':h}
