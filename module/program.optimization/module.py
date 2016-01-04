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

    s='======\n'+r['iso_datetime']+'\n'+txt

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
# crowdsource program optimization

def crowdsource(i):
    """
    Input:  {
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    print ('crowdsource program optimization')

    ck.out('')
    ck.out('Command line: ')
    ck.out('')

    import json
    cmd=json.dumps(i, indent=2)

    ck.out(cmd)

    return {'return':0}

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
                        'calibrate_time':5.0,
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
