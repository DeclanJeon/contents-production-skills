#!/usr/bin/env python3
"""Top-down blocking diagram and facing helpers for Blender proxy previs.

Pure standard-library module: it never imports bpy, so the same code produces
the shot diagram, the facing vectors and the silhouette sampling grid with or
without a Blender runtime. Everything is derived from a camera-spatial-1.0
spec; the SVG is a diagram, not a render, and proves no occlusion, contact or
performance.
"""
import json,math,sys
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'camera-spatial-design'/'scripts'))
from spatial_spec import sample,subject_positions

DIAGRAM_NOTE='spec-derived diagram: camera path, subject travel and facing only; no occlusion, contact, lighting or performance verification'
MIN_FACING_MOVE_M=0.01


def parse_facing_map(text):
    """Normalize a facing map to {shot_id:{subject_id:{'vector':[x,y]}}}.

    Shape: {"SH01": {"CH01": [0.0, 1.0]}}. Vectors are world XY headings and
    are unit-normalized here so callers never re-derive the length. Facing is
    an adapter-local input: camera-spatial-1.0 carries no facing field, so
    this never widens the versioned schema.
    """
    errors=[];out={}
    try:data=json.loads(text)
    except ValueError as e:return None,['invalid JSON: '+str(e)]
    if not isinstance(data,dict):return None,['facing map must be an object of shot ids']
    for shot,subjects in data.items():
        if not isinstance(subjects,dict):errors.append(f'{shot}: facing entry must be an object of subject ids');continue
        for subject,row in subjects.items():
            vector=row.get('vector') if isinstance(row,dict) else row
            if not isinstance(vector,list) or len(vector)!=2:
                errors.append(f'{shot}.{subject}: facing must be a two-number [x, y] vector');continue
            if not all(isinstance(v,(int,float)) and not isinstance(v,bool) and math.isfinite(v) for v in vector):
                errors.append(f'{shot}.{subject}: facing vector must be finite numbers');continue
            x,y=float(vector[0]),float(vector[1]);length=math.hypot(x,y)
            if length<1e-6:errors.append(f'{shot}.{subject}: facing vector must not be zero');continue
            out.setdefault(shot,{})[subject]={'vector':[x/length,y/length]}
    if not out and not errors:errors.append('facing map selects no subjects')
    return out,errors


def _position(spec,shot,frame,subject_id):
    """Subject position at a clamped local frame, or None when it has no track."""
    if subject_id not in shot.get('subject_ids',[]):return None
    n=shot.get('duration_frames')
    if not isinstance(n,int):return None
    f=max(0,min(n-1,frame))
    return subject_positions(spec,shot,f).get(subject_id)


def facing_at(spec,shot,subject_id,frame,facing_map=None):
    """Return (unit_xy_vector, source) for a subject at a local frame.

    Priority: the assigned facing map, then the subject's own travel measured
    over a widening window (immediate neighbours, then a tenth of the shot,
    then the whole shot). A subject that does not move stays undetermined
    instead of receiving an invented direction.
    """
    row=(facing_map or {}).get(shot['id'],{}).get(subject_id)
    if row:return (tuple(row['vector']),'facing-map')
    if _position(spec,shot,frame,subject_id) is None:return (None,'none')
    n=int(shot.get('duration_frames') or 1)
    windows=[1,max(2,n//10),None]
    for window in windows:
        if window is None:
            a=_position(spec,shot,0,subject_id);b=_position(spec,shot,n-1,subject_id)
        else:
            a=_position(spec,shot,frame-window,subject_id);b=_position(spec,shot,frame+window,subject_id)
        if a is None or b is None:continue
        dx,dy=b[0]-a[0],b[1]-a[1];length=math.hypot(dx,dy)
        if length>=MIN_FACING_MOVE_M:return (((dx/length),(dy/length)),'motion')
    return (None,'none')


def facing_summary(spec,shot,facing_map=None):
    """Per-subject facing record for the manifest: {subject:{vector,source}}.

    The middle frame is preferred; the rest of the shot is scanned only when
    the mid frame itself carries no determinable heading.
    """
    out={}
    n=max(1,int(shot.get('duration_frames') or 1))
    candidates=[n//2]+[f for f in range(0,n,max(1,n//8)) if f!=n//2]
    for subject_id in shot.get('subject_ids',[]):
        vector,source=None,'none'
        for frame in candidates:
            vector,source=facing_at(spec,shot,subject_id,frame,facing_map)
            if vector:break
        out[subject_id]={'vector':list(vector) if vector else None,'source':source}
    return out


def silhouette_points(size_m,proxy='box'):
    """Nine silhouette sample points as {name,z,lateral_frac}.

    ``z`` is metres above the subject base; ``lateral_frac`` multiplies the
    silhouette half-extent along the camera right axis, so the caller does not
    need to know whether the proxy is a box or a body. Points stay inside the
    proxy so a hit is meaningful: 0.9 of the half extent at most.
    """
    w,d,h=[float(v) for v in size_m]
    if proxy=='figure':
        parts={p['name']:p for p in figure_proxy_parts(size_m)}
        torso=parts['torso'];head=parts['head']
        half=torso['radius']*torso['scale'][2]
        rows=[('high',head['z']),('mid',torso['z']),('low',max(torso['z']-half*0.6,torso['z']*0.35))]
    else:
        rows=[('high',h*0.88),('mid',h*0.55),('low',h*0.25)]
    return [{'name':row+'_'+column,'z':z,'lateral_frac':frac}
            for row,z in rows for column,frac in (('left',-0.9),('center',0.0),('right',0.9))]


def silhouette_half_extent(size_m,proxy,right):
    """Half width of the proxy silhouette along the camera right axis."""
    if proxy=='figure':
        parts={p['name']:p for p in figure_proxy_parts(size_m)}
        return parts['torso']['radius']
    w,d,_=[float(v) for v in size_m]
    rx,ry=abs(right[0]),abs(right[1])
    return (rx*w+ry*d)/2.0


def figure_proxy_parts(size_m):
    """Body proxy parts, imported lazily to keep one definition in the adapter."""
    from build_previs import figure_proxy_parts as parts
    return parts(size_m)


def facing_marker_parts(size_m):
    """Cone marker geometry for a figure proxy: radius, length, offset and height.

    The cone points along local +Y, so the adapter places its base at
    ``offset_y`` on the body surface and rotates it about Z with
    :func:`facing_rotation_z`. The marker only shows travel or an assigned
    heading; it never claims face direction, eyeline target or acting.
    """
    parts={p['name']:p for p in figure_proxy_parts(size_m)}
    torso=parts['torso']
    radius=max(0.02,torso['radius']*0.32)
    return {'radius':radius,'length':max(0.12,torso['radius']*2.2),'z':torso['z'],'offset_y':torso['radius']*0.8}


def facing_rotation_z(vector):
    """Z rotation (radians) that points a local +Y cone along a world XY heading."""
    if not vector:return None
    return math.atan2(vector[1],vector[0])-math.pi/2


def cone_mesh(segments=16):
    """Return (vertices, faces) of a unit cone pointing along +Y.

    Base circle at y=0, apex at y=1, closed underneath so the mesh has a
    measurable signed volume. Pure helper: the adapter scales and rotates it.
    """
    verts=[(0.0,0.0,0.0),(0.0,1.0,0.0)]
    for j in range(segments):
        th=2.0*math.pi*j/segments
        verts.append((math.cos(th),0.0,math.sin(th)))
    faces=[]
    for j in range(segments):
        a=2+j;b=2+(j+1)%segments
        faces.append((1,b,a))
        faces.append((0,a,b))
    return verts,faces


def _f(value):
    """Fixed, locale-free number formatting so the SVG stays byte-stable."""
    return ('%.3f'%value).rstrip('0').rstrip('.') or '0'


def _escape(text):
    return (str(text).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;'))


def _camera_frames(shot,limit=60):
    """Frames to draw camera motion on: every frame, thinned to ``limit``."""
    n=max(1,int(shot.get('duration_frames') or 1))
    step=max(1,math.ceil(n/limit))
    frames=list(range(0,n,step))
    if frames[-1]!=n-1:frames.append(n-1)
    return frames


def tick_rows(rows,subject_id,to_px,min_gap_m=None):
    """Frame ticks spaced so their labels never overlap on the page.

    A slowly moving or static subject would otherwise stack every label on one
    point: the interval grows until consecutive ticks are at least ~26 px
    apart, and a fully static subject keeps a single frame label.
    """
    total=len(rows)
    if total<=1:return rows
    points=[row['positions'][subject_id] for row in rows]
    if all(point==points[0] for point in points):return rows[:1]
    scale=to_px((1.0,0.0))[0]-to_px((0.0,0.0))[0]
    gap_m=min_gap_m if min_gap_m is not None else 26.0/max(1e-9,abs(scale))
    for tick in range(max(1,math.ceil(total/6)),total):
        sampled=rows[::tick]
        gaps=[math.hypot(b['positions'][subject_id][0]-a['positions'][subject_id][0],
                         b['positions'][subject_id][1]-a['positions'][subject_id][1])
              for a,b in zip(sampled,sampled[1:])]
        if gaps and min(gaps)>=gap_m:return sampled
    return rows[::max(1,math.ceil(total/3))]


def shot_samples(spec,shot):
    """Per-frame camera samples and subject positions for the diagram."""
    rows=[]
    for f in _camera_frames(shot):
        cam=sample(shot['camera']['keyframes'],f,shot['camera']['interpolation'],shot['camera']['lens_mm'])
        rows.append({'frame':f,'camera':cam,'positions':subject_positions(spec,shot,f)})
    return rows


def _bounds(spec,shot,rows):
    xs=[c['camera']['position'][0] for c in rows];ys=[c['camera']['position'][1] for c in rows]
    for row in rows:
        for pos in row['positions'].values():xs.append(pos[0]);ys.append(pos[1])
    for subject in spec.get('subjects',[]):
        size=subject['size_m'];pos=subject['position']
        xs+=[pos[0]-size[0]/2,pos[0]+size[0]/2];ys+=[pos[1]-size[1]/2,pos[1]+size[1]/2]
    for obstacle in spec.get('obstacles',[]):
        size=obstacle['size_m'];pos=obstacle['position']
        xs+=[pos[0]-size[0]/2,pos[0]+size[0]/2];ys+=[pos[1]-size[1]/2,pos[1]+size[1]/2]
    if not xs or not ys:return (0.0,1.0,0.0,1.0)
    pad=0.8
    return (min(xs)-pad,max(xs)+pad,min(ys)-pad,max(ys)+pad)


def build_svg(spec,shot,facing_map=None,width=1180):
    """Render one shot's top-down blocking diagram as a standalone SVG string."""
    rows=shot_samples(spec,shot)
    xmin,xmax,ymin,ymax=_bounds(spec,shot,rows)
    span_x=max(1e-3,xmax-xmin);span_y=max(1e-3,ymax-ymin)
    scale=(width-80)/span_x
    height=max(320,int(span_y*scale)+180)
    origin_x=40;origin_y=60
    def px(x,y):return (origin_x+(x-xmin)*scale,origin_y+(ymax-y)*scale)
    def pxy(pos):return px(pos[0],pos[1])
    out=[]
    add=out.append
    c=shot.get('camera',{});sensor=c.get('sensor_width_mm',36.0)
    fps=spec.get('fps');n=int(shot.get('duration_frames') or 1)
    lens=[k.get('lens_mm',c.get('lens_mm')) for k in c.get('keyframes',[])] or [c.get('lens_mm')]
    add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" font-family="system-ui,sans-serif">')
    add(f'<rect width="{width}" height="{height}" fill="#0f1115"/>')
    add(f'<text x="40" y="28" fill="#f2f4f8" font-size="17" font-weight="600">{_escape(shot["id"])} top-down blocking · {_escape(shot.get("scene_id",""))} · {n} frames @ {fps}fps · lens {_f(min(lens))}–{_f(max(lens))}mm</text>')
    add(f'<text x="40" y="47" fill="#8b93a7" font-size="11">{_escape(DIAGRAM_NOTE)}</text>')
    # grid at 1 m
    step=1.0
    gx=math.floor(xmin);gy=math.floor(ymin)
    while gx<=math.ceil(xmax):
        x,_=px(gx,ymin);add(f'<line x1="{_f(x)}" y1="{_f(origin_y)}" x2="{_f(x)}" y2="{_f(origin_y+span_y*scale)}" stroke="#1e2330" stroke-width="1"/>');gx+=step
    while gy<=math.ceil(ymax):
        _,y=px(xmin,gy);add(f'<line x1="{_f(origin_x)}" y1="{_f(y)}" x2="{_f(origin_x+span_x*scale)}" y2="{_f(y)}" stroke="#1e2330" stroke-width="1"/>');gy+=step
    # obstacles
    for obstacle in spec.get('obstacles',[]):
        size=obstacle['size_m'];pos=obstacle['position']
        x0,y0=px(pos[0]-size[0]/2,pos[1]+size[1]/2);x1,y1=px(pos[0]+size[0]/2,pos[1]-size[1]/2)
        add(f'<rect x="{_f(x0)}" y="{_f(y0)}" width="{_f(x1-x0)}" height="{_f(y1-y0)}" fill="#2b3140" stroke="#4a5468"/>')
        add(f'<text x="{_f(x0+4)}" y="{_f(y0+14)}" fill="#9aa4bb" font-size="11">{_escape(obstacle["id"])}</text>')
    # subjects: start footprint (dashed), end footprint (solid), travel polyline
    for subject in spec.get('subjects',[]):
        sid=subject['id']
        if sid not in shot.get('subject_ids',[]):continue
        size=subject['size_m']
        start=rows[0]['positions'].get(sid);end=rows[-1]['positions'].get(sid)
        if start is None or end is None:continue
        for pos,dash in ((start,'6 5'),(end,'')):
            x0,y0=px(pos[0]-size[0]/2,pos[1]+size[1]/2);x1,y1=px(pos[0]+size[0]/2,pos[1]-size[1]/2)
            add(f'<rect x="{_f(x0)}" y="{_f(y0)}" width="{_f(x1-x0)}" height="{_f(y1-y0)}" fill="none" stroke="#5ad1a5" stroke-width="1.5"{f" stroke-dasharray=\"{dash}\"" if dash else ""}/>')
        points=' '.join(f'{_f(pxy(row["positions"][sid])[0])},{_f(pxy(row["positions"][sid])[1])}'
                        for i,row in enumerate(rows)
                        if i==0 or row['positions'][sid]!=rows[i-1]['positions'][sid])
        if ' ' not in points.strip():points=points.strip()+' '+points.strip()
        add(f'<polyline points="{points}" fill="none" stroke="#5ad1a5" stroke-width="2.5" opacity="0.9"/>')
        for row in tick_rows(rows,sid,pxy):
            x,y=pxy(row['positions'][sid])
            add(f'<circle cx="{_f(x)}" cy="{_f(y)}" r="2.5" fill="#5ad1a5"/>')
            add(f'<text x="{_f(x+5)}" y="{_f(y-5)}" fill="#5ad1a5" font-size="10">{row["frame"]}</text>')
        vector,source=facing_at(spec,shot,sid,n//2,facing_map)
        reach=min(1.0,max(0.35,0.75*max(subject['size_m'][0],subject['size_m'][1])))
        label_x,label_y=pxy(start)
        add(f'<text x="{_f(label_x-7)}" y="{_f(label_y-9)}" text-anchor="end" fill="#cdd5e4" font-size="11">{_escape(sid)}</text>')
        if vector:
            x,y=pxy(end);ax,ay=px(end[0]+vector[0]*reach,end[1]+vector[1]*reach)
            add(f'<line x1="{_f(x)}" y1="{_f(y)}" x2="{_f(ax)}" y2="{_f(ay)}" stroke="#ffd479" stroke-width="2.5"/>')
            add(f'<circle cx="{_f(ax)}" cy="{_f(ay)}" r="3.5" fill="#ffd479"/>')
            add(f'<text x="{_f(ax+6)}" y="{_f(ay+13)}" fill="#ffd479" font-size="10">facing·{source}</text>')
        else:
            x,y=pxy(end);add(f'<text x="{_f(x+6)}" y="{_f(y+15)}" fill="#7d869c" font-size="10">facing undetermined</text>')
        x,y=px(start[0],start[1]);add(f'<text x="{_f(x)}" y="{_f(y-8)}" fill="#cdd5e4" font-size="11">{_escape(sid)}</text>')
    # camera path + frustum wedges
    camera_points=[pxy(row['camera']['position']) for row in rows]
    deduped=[point for i,point in enumerate(camera_points) if i==0 or point!=camera_points[i-1]]
    if len(deduped)==1:deduped=deduped*2
    add('<polyline points="'+' '.join(f'{_f(x)},{_f(y)}' for x,y in deduped)+'" fill="none" stroke="#ff8c69" stroke-width="2"/>')
    drawn=set();wedges=0
    for row in rows:
        if wedges>=12:break
        cam=row['camera'];position=cam['position'];target=cam['target']
        dx,dy=target[0]-position[0],target[1]-position[1];length=math.hypot(dx,dy)
        if length<1e-6:continue
        heading=math.atan2(dy,dx)
        key=(round(position[0],3),round(position[1],3),round(heading,3))
        if key in drawn:continue
        drawn.add(key);wedges+=1
        half=math.atan(sensor/(2*max(1e-6,cam['lens_mm'])))
        nearest=min([math.hypot(p[0]-position[0],p[1]-position[1]) for p in row['positions'].values()]+[2.0])
        reach=max(0.6,min(2.0,nearest))
        x0,y0=px(position[0],position[1])
        edges=[]
        for angle in (heading-half,heading+half):
            ex,ey=position[0]+math.cos(angle)*reach,position[1]+math.sin(angle)*reach
            edges.append(px(ex,ey))
        add(f'<polygon points="{_f(x0)},{_f(y0)} {_f(edges[0][0])},{_f(edges[0][1])} {_f(edges[1][0])},{_f(edges[1][1])}" fill="#ff8c69" opacity="0.05" stroke="#ff8c69" stroke-opacity="0.22" stroke-width="1"/>')
    first_px=pxy(rows[0]['camera']['position']);last_px=pxy(rows[-1]['camera']['position'])
    add(f'<circle cx="{_f(first_px[0])}" cy="{_f(first_px[1])}" r="4" fill="#ff8c69"/>')
    if math.hypot(last_px[0]-first_px[0],last_px[1]-first_px[1])<6:
        add(f'<text x="{_f(first_px[0]+7)}" y="{_f(first_px[1]+13)}" fill="#ff8c69" font-size="10">cam static·f{rows[0]["frame"]}–f{rows[-1]["frame"]}</text>')
    else:
        add(f'<text x="{_f(first_px[0]+7)}" y="{_f(first_px[1]+13)}" fill="#ff8c69" font-size="10">cam start·f{rows[0]["frame"]}</text>')
        add(f'<circle cx="{_f(last_px[0])}" cy="{_f(last_px[1])}" r="4" fill="#ff8c69"/>')
        add(f'<text x="{_f(last_px[0]+7)}" y="{_f(last_px[1]-8)}" fill="#ff8c69" font-size="10">cam end·f{rows[-1]["frame"]}</text>')
    # legend + scale bar
    add(f'<g transform="translate(40 {height-52})" font-size="11">')
    add('<line x1="0" y1="0" x2="22" y2="0" stroke="#ff8c69" stroke-width="2"/><text x="28" y="4" fill="#cdd5e4">camera path / frustum</text>')
    add('<line x1="200" y1="0" x2="222" y2="0" stroke="#5ad1a5" stroke-width="2"/><text x="228" y="4" fill="#cdd5e4">subject travel</text>')
    add('<line x1="360" y1="0" x2="382" y2="0" stroke="#ffd479" stroke-width="2.5"/><text x="388" y="4" fill="#cdd5e4">facing (map or motion)</text>')
    add('</g>')
    bx0,by0=px(xmin+0.3,ymin+0.3)
    add(f'<line x1="{_f(bx0)}" y1="{_f(by0)}" x2="{_f(bx0+scale)}" y2="{_f(by0)}" stroke="#8b93a7" stroke-width="2"/>')
    add(f'<text x="{_f(bx0+4)}" y="{_f(by0-5)}" fill="#8b93a7" font-size="10">1 m</text>')
    add('</svg>')
    return '\n'.join(out)+'\n'


def occlusion_summary(checks,shot,proxy='box'):
    """Per-subject visible fraction and first occluded point from inspection rows."""
    out={}
    for subject_id in shot.get('subject_ids',[]):
        rows=[c for c in checks if c['subject_id']==subject_id]
        if not rows:continue
        visible=[c for c in rows if c['proxy_point_visible']]
        first_hidden=next((c for c in rows if not c['proxy_point_visible']),None)
        out[subject_id]={'points_checked':len(rows),'points_visible':len(visible),
                         'visible_fraction':round(len(visible)/len(rows),4),
                         'first_occluded':({'frame':first_hidden['frame'],'point':first_hidden['point'],'first_hit':first_hidden['first_hit']} if first_hidden else None),
                         'proxy':proxy}
    return {'frames_checked':len({c['frame'] for c in checks}),'subjects':out,
            'scope':'nine silhouette sample points per subject per frame; point sampling only, not whole-silhouette, articulated or contact visibility'}
