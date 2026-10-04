#!/usr/bin/env python3
"""Validate/sample an ideal horizontal-fit perspective camera and box proxies."""
import argparse, itertools, json, math, re
from pathlib import Path

def finite(v):
    try:return isinstance(v,(int,float)) and not isinstance(v,bool) and math.isfinite(v)
    except OverflowError:return False

def vec(v):return isinstance(v,list) and len(v)==3 and all(finite(x) for x in v)
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def norm(a):return math.sqrt(dot(a,a))
def unit(a):return tuple(x/norm(a) for x in a)

def validate(p):
    errors=[]
    if not isinstance(p,dict):return ['spec must be object']
    if p.get('schema_version')!='camera-spatial-1.0':errors.append('schema_version must be camera-spatial-1.0')
    if not isinstance(p.get('project_id'),str) or not p['project_id'].strip():errors.append('project_id required')
    fps=p.get('fps')
    if not isinstance(fps,int) or isinstance(fps,bool) or fps<=0:errors.append('fps must be positive integer')
    r=p.get('resolution')
    if not isinstance(r,list) or len(r)!=2 or not all(isinstance(x,int) and not isinstance(x,bool) and x>0 for x in r):errors.append('resolution must be two positive integers')
    tables={}
    for kind in ['subjects','obstacles','shots']:
        rows=p.get(kind)
        if not isinstance(rows,list):errors.append(kind+' must be array');rows=[]
        tables[kind]={}
        for row in rows:
            if not isinstance(row,dict):errors.append(kind+' entry must be object');continue
            rid=row.get('id')
            if not isinstance(rid,str) or not rid.strip():errors.append(kind+' id required');continue
            if rid in tables[kind]:errors.append('duplicate '+rid)
            if kind=='shots' and not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*',rid):errors.append('shot id must use ASCII letters, digits, underscore or hyphen')
            tables[kind][rid]=row
    if not tables['shots']:errors.append('at least one shot required')
    if set(tables['subjects']) & set(tables['obstacles']):errors.append('subject and obstacle IDs must be distinct')
    for rid,row in {**tables['subjects'],**tables['obstacles']}.items():
        if not vec(row.get('position')):errors.append(rid+' position requires finite xyz')
        if not vec(row.get('size_m')) or any(x<=0 for x in row.get('size_m',[]) if finite(x)):errors.append(rid+' size_m requires positive xyz')
        if 'color_rgba' in row:
            c=row['color_rgba']
            if not isinstance(c,list) or len(c)!=4 or not all(finite(x) and 0<=x<=1 for x in c):errors.append(rid+' invalid RGBA')
    def keys(rows,n,label,camera=False):
        if not isinstance(rows,list) or not rows:errors.append(label+' keyframes required');return
        frames=[]
        for k in rows:
            if not isinstance(k,dict):errors.append(label+' key must be object');continue
            f=k.get('frame')
            if not isinstance(f,int) or isinstance(f,bool) or not 0<=f<n:errors.append(label+' invalid frame');continue
            frames.append(f)
            if not vec(k.get('position')):errors.append(label+' invalid position')
            if camera:
                if not vec(k.get('target')):errors.append(label+' invalid target')
                elif vec(k.get('position')):
                    d=sub(k['target'],k['position'])
                    if norm(d)<1e-6 or math.hypot(d[0],d[1])<1e-6:errors.append(label+' degenerate/up-parallel look direction')
                if 'lens_mm' in k and (not finite(k['lens_mm']) or k['lens_mm']<=0):errors.append(label+' invalid key lens')
        if frames!=sorted(set(frames)) or not frames or frames[0]!=0 or frames[-1]!=n-1:errors.append(label+' keys must be sorted unique and cover first/last frames')
    for rid,s in tables['shots'].items():
        for field in ['scene_id','purpose','motion_reason']:
            if not isinstance(s.get(field),str) or not s[field].strip():errors.append(rid+' '+field+' required')
        n=s.get('duration_frames')
        if not isinstance(n,int) or isinstance(n,bool) or n<=0:errors.append(rid+' invalid duration_frames');continue
        ids=s.get('subject_ids')
        if not isinstance(ids,list) or any(not isinstance(x,str) or x not in tables['subjects'] for x in ids):errors.append(rid+' invalid subject_ids')
        elif len(ids)!=len(set(ids)):errors.append(rid+' duplicate subject_ids')
        c=s.get('camera')
        if not isinstance(c,dict):errors.append(rid+' camera required');continue
        for field in ['sensor_width_mm','lens_mm','clip_start_m','clip_end_m']:
            if not finite(c.get(field)) or c[field]<=0:errors.append(rid+' positive '+field+' required')
        if finite(c.get('clip_start_m')) and finite(c.get('clip_end_m')) and c['clip_start_m']>=c['clip_end_m']:errors.append(rid+' invalid clip range')
        if not finite(c.get('roll_deg',0)):errors.append(rid+' roll_deg must be finite')
        if not finite(c.get('clearance_radius_m')) or c['clearance_radius_m']<0:errors.append(rid+' nonnegative clearance radius required')
        if c.get('interpolation') not in ['linear','smoothstep']:errors.append(rid+' invalid camera interpolation')
        keys(c.get('keyframes'),n,rid,True)
        tracks=s.get('subject_tracks',[])
        if not isinstance(tracks,list):errors.append(rid+' subject_tracks must be array');tracks=[]
        seen=set()
        for t in tracks:
            if not isinstance(t,dict):errors.append(rid+' track must be object');continue
            tid=t.get('subject_id')
            if not isinstance(tid,str) or tid not in tables['subjects']:errors.append(rid+' unknown track subject');continue
            if tid in seen:errors.append(rid+' duplicate subject track')
            seen.add(tid)
            if t.get('interpolation') not in ['linear','smoothstep']:errors.append(rid+' invalid track interpolation')
            keys(t.get('keyframes'),n,rid+'/'+tid)
        axis=s.get('axis')
        if axis is not None:
            if not isinstance(axis,dict):errors.append(rid+' axis must be object or null')
            else:
                for k in ['a_subject_id','b_subject_id']:
                    v=axis.get(k)
                    if not isinstance(v,str) or v not in tables['subjects']:errors.append(rid+' axis subject missing')
                if axis.get('a_subject_id')==axis.get('b_subject_id'):errors.append(rid+' axis needs two distinct subjects')
                if axis.get('allowed_side') not in ['positive','negative','either']:errors.append(rid+' invalid axis side')
    if errors:return errors
    # Interpolated look vectors can degenerate even when endpoint vectors are valid.
    for s in p['shots']:
        for f in range(s['duration_frames']):
            k=sample(s['camera']['keyframes'],f,s['camera']['interpolation'],s['camera']['lens_mm'])
            d=sub(k['target'],k['position'])
            if norm(d)<1e-6 or math.hypot(d[0],d[1])<1e-6:
                errors.append(f'{s["id"]} frame {f}: degenerate interpolated direction');break
    return errors

def sample(keys,frame,interpolation,default_lens=None):
    if len(keys)==1:a=b=keys[0];t=0
    else:
        a,b=keys[-2:];t=1
        for left,right in zip(keys,keys[1:]):
            if left['frame']<=frame<=right['frame']:
                a,b=left,right;t=(frame-a['frame'])/(b['frame']-a['frame']);break
    if interpolation=='smoothstep':t=t*t*(3-2*t)
    out={}
    for field in ['position','target']:
        if field in a:out[field]=[x+(y-x)*t for x,y in zip(a[field],b[field])]
    if default_lens is not None:
        la=a.get('lens_mm',default_lens);lb=b.get('lens_mm',default_lens);out['lens_mm']=la+(lb-la)*t
    return out

def subject_positions(p,s,f):
    result={x['id']:x['position'] for x in p['subjects']}
    for t in s.get('subject_tracks',[]):result[t['subject_id']]=sample(t['keyframes'],f,t['interpolation'])['position']
    return result

def project(point,camera,width,height,sensor_width,roll=0):
    forward=unit(sub(camera['target'],camera['position']))
    right=unit(cross(forward,(0,0,1)));up=cross(right,forward)
    angle=math.radians(roll)
    rolled_right=tuple(math.cos(angle)*r+math.sin(angle)*u for r,u in zip(right,up))
    rolled_up=tuple(-math.sin(angle)*r+math.cos(angle)*u for r,u in zip(right,up))
    d=sub(point,camera['position']);depth=dot(d,forward)
    if abs(depth)<1e-9:return [None,None,depth]
    scale=sensor_width/(2*camera['lens_mm'])
    return [.5+dot(d,rolled_right)/(2*depth*scale),.5+dot(d,rolled_up)/(2*depth*scale*height/width),depth]

def corners(pos,size):
    return [[pos[0]+x*size[0]/2,pos[1]+y*size[1]/2,pos[2]+z*size[2]] for x,y,z in itertools.product([-1,1],[-1,1],[0,1])]

def analyze(p):
    errors=validate(p)
    if errors:return {'valid':False,'errors':errors}
    subjects={x['id']:x for x in p['subjects']};reports=[]
    for s in p['shots']:
        c=s['camera'];samples=[];warnings=[];previous=None;previous_forward=None;previous_velocity=None
        for f in range(s['duration_frames']):
            cam=sample(c['keyframes'],f,c['interpolation'],c['lens_mm']);positions=subject_positions(p,s,f)
            velocity=[0,0,0] if previous is None else [v*p['fps'] for v in sub(cam['position'],previous)]
            speed=norm(velocity);acceleration=0 if previous_velocity is None else norm(sub(velocity,previous_velocity))*p['fps']
            direction=sub(cam['target'],cam['position']);forward=unit(direction)
            angular_speed=0 if previous_forward is None else math.degrees(math.acos(max(-1,min(1,dot(forward,previous_forward)))))*p['fps']
            previous=cam['position'];previous_forward=forward;previous_velocity=velocity
            record={'frame':f,'camera_position_m':cam['position'],'target_m':cam['target'],'lens_mm':cam['lens_mm'],'fov_x_deg':math.degrees(2*math.atan(c['sensor_width_mm']/(2*cam['lens_mm']))),'camera_speed_m_s':speed,'camera_acceleration_m_s2':acceleration,'look_angular_speed_deg_s':angular_speed,'camera_height_m':cam['position'][2],'yaw_deg':math.degrees(math.atan2(direction[1],direction[0])),'pitch_deg':math.degrees(math.atan2(direction[2],math.hypot(direction[0],direction[1]))),'roll_deg':c.get('roll_deg',0),'subjects':{},'pair_distances_m':{}}
            for aid,bid in itertools.combinations(s['subject_ids'],2):record['pair_distances_m'][aid+'/'+bid]=norm(sub(positions[aid],positions[bid]))
            for rid in s['subject_ids']:
                pos=positions[rid];size=subjects[rid]['size_m'];center=[pos[0],pos[1],pos[2]+size[2]/2]
                points=[project(v,cam,*p['resolution'],c['sensor_width_mm'],c.get('roll_deg',0)) for v in corners(pos,size)]
                finite_points=[v for v in points if v[0] is not None]
                bounds=[min(v[0] for v in finite_points),min(v[1] for v in finite_points),max(v[0] for v in finite_points),max(v[1] for v in finite_points)] if len(finite_points)==8 else None
                depth=project(center,cam,*p['resolution'],c['sensor_width_mm'],c.get('roll_deg',0))[2]
                flags=[]
                if any(v[2]<c['clip_start_m'] or v[2]>c['clip_end_m'] for v in points):flags.append('clip_or_behind')
                if bounds is None or bounds[0]<0 or bounds[1]<0 or bounds[2]>1 or bounds[3]>1:flags.append('proxy_cropped_or_offscreen')
                record['subjects'][rid]={'camera_to_center_m':norm(sub(center,cam['position'])),'optical_depth_m':depth,'bbox_ndc':bounds,'warnings':flags}
                for flag in flags:warnings.append({'frame':f,'subject_id':rid,'type':flag})
            axis=s.get('axis')
            if axis:
                a,b=positions[axis['a_subject_id']],positions[axis['b_subject_id']];v=sub(b,a);w=sub(cam['position'],a);signed=v[0]*w[1]-v[1]*w[0]
                side='neutral' if abs(signed)<1e-8 else ('positive' if signed>0 else 'negative');record['axis_side']=side
                if math.hypot(v[0],v[1])<1e-8:warnings.append({'frame':f,'type':'degenerate_subject_axis'})
                elif axis['allowed_side']!='either' and side!=axis['allowed_side']:warnings.append({'frame':f,'type':'axis_side_change','exception_reason':axis.get('exception_reason','')})
            radius=c['clearance_radius_m']
            if cam['position'][2]<radius:warnings.append({'frame':f,'type':'camera_ground_clearance'})
            bodies=[(o['id'],o['position'],o['size_m']) for o in p['obstacles']]+[(rid,positions[rid],subjects[rid]['size_m']) for rid in subjects]
            for rid,pos,size in bodies:
                low=[pos[0]-size[0]/2,pos[1]-size[1]/2,pos[2]];high=[pos[0]+size[0]/2,pos[1]+size[1]/2,pos[2]+size[2]]
                if all(low[i]-radius<=cam['position'][i]<=high[i]+radius for i in range(3)):warnings.append({'frame':f,'type':'camera_clearance_aabb_overlap','object_id':rid})
            samples.append(record)
        reports.append({'shot_id':s['id'],'duration_s':s['duration_frames']/p['fps'],'max_camera_speed_m_s':max(x['camera_speed_m_s'] for x in samples),'warnings':warnings,'samples':samples})
    return {'valid':True,'schema_version':p['schema_version'],'project_id':p['project_id'],'scope':'ideal pinhole, all integer frames, box proxies; no rendered or artistic validation','total_duration_s':sum(s['duration_frames'] for s in p['shots'])/p['fps'],'shots':reports}

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('spec');ap.add_argument('--out');args=ap.parse_args()
    try:result=analyze(json.loads(Path(args.spec).read_text(encoding='utf-8')))
    except (OSError,ValueError) as e:result={'valid':False,'errors':[str(e)]}
    data=json.dumps(result,ensure_ascii=False,indent=2)
    if args.out:Path(args.out).write_text(data+'\n',encoding='utf-8')
    else:print(data)
    return 0 if result['valid'] else 1
if __name__=='__main__':raise SystemExit(main())
