#
# Collective Knowledge (collective scenario: compiler flag tuning)
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
# crowtune compiler flags

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
