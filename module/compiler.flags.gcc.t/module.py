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
              pipeline
              frontier_keys
              experiment_uoa
              points1
              result1
              points2
              result2
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              report       - report to print or add to log
            }

    """

    pipeline=i.get('pipeline',{})
    fk=i.get('frontier_keys',[])
    euoa=i.get('experiment_uoa','')
    points1=i.get('points1',[])
    result1=i.get('result1',[])
    points2=i.get('points2',[])
    result2=i.get('result2',[])

    rp=''

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

          cdesc=pipeline.get('choices_desc',{})

          dv1=r1['flat'].get(kt,None)
          dv2=r2['flat'].get(kt,None)

          if dv1!=None and dv2!=None and dv2!=0:
             print dv1, dv2

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
