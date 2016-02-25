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
              (features)          - remote device features
              (features_uoa_list) - remote device features UOA list:
                                       * platform_uoa
                                       * platform_os_uoa
                                       * platform_cpu_uoa
                                       * platform_gpu_uoa
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
