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
              file_name - file name
              text      - text
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import os

    fn=i['file_name']
    txt=i.get('text','')

    r=ck.get_current_date_time({})
    if r['return']>0: return r

    s='======\n'+r['iso_datetime']+' ; '+txt

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


    return {'return':0}

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

    print ('explore program optimizations')

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

    return {'return':0, 'status':status 
           }

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

              (exchange_repo)              - which repo to record/update info (remote-ck by default)
              (exchange_subrepo)           - if remote, remote repo UOA

              (force_platform_name)        - if !='', use this for platform name

              (scenario)                   - module UOA of crowdsourcing scenario

              (program_tags)               - force selection of programs by tags

              (program_uoa)                - force program UOA
              (cmd_key)                    - CMD key
              (dataset_uoa)                - dataset UOA
              (dataset_file)               - dataset filename (if more than one inside one entry - suggest to have a UID in name)

            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import copy

    # Setting output
    o=i.get('out','')
    oo=''
    if o=='con': oo='con'

    # Params
    hos=i.get('host_os','')
    tos=i.get('target_os', '')
    tdid=i.get('device_id', '')

    exc='yes'
    se=i.get('skip_exchange','')
    if se=='yes': exc='no'

    er=i.get('exchange_repo','')
    esr=i.get('exchange_subrepo','')
    fpn=i.get('force_platform_name','')

    quiet=i.get('quiet','')

    scenario=i.get('crowdsourcing_scenario_uoa','')

    #**************************************************************************************************************
    # Welcome info
    if o=='con':
       ck.out(line)
       ck.out(welcome)

       if quiet!='yes':
          r=ck.inp({'text':'Press Enter to continue'})

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
                 'add_meta':'yes',
                 'scenario':scenario,
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

                       zux=z1.get('meta',{}).get('crowd_desc','')
                       if zux!='': zu=zux

                       zs=str(iz)
                       zz[zs]=z

                       ck.out(zs+') '+zu+' ('+z+')')

                       iz+=1

                   ck.out('')
                   rx=ck.inp({'text':'Select scenario UOA (or Enter to select 0): '})
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
          sdesc=ds.get('crowd_desc','')

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
              'program_tags':program_tags,
              'program_uoa':program_uoa,
              'cmd_key':cmd_key,
              'dataset_uoa':dataset_uoa,
              'dataset_file':dataset_file,
              'random':'yes',
              'skip_local':'yes',
              'generate_rnd_tmp_dir':'yes', # to be able to run crowdtuning in parallel on the same machine ...
              'prepare':'yes'}
          if quiet!='yes': ii['out']=oo
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

             if o=='con':
                ck.out(line)
                ck.out('Prepared experiment:')
                ck.out('')
                ck.out(' * Program:                  '+prog_uoa)
                ck.out(' * CMD:                      '+cmd_key)
                ck.out(' * Dataset:                  '+dataset_uoa)
                ck.out(' * Dataset file:             '+dataset_file)
                ck.out(' * Default compiler version: '+cver)

             # Saving pipeline
             pipeline_copy=copy.deepcopy(pipeline)





             # Run with default optimization




             # Run auto-tuning









          raw_input('xyz')


    return {'return':0}
