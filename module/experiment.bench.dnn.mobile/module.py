#
# Collective Knowledge: crowdbenchmarking using ARM's workload automation and CK
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
rrepo='upload' # TBD - get from cfg

compiler_choices='#choices#compiler_flags#'

line='================================================================'

fsummary='summary.json'
fclassification='classification.json'
fgraph='tmp-reactions-graph.json'
ffstat='ck-stat-flat-characteristics.json'

form_name='wa_web_form'
onchange='document.'+form_name+'.submit();'

hextra='<i><center>\n'
hextra+='This is an on-going, community-driven project. Please see this <a href="https://play.google.com/store/apps/details?id=openscience.crowdsource.video.experiments&hl=fr">Android app</a>, long-term vision [ '
hextra+='<a href="http://arxiv.org/abs/1506.06256">CPC\'15</a>, \n'
hextra+='<a href="http://doi.acm.org/10.1145/2909437.2909449">IWOCL\'16</a>, \n'
hextra+='<a href="https://www.youtube.com/watch?v=Q94yWxXUMP0">YouTube</a>, \n'
hextra+='<a href="http://ctuning.org/cm/wiki/index.php?title=CM:data:45741e3fbcf4024b:1db78910464c9d05">wiki</a> ] '
hextra+=' and <a href="https://github.com/dividiti/ck-caffe">CK-Caffe GitHub repo</a>.'
hextra+='</center></i>\n'
hextra+='<br>\n'

selector=[{'name':'Scenario', 'key':'crowd_uid', 'module_uoa':'65477d547a49dd2c', 'module_key':'##dict#title'},
          {'name':'DNN engine', 'key':'engine'},
          {'name':'Model', 'key':'model'},
          {'name':'Platform', 'key':'plat_name','new_line':'yes'},
          {'name':'OS', 'key':'os_name'},
          {'name':'CPU', 'key':'cpu_name', 'new_line':'yes'},
          {'name':'CPU ABI', 'key':'cpu_abi'},
          {'name':'GPU', 'key':'gpu_name'}]

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
# show results

def show(i):
    """
    Input:  {
               (crowd_module_uoa) - if rendered from experiment crowdsourcing
               (crowd_key)        - add extra name to Web keys to avoid overlapping with original crowdsourcing HTML
               (crowd_on_change)  - reuse onchange doc from original crowdsourcing HTML

               (highlight_behavior_uid) - highlight specific result (behavior)!
               (highlight_by_user)      - highlight all results from a given user
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import os
    import copy

    st=''

    cmuoa=i.get('crowd_module_uoa','')
    ckey=i.get('crowd_key','')

    conc=i.get('crowd_on_change','')
    if conc=='':
        conc=onchange

    hi_uid=i.get('highlight_behavior_uid','')
    hi_user=i.get('highlight_by_user','')

    h='<hr>\n'
    h+='<center>\n'
    h+='\n\n<script language="JavaScript">function copyToClipboard (text) {window.prompt ("Copy to clipboard: Ctrl+C, Enter", text);}</script>\n\n' 

    h+=hextra

    # Check host URL prefix and default module/action
    rx=ck.access({'action':'form_url_prefix',
                  'module_uoa':'wfe',
                  'host':i.get('host',''), 
                  'port':i.get('port',''), 
                  'template':i.get('template','')})
    if rx['return']>0: return rx
    url0=rx['url']
    template=rx['template']

    url=url0
    action=i.get('action','')
    muoa=i.get('module_uoa','')

    st=''

    url+='action=index&module_uoa=wfe&native_action='+action+'&'+'native_module_uoa='+muoa
    url1=url

    # List entries
    ii={'action':'search',
        'module_uoa':work['self_module_uid'],
        'add_meta':'yes'}

    if cmuoa!='':
        ii['module_uoa']=cmuoa

    r=ck.access(ii)
    if r['return']>0: return r

    lst=r['lst']

    # Check unique entries
    choices={}
    mchoices={} # cache of UID -> alias choices
    wchoices={}

    cache_meta={}

    for q in lst:
        d=q['meta']
        meta=d.get('meta',{})

        # Process some derivatives
        scenario=meta.get('crowd_uid','')

        kscenario=cfg['module_deps']['experiment.scenario.mobile']+':'+scenario
        if kscenario not in cache_meta:
            r=ck.access({'action':'load',
                         'module_uoa':cfg['module_deps']['experiment.scenario.mobile'],
                         'data_uoa':scenario})
            if r['return']>0: return r
            xd=r['dict']

            # Find model size
            for q in xd.get('files',[]):
                if q.get('model_weights','')=='yes':
                    xd['model_weights_size']=int(q.get('file_size',0)/1E6)
                    break

            cache_meta[kscenario]=xd
        else:
            xd=cache_meta[kscenario]

        if meta.get('engine','')=='': meta['engine']=xd.get('engine','')
        if meta.get('model','')=='': meta['model']=xd.get('model','')

        meta['engine_meta']=xd.get('engine_meta',{})

        # Process selector meta
        for kk in selector:
            kx=kk['key']
            k=ckey+kx

            if k not in choices: 
                choices[k]=[]
                wchoices[k]=[{'name':'','value':''}]

            v=meta.get(kx,'')
            if v!='':

                if v not in choices[k]: 
                    choices[k].append(v)

                    muoa=kk.get('module_uoa','')
                    vv=v
                    if muoa!='':
                        if k not in mchoices:
                            mchoices[k]={}

                        vv=mchoices[k].get(v,'')
                        if vv=='':
                            r=ck.access({'action':'load',
                                         'module_uoa':muoa,
                                         'data_uoa':v})
                            if r['return']==0:
                                mk=kk.get('module_key','')
                                if mk=='': mk='##data_name'

                                rx=ck.get_by_flat_key({'dict':r, 'key':mk})
                                if rx['return']>0: return rx
                                vv=rx['value']

                        if vv=='' or vv==None: vv=v

                        mchoices[k][v]=vv

                    wchoices[k].append({'name':vv, 'value':v})

    # Prepare query div ***************************************************************
    if cmuoa=='':
        # Start form + URL (even when viewing entry)
        r=ck.access({'action':'start_form',
                     'module_uoa':cfg['module_deps']['wfe'],
                     'url':url1,
                     'name':form_name})
        if r['return']>0: return r
        h+=r['html']

    for kk in selector:
        k=ckey+kk['key']
        n=kk['name']

        nl=kk.get('new_line','')
        if nl=='yes':
            h+='<br>\n<div id="ck_entries_space8"></div>\n'

        v=''
        if i.get(k,'')!='':
            v=i[k]
            kk['value']=v

        # Show hardware
        ii={'action':'create_selector',
            'module_uoa':cfg['module_deps']['wfe'],
            'data':wchoices.get(k,[]),
            'name':k,
            'onchange':conc, 
            'skip_sort':'no',
            'selected_value':v}
        r=ck.access(ii)
        if r['return']>0: return r

        h+='<b>'+n+':</b> '+r['html'].strip()+'\n'

    # Check hidden
    if hi_uid!='':
        h+='<input type="hidden" name="highlight_behavior_uid" value="'+hi_uid+'">\n'

    if hi_user!='':
        h+='<input type="hidden" name="highlight_by_user" value="'+hi_user+'">\n'

    h+='<br><br>'

    # Prune list ******************************************************************
    plst=[]

    for q in lst:
        d=q['meta']
        meta=d.get('meta',{})

        # Check selector
        skip=False
        for kk in selector:
            k=kk['key']
            n=kk['name']
            v=kk.get('value','')

            if v!='' and meta.get(k,'')!=v:
                skip=True

        if not skip:
            # Process raw results
            arr=d.get('all_raw_results',[])

            for g in arr:
                nn=copy.deepcopy(q)

                ih=g.get('image_height',0)
                iw=g.get('image_width',0)

                it=0
                if ih!=0 and iw!=0:
                    it=ih*iw

                key=str(ih)+' x '+str(iw)

                prd=g.get('prediction','')
                if prd!='':
                    j1=prd.find('\n')
                    if j1>0:
                        j2=prd.find('\n',j1+1)
                        if j2>0:
                            prd=prd[j1:j2]

                # Check timing - currently temporal ugly hack
                t=g.get('time',[])

                tmin=0
                tmax=0

                if len(t)>0:
                    tmin=min(t)/1E3
                    tmax=max(t)/1E3

                nn['extra']={'key':key, 'raw_results':g, 'time_min':tmin, 'time_max':tmax, 'prediction':prd}

                # Check xOpenME timing
                xopenme=g.get('xopenme',{})
                xxopenme={}

                if type(xopenme)==dict:
                   for xk in xopenme:
                       t=xopenme[xk]

                       tmin=0
                       tmax=0

                       if len(t)>0:
                           tmin=min(t)
                           tmax=max(t)

                       xxopenme['xopenme_'+xk+'_min']=tmin
                       xxopenme['xopenme_'+xk+'_max']=tmax

                nn['extra'].update(xxopenme)

                plst.append(nn)

    # Check if too many
    lplst=len(plst)
    if lplst==0:
        h+='<b>No results found!</b>'
        return {'return':0, 'html':h, 'style':st}
    elif lplst>200:
        h+='<b>Too many entries to show ('+str(lplst)+') - please, prune list further!</b>'
        return {'return':0, 'html':h, 'style':st}

    # Prepare table
#    bgc='afffaf'
    bgc='dfffdf'
    bg=' style="background-color:#'+bgc+';"'
    bg1=' style="background-color:#bfffbf;"'
    bg2=' style="background-color:#afffaf;"'

    h+='<table border="1" cellpadding="7" cellspacing="0">\n'

    ha='align="center" valign="top"'
    hb='align="left" valign="top"'

    h+='  <tr style="background-color:#dddddd">\n'

    h+='   <td '+ha+'><b>#</b></td>\n'
    h+='   <td '+ha+'><b>Platform</b></td>\n'
    h+='   <td '+ha+'><b>Crowd scenario</b></td>\n'
    h+='   <td '+ha+'><b>Versions</b></td>\n'
    h+='   <td '+ha+'><b>Model weight size</b></td>\n'
    h+='   <td '+ha+'><b>Total time (min/max sec.)</b></td>\n'
    h+='   <td '+ha+'><b>Init network time (min/max sec.)</b></td>\n'
    h+='   <td '+ha+'><b>Image preparation (min/max sec.)</b></td>\n'
    h+='   <td '+ha+'><b>Classification time (min/max sec.)</b></td>\n'
    h+='   <td '+ha+'><b>Prediction probability</b></td>\n'
    h+='   <td '+ha+'><b>Energy</td>\n'
    h+='   <td '+ha+'><b><a href="https://github.com/dividiti/ck-caffe/blob/master/script/explore-accuracy/explore_accuracy.20160808.ipynb">Model accuracy on ImageNet</a></td>\n'
    h+='   <td '+ha+'><b>HW costs</td>\n'
    h+='   <td '+ha+'><b>Mispredictions and unexpected behavior</b></td>\n'
    h+='   <td '+ha+'><b>Image features</b></td>\n'
    h+='   <td '+ha+'><b>CPU</b></td>\n'
    h+='   <td '+ha+'><b>CPU ABI</b></td>\n'
    h+='   <td '+ha+'><b>GPU</b></td>\n'
    h+='   <td '+ha+'><b>OS</b></td>\n'
    h+='   <td '+ha+'><b>Data UID / Behavior UID</b></td>\n'
    h+='   <td '+ha+'><b>User</b></td>\n'
    h+='  <tr>\n'

    # Dictionary to hold target meta
    tm={}

    ix=0
    bgraph={'0':[]} # Just for graph demo
    if hi_uid!='' or hi_user!='':
        bgraph['1']=[]

    # Sort
    splst=sorted(plst, key=lambda x: x.get('extra',{}).get('time_min',0))

    for q in splst:
        ix+=1

        duid=q['data_uid']
        path=q['path']

        d=q['meta']

        meta=d.get('meta',{})

        extra=q['extra']
        img=extra.get('img',{})
        rres=extra.get('raw_results',{})

        mp=rres.get('mispredictions',[])

        key=extra.get('key','')

        buid=rres.get('behavior_uid','')
        pred=extra.get('prediction','').replace(' ','&nbsp;')
        user=rres.get('user','')

        tmin=extra.get('time_min',0)
        tmax=extra.get('time_max',0)

        scenario=meta.get('crowd_uid','')

        plat_name=meta.get('plat_name','')
        cpu_name=meta.get('cpu_name','')
        cpu_abi=meta.get('cpu_abi','')
        os_name=meta.get('os_name','')
        gpu_name=meta.get('gpu_name','')
        gpgpu_name=meta.get('gpgpu_name','')

        plat_uid=meta.get('platform_uid','')
        cpu_uid=meta.get('cpu_uid','')
        os_uid=meta.get('os_uid','')
        gpu_uid=meta.get('gpu_uid','')
        gpgpu_uid=meta.get('gpgpu_uid','')

        te=d.get('characteristics',{}).get('run',{})

        bgx=bg
        bgx1=bg1
        bgx2=bg2
        if (hi_uid!='' and buid==hi_uid) or (hi_user!='' and hi_user==user):
           bgx=' style="background-color:#ffcf7f"'
           bgx1=' style="background-color:#ffbf5f"'
           bgx2=' style="background-color:#ffaf2f"'

        # Starting raw
        h+='  <tr'+bgx+'>\n'

        h+='   <td '+ha+'>'+str(ix)+'</a></td>\n'

        x=plat_name
        if plat_uid!='':
            x='<a href="'+url0+'&wcid='+cfg['module_deps']['platform']+':'+plat_uid+'">'+x+'</a>'
        h+='   <td '+ha+'>'+x+'</td>\n'

        # Output scenario
        xx=mchoices.get(ckey+'crowd_uid',{}).get(scenario,'')

        kscenario=cfg['module_deps']['experiment.scenario.mobile']+':'+scenario
        xd=cache_meta[kscenario]

        xx=xd.get('title','')
        xy=int(xd.get('model_weights_size',0))+1

        h+='   <td '+ha+'><a href="'+url0+'&wcid='+kscenario+'">'+xx+'</a></td>\n'

        # Versions
        ver=''
        dver=meta.get('engine_meta',{}).get(cpu_abi,{})
        ver+='main: '+str(dver.get('program_version',''))+'\n'
        dps=dver.get('deps_versions',{})
        for dx in dps:
            ver+=dx+': '+str(dps[dx].get('version',''))+'\n'

        ver=ver.replace("\'","'").replace("'","\\'").replace('\"','"').replace('"',"\\'").replace('\n','\\n')
        if ver!='':
            ver='<input type="button" class="ck_small_button" onClick="alert(\''+ver+'\');" value="View">'
        h+='   <td '+ha+'>'+ver+'</td>\n'

        h+='   <td '+ha+'>'+str(xy)+' MB</td>\n'

        # Check relative time
        xx='<b>'+('%.3f'%tmin)+'</b>&nbsp;/&nbsp;'+('%.3f'%tmax)

        if tmin==0: xx+='<br><b><center>bug?</center></b>\n'

        if (hi_uid!='' and buid==hi_uid) or (hi_user!='' and hi_user==user):
            bgraph['0'].append([ix,None])
            bgraph['1'].append([ix,tmin])
        else:
            bgraph['0'].append([ix,tmin])
            if hi_uid!='' or hi_user!='': 
               bgraph['1'].append([ix,None])

        h+='   <td '+ha+' '+bgx1+'>'+xx+'</a></td>\n'

        for ixo in range(0,3):
           tmin=extra.get('xopenme_execution_time_kernel_'+str(ixo)+'_min',0)
           tmax=extra.get('xopenme_execution_time_kernel_'+str(ixo)+'_max',0)

           xx='<b>'+('%.3f'%tmin)+'</b>&nbsp;/&nbsp;'+('%.3f'%tmax)
           if tmin==0: xx+='<br><b><center>bug?</center></b>\n'

           h+='   <td '+ha+' '+bgx1+'>'+xx+'</a></td>\n'

        # Accuracy
        x=pred
        j=x.find('-')
        if j>0:
            x=x[:j-1].strip()
        h+='   <td '+ha+' '+bgx2+'>'+x+'</a></td>\n'

        # Energy TBD
        h+='   <td '+ha+'>-</a></td>\n'

        # Accuracy (take from model info)
        acc=xd.get('features',{}).get('accuracy','')
        acc5=xd.get('features',{}).get('accuracy_top5','')

        x=str(acc)
        if acc5!='':
           x+=' / '+str(acc5)

        if x=='': x='-'

        h+='   <td '+ha+'>'+x+'</a></td>\n'

        # Cost (take from platform meta)
        hc='-'
        if plat_uid!='':
           rh=ck.access({'action':'load',
                        'module_uoa':cfg['module_deps']['platform'],
                        'data_uoa':plat_uid})
           if rh['return']==0:
              hd=rh['dict']

              costs=hd.get('features',{}).get('cost',[])
              hc=''
              for c in costs:
                  if hc!='': hc+='<br>\n'
                  hc+='<b>'+str(c.get('price',''))+' '+c.get('currency','')+ '</b> - '+c.get('desc','')+' ('+c.get('date','')+')'

        h+='   <td '+ha+'>'+hc+'</a></td>\n'

        x=''
        for q in mp:
            ca=q.get('correct_answer','')
            mi=q.get('mispredicted_image','')
            mr=q.get('misprediction_results','')

            if mr!='':
                j1=mr.find('\n')
                if j1>0:
                    j2=mr.find('\n',j1+1)
                    if j2>0:
                        mr=mr[j1:j2]

            xx=ca
            if mi!='':
                y=work['self_module_uid']
                if cmuoa!='': y=cmuoa
                url=url0+'action=pull&common_action=yes&cid='+y+':'+duid+'&filename='+mi

                if ca=='': ca='<i>unknown</i>'
                xx='<a href="'+url+'">'+ca+'</a>'

            if x!='':
                x+='<hr>\n'

            x+='<strike>'+mr+'</strike><br>'+xx+'<br>\n'

        if tmin==0: x+='<br><b><center>Bug detected</center></b>\n'

        h+='   <td '+ha+'>'+x+'</td>\n'

        # All images
        h+='   <td '+ha+'>'+key.replace(' ','&nbsp;')+'</a></td>\n'

        # Extra info about platform

        x=cpu_name
        if cpu_uid!='':
            x='<a href="'+url0+'&wcid='+cfg['module_deps']['platform.cpu']+':'+cpu_uid+'">'+x+'</a>'
        h+='   <td '+ha+'>'+x+'</td>\n'

        h+='   <td '+ha+'>'+cpu_abi+'</td>\n'

        x=gpu_name
        if gpu_uid!='':
            x='<a href="'+url0+'&wcid='+cfg['module_deps']['platform.gpu']+':'+gpu_uid+'">'+x+'</a>'
        h+='   <td '+ha+'>'+x+'</td>\n'

        x=os_name
        if os_uid!='':
            x='<a href="'+url0+'&wcid='+cfg['module_deps']['platform']+':'+os_uid+'">'+x+'</a>'
        h+='   <td '+ha+'>'+x+'</td>\n'


        x=work['self_module_uid']
        if cmuoa!='': x=cmuoa
        h+='   <td '+ha+'><a href="'+url0+'&wcid='+x+':'+duid+'">'+duid+' '+buid+'</a></td>\n'

        h+='   <td '+ha+'><a href="'+url0+'&action=index&module_uoa=wfe&native_action=show&native_module_uoa=experiment.user">'+user+'</a></td>\n'

        h+='  <tr>\n'

    h+='</table>\n'
    h+='</center>\n'

    if cmuoa=='':
        h+='</form>\n'

    if len(bgraph['0'])>0:
       ii={'action':'plot',
           'module_uoa':cfg['module_deps']['graph'],

           "table":bgraph,

           "ymin":0,

           "ignore_point_if_none":"yes",

           "plot_type":"d3_2d_bars",

           "display_y_error_bar":"no",

           "title":"Powered by Collective Knowledge",

           "axis_x_desc":"Experiment",
           "axis_y_desc":"DNN image classification time (s)",

           "plot_grid":"yes",

           "d3_div":"ck_interactive",

           "image_width":"900",
           "image_height":"400",

           "wfe_url":url0}

       r=ck.access(ii)
       if r['return']==0:
          x=r.get('html','')
          if x!='':
             st+=r.get('style','')

             h+='<br>\n'
             h+='<center>\n'
             h+='<div id="ck_box_with_shadow" style="width:920px;">\n'
             h+=' <div id="ck_interactive" style="text-align:center">\n'
             h+=x+'\n'
             h+=' </div>\n'
             h+='</div>\n'
             h+='</center>\n'

    return {'return':0, 'html':h, 'style':st}

##############################################################################
# process raw results from mobile devices

def process(i):
    """
    Input:  {
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import copy

#    Debug
#    ck.save_json_to_file({'json_file':'/tmp/xyz1.json','dict':i})

    crowd_uid=i.get('crowd_uid','')
    email=i.get('email','')
    raw_results=i.get('raw_results',{})

    cfb=i.get('cpu_freqs_before',{})
    cfa=i.get('cpu_freqs_after',{})

    features=i.get('platform_features',{})

    fplat=features.get('platform',{})
    fos=features.get('os',{})
    fcpu=features.get('cpu',{})
    fgpu=features.get('gpu',{})

    plat_name=fplat.get('name','')
    plat_uid=features.get('platform_uid','')
    os_name=fos.get('name','')
    os_uid=features.get('os_uid','')
    gpu_uid=features.get('gpu_uid','')
    cpu_name=fcpu.get('name','')
    cpu_abi=fcpu.get('cpu_abi','')
    if cpu_name=='' and cpu_abi!='': 
        cpu_name='unknown-'+fcpu.get('cpu_abi','')
    cpu_uid=features.get('cpu_uid','')
    gpu_name=fgpu.get('name','')
    gpgpu_name=''
    gpgpu_uid=''
    sn=fos.get('serial_number','')

    # Prepare high-level experiment meta
    meta={'cpu_name':cpu_name,
          'cpu_abi':cpu_abi,
          'os_name':os_name,
          'plat_name':plat_name,
          'gpu_name':gpu_name,
          'gpgpu_name':gpgpu_name,
          'crowd_uid':crowd_uid}

    # Load scenario and update meta
    r=ck.access({'action':'load',
                 'module_uoa':cfg['module_deps']['experiment.scenario.mobile'],
                 'data_uoa':crowd_uid})
    if r['return']>0: return r
    xd=r['dict']

    meta['engine']=xd.get('engine','')
    meta['model']=xd.get('model','')

    mmeta=copy.deepcopy(meta)

    # Extra meta which is not used to search similar case ...
    mmeta['platform_uid']=plat_uid
    mmeta['os_uid']=os_uid
    mmeta['cpu_uid']=cpu_uid
    mmeta['gpu_uid']=gpu_uid
    mmeta['gpgpu_uid']=gpgpu_uid

    # Generate behavior UID
    rx=ck.gen_uid({})
    if rx['return']>0: return rx
    buid=rx['data_uid']

    raw_results['user']=email
    raw_results['behavior_uid']=buid

    # Check if already exists
    duid=''
    ddd={}

    ii={'action':'search',
        'module_uoa':work['self_module_uid'],
        'repo_uoa':rrepo,
        'search_dict':{'meta':meta},
        'add_meta':'yes'}
    rx=ck.access(ii)
    if rx['return']>0: return rx

    lst=rx['lst']

    if len(lst)==1:
        duid=lst[0]['data_uid']
        ddd=lst[0]['meta']
    else:
        rx=ck.gen_uid({})
        if rx['return']>0: return rx
        duid=rx['data_uid']

    # We keep time1,2,3 just for compatibility with the first beta version
    t=raw_results.get('time',[])
    tx=raw_results.get('time1',None)
    if tx!=None: t.append(tx)
    tx=raw_results.get('time2',None)
    if tx!=None: t.append(tx)
    tx=raw_results.get('time3',None)
    if tx!=None: t.append(tx)
    raw_results['time']=t

    # Check XOpenME
    xopenme={}

    yopenme=raw_results.get('xopenme',[])
    for xx in yopenme:
        for k in xx:
            v=xx[k]
            if k not in xopenme:
               xopenme[k]=[]
            if v!=None:
               xopenme[k].append(v)

    raw_results['xopenme']=xopenme

    # Record freq (not checking if changed at this stage)
    raw_results['cpu_freqs_before']=[cfb]
    raw_results['cpu_freqs_after']=[cfa]

    # Process freq before and freq after (for now no any intelligence)
    fb=raw_results

    # Process results
    results=ddd.get('all_raw_results',[])

    # Check if already exists with this image topology
    found=False
    for q in results:
        if (q.get('image_height',None)==raw_results.get('image_height',None) and \
           q.get('image_width',None)==raw_results.get('image_width',None)) or \
           (q.get('image_height',None)==raw_results.get('image_width',None) and \
           q.get('image_width',None)==raw_results.get('image_height',None)):
            t=q.get('time',[])

            for tx in raw_results.get('time',[]):
                t.append(tx)
            q['time']=t

            tkk1=raw_results.get('xopenme',{})
            tkk2=q.get('xopenme',{})

            for tk in tkk1:
                if tk not in tkk2: tkk2[tk]=[]
                for tx in tkk1[tk]:
                    if tx!=None: 
                       tkk2[tk].append(tx)

            q['xopenme']=tkk2

            fb=q.get('cpu_freqs_before',[])
            fb.append(cfb)
            q['cpu_freqs_before']=fb

            fa=q.get('cpu_freqs_after',[])
            fa.append(cfa)
            q['cpu_freqs_before']=fa

            buid=q.get('behavior_uid','')

            found=True

            break

    if not found:
        results.append(raw_results)

    ddd['all_raw_results']=results

    xmeta=ddd.get('meta',{})
    xmeta.update(mmeta)
    ddd['meta']=xmeta

    # Update meta
    rx=ck.access({'action':'update',
                  'module_uoa':work['self_module_uid'],
                  'data_uoa':duid,
                  'repo_uoa':rrepo,
                  'dict':ddd,
                  'substitute':'yes',
                  'sort_keys':'yes'})
    if rx['return']>0: return rx

    # Prepare url with results
    rx=ck.access({'action':'form_url_prefix',
                  'module_uoa':'wfe'})
    if rx['return']>0: return rx

    url=rx['url']+'&action=index&module_uoa=wfe&native_action=show&native_module_uoa=program.optimization&scenario='+work['self_module_uid']+'&highlight_behavior_uid='+buid

    return {'return':0, 'status':'Results successfully added to Collective Knowledge (UID='+duid+')!', 'data_uid':duid, 'behavior_uid':buid, 'result_url':url}

##############################################################################
# record unexpected behavior

def process_unexpected_behavior(i):
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

    duid=i.get('data_uid','')
    buid=i.get('behavior_uid','')
    cuid=i.get('crowd_uid','')
    rres=i.get('raw_results','')
    ca=i.get('correct_answer','')
    file_base64=i.get('file_base64','')

    # Find data
    r=ck.access({'action':'load',
                 'module_uoa':work['self_module_uid'],
                 'data_uoa':duid})
    if r['return']>0: return r
    d=r['dict']
    p=r['path']

    # Find behavior
    found=False
    arr=d.get('all_raw_results',[])
    for q in arr:
        if q.get('behavior_uid','')==buid:
            found=True
            break

    if not found:
        return {'return':1, 'error':'can\'t find behavior '+buid+' in entry '+duid}

    # Generate UID for the file with unexpected behavior
    rx=ck.gen_uid({})
    if rx['return']>0: return rx

    ff='misprediction-image-'+rx['data_uid']+'.jpg'

    pf=os.path.join(p,ff)

    mp=q.get('mispredictions',[])

    qq={}
    qq['misprediction_results']=rres
    qq['mispredicted_image']=ff
    qq['correct_answer']=ca

    mp.append(qq)

    q['mispredictions']=mp

    # Record file
    rx=ck.convert_upload_string_to_file({'file_content_base64':file_base64,
                                         'filename':pf})
    if rx['return']>0: return rx

    # Update entry (should add lock in the future for parallel processing)
    r=ck.access({'action':'update',
                 'module_uoa':work['self_module_uid'],
                 'data_uoa':duid,
                 'dict':d,
                 'sort_keys':'yes',
                 'substitute':'yes',
                 'ignore_update':'yes'})
    if r['return']>0: return r

    return {'return':0}
