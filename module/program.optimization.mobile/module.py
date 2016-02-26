#
# Collective Knowledge (collaborative program optimization using mobile devices (such as Android mobile phones and tables))
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
line='********************************************************************'

fpack='crowd-pack.zip'

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
# prepare experiments for crowdsourcing using mobile phones

def crowdsource(i):
    """
    Input:  {
              (crowd_uid)         - if !='', processing results and possibly chaining experiments

              (email)             - email or person UOA
              (platform_features) - remote device platform features

              (scenario)          - pre-set scenario
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import os
    from random import randint
    import copy
    import shutil
    import zipfile

    # Setting output
    o=i.get('out','')
    oo=''
    if o=='con': oo='con'

    rr={'return':0}

    email=i.get('email','')

    # Check if processing started experiments
    cuid=i.get('crowd_uid','')
    if cuid!='':
       #Log
       r=ck.access({'action':'log',
                    'module_uoa':cfg['module_deps']['experiment'],
                    'text':'Finishing crowd experiment: '+cuid+'\n'})
       if r['return']>0: return r








    else:
       # Initialize platform
       tos='android19-arm'
       tdid=''
       hos=''

       xscenario=i.get('scenario','')

       scenarios=cfg['scenarios']
       ls=len(scenarios)

       # Prepare platform info
       ii={'action':'detect',
           'module_uoa':cfg['module_deps']['platform.os'],
           'target_os':tos,
           'skip_info_collection':'yes',
           'out':oo}
       pi=ck.access(ii)
       if pi['return']>0: return pi
       del(pi['return'])

       # Merge with remote device platform features
       pf=i.get('platform_features',{})
       r=ck.merge_dicts({'dict1':pi['features'], 'dict2':pf})
       if r['return']>0: return r

       pf['features']=r['dict1']

       #Log
       r=ck.dumps_json({'dict':pf, 'skip_indent':'yes', 'sort_keys':'yes'})
       if r['return']>0: return r
       x=r['string']

       r=ck.access({'action':'log',
                    'module_uoa':cfg['module_deps']['experiment'],
                    'text':email+'\n'+x+'\n'})
       if r['return']>0: return r

       # Try to generate at least one experimental pack!
       n=0
       nm=10

       success=False
       while n<nm and not success:
          n+=1

          # select scenario randomly
          if xscenario!='': scenario=xscenario
          else:             scenario=scenarios[randint(0,ls-1)]

          pic=copy.deepcopy(pi)

          ii={'action':'crowdsource',
              'module_uoa':scenario,
              'target_os':tos,
              'local':'yes',
              'quiet':'yes',
              'iterations':1,
              'platform_info':pic,
              'once':'yes',
              'static':'yes',
#              'program_uoa':'*susan',
              'no_run':'yes',
              'keep_experiments':'yes',
              'new':'yes',
              'skip_pruning':'yes',
              'skip_info_collection':'yes',
              'out':oo}
          rrr=ck.access(ii)
          if rrr['return']>0:
             if o=='con':
                ck.out('')
                ck.out('WARNING: '+rrr['error'])
                ck.out('')
          else:
             # Prepare pack ...
             ri=rrr.get('recorded_info',{})
             ruid=ri.get('recorded_uid','')

             lio=rrr.get('last_iteration_output',{})
             fail=lio.get('fail','')
             if fail=='yes':
                if o=='con':
                   ck.out('')
                   ck.out('WARNING: Pipeline failed ('+lio.get('fail_reason','')+')')
                   ck.out('')

                # Delete failed experiment
                if ruid!='':
                   ii={'action':'delete',
                       'module_uoa':cfg['module_deps']['experiment'],
                       'data_uoa':ruid}
                   r=ck.access(ii)
                   # ignore output

             else:
                # Prepare pack
                d={'experiment_uoa':ruid}

                ii={'action':'add',
                    'module_uoa':work['self_module_uid'],
                    'dict':d}
                r=ck.access(ii)
                if r['return']>0: return r

                p=r['path']

                cuid=r['data_uid'] # crowd experiment identifier
                rr['crowd_uid']=cuid

                rr['desc']=rrr.get('scenario_desc','')
                rr['desc1']=rrr.get('subscenario_desc','')

                if o=='con':
                   ck.out('')
                   ck.out('  Crowd UID: '+cuid)

                # Copying binaries and inputs here
                sd=lio.get('state',{})
                ptmp=sd.get('cur_dir','')

                target_exe_0=rrr.get('original_target_exe','')
                target_exe_1=lio.get('state',{}).get('target_exe','')

                if ptmp!='' and target_exe_0!='' and target_exe_1!='':
                   te0=os.path.join(ptmp, target_exe_0)
                   te1=os.path.join(ptmp, target_exe_1)

                   nte0=os.path.join(p, target_exe_0)
                   nte1=os.path.join(p, target_exe_1)

                   # Copying binary files
                   copied=True
                   try:
                      shutil.copyfile(te0, nte0)
                      shutil.copyfile(te1, nte1)
                   except Exception as e: 
                      copied=False
                      pass

                   if copied:
                      # Check dataset files
                      ed=rrr.get('experiment_desc',{})
                      choices=ed.get('choices',{})

                      duoa=choices.get('dataset_uoa','')
                      dfile=choices.get('dataset_file','')

                      rr['choices']=choices

                      copied=True
                      if duoa!='' and dfile!='':
                         r=ck.access({'action':'load',
                                      'module_uoa':cfg['module_deps']['dataset'],
                                      'data_uoa':duoa})
                         if r['return']>0: return r

                         pd=r['path']

                         td=os.path.join(pd, dfile)
                         ntd=os.path.join(p, dfile)

                         copied=True
                         try:
                            shutil.copyfile(td, ntd)
                         except Exception as e: 
                            copied=False
                            pass

                      if copied:
                         # Prepare archive
                         zip_method=zipfile.ZIP_DEFLATED

                         gaf=i.get('all','')

                         fl={}

                         r=ck.list_all_files({'path':p})
                         if r['return']>0: return r

                         flx=r['list']

                         for k in flx:
                             fl[k]=flx[k]

                         pfn=os.path.join(p, fpack)

                         # Write archive
                         copied=True
                         try:
                            f=open(pfn, 'wb')
                            z=zipfile.ZipFile(f, 'w', zip_method)
                            for fn in fl:
                                p1=os.path.join(p, fn)
                                z.write(p1, fn, zip_method)
                            z.close()
                            f.close()

                         except Exception as e:
                            copied=False

                         if copied:
                            # preparing zip file
                            size=os.path.getsize(pfn) 

                            r=ck.convert_file_to_upload_string({'filename':pfn})
                            if r['return']>0: return r

                            fx=r['file_content_base64']

                            #MD5
                            import hashlib
                            md5=hashlib.md5(fx.encode()).hexdigest()

                            # create cmd
                            prog_uoa=choices.get('data_uoa','')
                            cmd_key=choices.get('cmd_key','')
                            r=ck.access({'action':'load',
                                         'module_uoa':cfg['module_deps']['program'],
                                         'data_uoa':prog_uoa})
                            if r['return']>0: return r
                            dd=r['dict']

                            rcm=dd.get('run_cmds','').get(cmd_key,{}).get('run_time',{}).get('run_cmd_main','')
                            rcm=rcm.replace('$#BIN_FILE#$ ','')
                            rcm=rcm.replace('$#dataset_path#$','')
                            rcm=rcm.replace('$#dataset_filename#$',dfile)

                            if rcm.find('$#')>=0 and rcm.find('#$')>=0:
                               success=False

                            if success:
                               calibrate='no'
                               if dd.get('run_vars',{}).get('CT_REPEAT_MAIN','')!='':
                                  calibrate='yes'

                               # finalize info
                               rr['file_content_base64']=fx
                               rr['size']=size 
                               rr['md5sum']=md5
                               rr['run_cmd_main']=rcm
                               rr['bin_file0']=target_exe_0
                               rr['bin_file1']=target_exe_1
                               rr['calibrate']=calibrate
                               rr['calibrate_max_iters']=10
                               rr['calibrate_time']=10.0
                               rr['repeat']=5
                               rr['ct_repeat']=1

                               success=True

                if not success:
                   if o=='con':
                      ck.out('')
                      ck.out('WARNING: some files are missing - removing crowd entry ('+cuid+') ...')
                   
                   ii={'action':'rm',
                       'module_uoa':work['self_module_uid'],
                       'data_uoa':cuid}
                   r=ck.access(ii)
                   if r['return']>0: return r

       if not success:
          rr={'return':1, 'error':'could not create any valid expeirmental pack for your mobile - possibly internal error! Please, contact authors'}

    return rr
