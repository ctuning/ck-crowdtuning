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
              (email)             - email or person UOA
              (platform_features) - remote device platform features
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import os
    from random import randint

    curdir=os.getcwd()

    # Setting output
    o=i.get('out','')
    oo=''
    if o=='con': oo='con'

    # Platform
    tos='android19-arm'
    tdid=''
    hos=''

    scenarios=cfg['scenarios']
    ls=len(scenarios)

    print (cfg['module_deps'])

    # Prepare platform info
    ii={'action':'detect',
        'module_uoa':cfg['module_deps']['platform.os'],
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

    ck.save_json_to_file({'json_file':'/tmp/xyz1.json','dict':pi})


    return {'return':1, 'error':'not completed'}
#    print (pi)
#    exit(1)



    # Try to generate at least one experimental pack!
    n=0
    nm=10

    success=False
    while n<nm and not success:
       n+=1

       # select scenario randomly
       scenario=scenarios[randint(0,ls-1)]

       ii={'action':'crowdsource',
           'module_uoa':scenario,
           'target_os':tos,
           'local':'yes',
           'quiet':'yes',
           'iterations':1,
           'once':'yes',
           'out':oo}
       r=ck.access(ii)
       if r['return']>0: return r
       if r['return']==0:
          success=True




    if not success:
       return {'return':1, 'error':'could not create any valid expeirmental pack for your mobile - possibly internal error! Please, contact authors'}





    # Prepare random pipeline

    import json
    print (json.dumps(sdeps, indent=2))
    exit(1)










    email=i.get('email','')
    ft=i.get('features','')
    if ft=='': ft={}

    # Logging
    r=ck.dumps_json({'dict':ft, 'skip_indent':'yes', 'sort_keys':'yes'})
    if r['return']>0: return r
    x=r['string']

    r=ck.access({'action':'log',
                 'module_uoa':cfg['module_deps']['program.optimization'],
                 'text':email+'\n'+x+'\n'})
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
