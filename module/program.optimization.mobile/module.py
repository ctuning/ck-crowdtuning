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
max_size_pack=1200000

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
    import json

    # Setting output
    o=i.get('out','')
    oo=''
    if o=='con': oo='con'

    rr={'return':0}

    email=i.get('email','')

    ruoa=i.get('record_repo_uoa','')
#    if ruoa=='': ruoa='upload'
    # Hack
    ck.cfg["forbid_writing_to_local_repo"]="no"
    ck.cfg["allow_writing_only_to_allowed"]="no"
    ck.cfg["forbid_global_delete"]="no"
#    ck.cfg["allow_run_only_from_allowed_repos"]="yes"

    # Check if processing started experiments
    cuid=i.get('crowd_uid','')
    if cuid!='':
       ###################################################################################################################
       # Load info
       r=ck.access({'action':'load',
                    'module_uoa':work['self_module_uid'],
                    'data_uoa':cuid})
       if r['return']>0: return r
       d=r['dict']

       euoa=d['experiment_uoa']
       ol=d['off_line']

       suid=ol.get('solution_uid','') # should normally be prepared in advance!

       scenario_uoa=ol['scenario_module_uoa']
       condition_objective='#'+ol['meta']['objective']

       xstatus=''

       results=i.get('results',{})

       #Log
       r=ck.access({'action':'log',
                    'module_uoa':cfg['module_deps']['experiment'],
                    'text':'Finishing crowd experiment: '+cuid+' ('+email+')\n'+json.dumps(results,indent=2,sort_keys=True)+'\n'})
       if r['return']>0: return r

       if len(results)>0:

          repeat=results.get('ct_repeat','')
          if repeat=='': repeat=1

          cpu_freq0=results.get('cpu_freq0',{})
          cpu_freq1=results.get('cpu_freq1',{})

          ch0=results.get('characteristics0',{})
          ch1=results.get('characteristics1',{})

          # TBD: improve stat analysis -> use CK module (here quick prototyping)
          fch0min=-1
          fch0max=-1
          for q in ch0:
              v=ch0[q]
              if fch0min==-1 or v<fch0min:
                 fch0min=v
              if fch0max==-1 or v>fch0max:
                 fch0max=v

          var=(fch0max-fch0min)/fch0min

          fch1min=-1
          fch1max=-1
          for q in ch1:
              v=ch1[q]
              if fch1min==-1 or v<fch1min:
                 fch1min=v
              if fch1max==-1 or v>fch1max:
                 fch1max=v

          impr=0.0
          if fch1min!=0: impr=fch0min/fch1min

          ol["meta_extra"]["cpu_cur_freq"]=cpu_freq1

          sol=ol["solutions"][0]
          sol["extra_meta"]["cpu_cur_freq"]=cpu_freq1

          point=sol["points"][0]

          point["characteristics"]["##characteristics#run#execution_time_kernel_0#min"]=fch0min
          point["characteristics"]["##characteristics#run#repeat#min"]=repeat

          point["improvements"]["##characteristics#run#execution_time_kernel_0#min_imp"]=impr

#          Hack: don't write for now, otherwise most of the time ignored ...
          var=-1
          point["misc"]["##characteristics#run#execution_time_kernel_0#range_percent"]=var

          sol["points"][0]=point
          ol["solutions"][0]=sol

          # Get conditions from a scenario
          r=ck.access({'action':'load',
                       'module_uoa':cfg['module_deps']['module'],
                       'data_uoa':scenario_uoa})
          if r['return']>0: return r
          ds=r['dict']

          scon=ds.get('solution_conditions',[])
          if len(scon)>0:
             con=copy.deepcopy(point["characteristics"])
             con.update(point["improvements"])
             con.update(point["misc"])
             # Hack
             con["##characteristics#compile#md5_sum#min_imp"]=0

             ii={'action':'check',
                 'module_uoa':cfg['module_deps']['math.conditions'],
                 'new_points':['0'],
                 'results':[{'point_uid':'0', 'flat':con}],
                 'conditions':scon,
                 'middle_key':condition_objective,
                 'out':oo}
             ry=ck.access(ii)
             if ry['return']>0: return ry 

             xdpoints=ry['points_to_delete']
             if len(xdpoints)>0:
                xstatus='*** Your explored solution is not better than existing ones (conditions are not met) ***\n' 
                if o=='con':
                   ck.out('')
                   ck.out('    WARNING: conditions on characteristics were not met!')
             else:
                # Submitting solution
                ii=copy.deepcopy(ol)
                ii['action']='add_solution'
                ii['module_uoa']=cfg['module_deps']['program.optimization']
                ii['repo_uoa']='upload' # Hack 
                ii['user']=email
                rx=ck.access(ii)
                if rx['return']>0: return rx

                if rx.get('recorded','')=='yes':
                   ri=rx.get('recorded_info',{})
                   xstatus=ri.get('status','')
                   xlog=ri.get('log','')

                   rz=ck.access({'action':'log',
                                 'module_uoa':cfg['module_deps']['experiment'],
                                 'file_name':cfg['log_file_results'],
                                 'text':xlog})
                   if rz['return']>0: return rz

                else:
                   xstatus='*** Your explored solution is not better than existing ones ***\n' 

             r=ck.access({'action':'log',
                          'module_uoa':cfg['module_deps']['experiment'],
                          'text':'Result of crowd experiment (UID='+suid+') : '+cuid+' ('+email+'): '+xstatus+'\n'})
             if r['return']>0: return r


       # Cleaning experiment entry
       r=ck.access({'action':'delete',
                    'module_uoa':cfg['module_deps']['experiment'],
                    'data_uoa':euoa})
       if r['return']>0: return r

       # Cleaning crowd entry
       r=ck.access({'action':'delete',
                    'module_uoa':work['self_module_uid'],
                    'data_uoa':cuid})
       if r['return']>0: return r

       # Finishing
       status='Crowdsourced results from your mobile device were successfully processed by Collective Knowledge Aggregator!\n\n'+xstatus

       if o=='con':
          ck.out('')
          ck.out(status)

       rr['status']=status

    else:
       ###################################################################################################################
       # Initialize platform
       pf=i.get('platform_features',{})

       cpu_abi=pf.get('cpu',{}).get('cpu_abi','')
       os_bits=pf.get('os',{}).get('bits','')

       tos=''
       if cpu_abi.startswith('armeabi-'):
          tos='android19-arm'
#       elif cpu_abi=='x86':
#          tos='android19-x86'
#          if os_bits=='64':
#             tos='android21-x86_64'

       if tos=='':
          return {'return':1, 'error':'ABI of your mobile device is not yet supported for crowdtuning ('+cpu_abi+') - please contact authors to check if it\'s in development'}

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
       nm=20

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
              'skip_collaborative':'yes',
              'parametric_flags':'yes',
#              'static':'yes',
#              'program_uoa':'*susan',
              'any_flag_tags':'arm-specific',
#              'cmd_key':'edges',
#              'dataset_uoa':'image-pgm-0001',
              'extra_dataset_tags':['small'],
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
                ol=rrr['off_line']
                ed=rrr.get('experiment_desc',{})
                choices=ed.get('choices',{})

                d={'experiment_uoa':ruid,
                   'off_line':ol}

                ii={'action':'add',
                    'module_uoa':work['self_module_uid'],
                    'repo_uoa':ruoa,
                    'dict':d}
                r=ck.access(ii)
                if r['return']>0: return r

                p=r['path']

                cuid=r['data_uid'] # crowd experiment identifier
                rr['crowd_uid']=cuid

                x=lio.get('characteristics',{}).get('compile',{}).get('joined_compiler_flags','')

                dsc='Scenario: '+rrr.get('scenario_desc','')+'\n'
                dsc+='Sub-scenario: '+rrr.get('subscenario_desc','')+'\n'
                dsc+='Benchmark/codelet: '+choices.get('data_uoa','')+'\n'
                dsc+='CMD key: '+choices.get('cmd_key','')+'\n'
                dsc+='Dataset: '+choices.get('dataset_uoa','')+'\n'
                dsc+='Dataset file: '+choices.get('dataset_file','')+'\n'
                dsc+='Optimizations:\n'
                dsc+='* OpenCl tuning: not used\n'
                dsc+='* Compiler description: '+choices.get('compiler_description_uoa','')+'\n'
                dsc+='* Compiler flags: -O3 vs '+x+'\n'

                rr['desc']=dsc

                deps=lio.get('dependencies',{})
                for kdp in deps:
                    dp=deps[kdp]
                    z=dp.get('cus',{})
                    dl=z.get('dynamic_lib','')
                    pl=z.get('path_lib','')

                    if dl!='' and pl!='':
                       pidl=os.path.join(pl, dl)
                       if os.path.isfile(pidl):
                          pidl1=os.path.join(p, dl)
                          try:
                             shutil.copyfile(pidl, pidl1)
                          except Exception as e: 
                             pass

                if o=='con':
                   ck.out('')
                   ck.out('  Crowd UID: '+cuid)

                # Copying binaries and inputs here
                target_exe_0=rrr.get('original_target_exe','')
                target_path_0=rrr.get('original_path_exe','')
                target_exe_1=lio.get('state',{}).get('target_exe','')
                tp1=rrr.get('new_path_exe','')

                tp0=os.path.dirname(target_path_0)
                target_path_1=os.path.join(tp0,tp1)

                if o=='con':
                   ck.out('')
                   ck.out('Copying executables:')
                   ck.out(' * '+target_path_0+'  /  '+target_exe_0)
                   ck.out(' * '+target_path_1+'  /  '+target_exe_1)
                   ck.out('')

                duoa=choices.get('dataset_uoa','')
                dfile=choices.get('dataset_file','')

                # create cmd
                prog_uoa=choices.get('data_uoa','')
                cmd_key=choices.get('cmd_key','')
                r=ck.access({'action':'load',
                             'module_uoa':cfg['module_deps']['program'],
                             'data_uoa':prog_uoa})
                if r['return']>0: return r
                dd=r['dict']
                pp=r['path']

                rcm=dd.get('run_cmds','').get(cmd_key,{}).get('run_time',{}).get('run_cmd_main','')
                rcm=rcm.replace('$#BIN_FILE#$ ','')
                rcm=rcm.replace('$#dataset_path#$','')
                rcm=rcm.replace('$#dataset_filename#$',dfile)
                rcm=rcm.replace('$#src_path#$','')

                rif=dd.get('run_cmds','').get(cmd_key,{}).get('run_time',{}).get('run_input_files',[])

                if o=='con':
                   ck.out('Cmd: '+rcm)

                if target_path_0!='' and target_path_1!='' and target_exe_0!='' and target_exe_1!='' and \
                   not (rcm.find('$#')>=0 or rcm.find('#$')>=0 or rcm.find('<')>=0):

                   te0=os.path.join(target_path_0, target_exe_0)
                   te1=os.path.join(target_path_1, target_exe_1)

                   nte0=os.path.join(p, target_exe_0)
                   nte1=os.path.join(p, target_exe_1)

                   # Copying binary files
                   copied=True
                   try:
                      shutil.copyfile(te0, nte0)
                      shutil.copyfile(te1, nte1)

                      for inp in rif:
                          px1=os.path.join(pp, inp)
                          px2=os.path.join(p, inp)
                          shutil.copyfile(px1, px2)

                   except Exception as e: 
                      copied=False
                      pass

                   if copied:
                      # clean dirs
                      try:
                         shutil.rmtree(target_path_0, ignore_errors=True)
                         shutil.rmtree(target_path_1, ignore_errors=True)
                      except Exception as e: 
                         if o=='con':
                            ck.out('')
                            ck.out('WARNING: can\'t fully erase tmp dir')
                            ck.out('')
                         pass

                      if o=='con':
                         ck.out('Copying datasets ...')

                      # Check dataset files
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
                         if o=='con':
                            ck.out('Preparing zip ...')

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
                            if o=='con':
                               ck.out('Preparing cmd ...')

                            size=os.path.getsize(pfn) 

                            r=ck.convert_file_to_upload_string({'filename':pfn})
                            if r['return']>0: return r

                            fx=r['file_content_base64']

                            #MD5
                            import hashlib
                            md5=hashlib.md5(fx.encode()).hexdigest()

                            if o=='con':
                               ck.out('Finalizing ...')

                            calibrate='no'
                            if dd.get('run_vars',{}).get('CT_REPEAT_MAIN','')!='':
                               calibrate='yes'

                            if len(fx)>max_size_pack:
                               if o=='con':
                                  ck.out('')
                                  ck.out('WARNING: pack is too large ('+str(len(fx))+')')
                                  ck.out('')
                            
                            else:
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
