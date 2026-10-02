#!/usr/bin/env python3
"""Draw mathematical wireframe panels, NOT Blender renders; requires Pillow."""
import argparse,json,sys
from pathlib import Path
from spatial_spec import validate,sample,subject_positions,corners,project

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('spec');p.add_argument('output');args=p.parse_args()
    from PIL import Image,ImageDraw,ImageFont
    data=json.loads(Path(args.spec).read_text());errors=validate(data)
    if errors:raise SystemExit(json.dumps(errors))
    width=360;height=round(width*data['resolution'][1]/data['resolution'][0]);header=50;rowheight=height+30
    result=Image.new('RGB',(width*3,header+rowheight*len(data['shots'])),(236,240,244));d=ImageDraw.Draw(result)
    d.text((12,8),'NUMERICAL PINHOLE PREVIEW / NOT A BLENDER RENDER',fill=(10,30,50))
    d.text((12,25),'Box proxies; occlusion, lighting and acting are not simulated.',fill=(30,50,70))
    subjects={x['id']:x for x in data['subjects']}
    for row,shot in enumerate(data['shots']):
        for col,f in enumerate(sorted({0,shot['duration_frames']//2,shot['duration_frames']-1})):
            x0=col*width;y0=header+row*rowheight;d.rectangle((x0+2,y0+24,x0+width-2,y0+24+height),fill='white',outline=(150,160,170))
            d.text((x0+10,y0+5),f'{shot["id"]} frame {f} / {data["fps"]} fps',fill=(20,35,55))
            panel=Image.new('RGB',(width,height),'white');pd=ImageDraw.Draw(panel);pd.rectangle((1,1,width-2,height-2),outline=(150,160,170))
            c=shot['camera'];k=sample(c['keyframes'],f,c['interpolation'],c['lens_mm']);positions=subject_positions(data,shot,f)
            for rid in shot['subject_ids']:
                obj=subjects[rid];points=[project(pt,k,*data['resolution'],c['sensor_width_mm'],c.get('roll_deg',0)) for pt in corners(positions[rid],obj['size_m'])]
                color=tuple(round(x*255) for x in obj.get('color_rgba',[.2,.4,.7,1])[:3])
                for i in range(8):
                    for j in range(i+1,8):
                        if (i^j) not in (1,2,4):continue
                        a,b=points[i],points[j]
                        if a[0] is None or b[0] is None or a[2]<=0 or b[2]<=0:continue
                        pd.line((a[0]*width,(1-a[1])*height,b[0]*width,(1-b[1])*height),fill=color,width=2)
                center=project([positions[rid][0],positions[rid][1],positions[rid][2]+obj['size_m'][2]],k,*data['resolution'],c['sensor_width_mm'],c.get('roll_deg',0))
                if center[0] is not None and center[2]>0:pd.text((center[0]*width,(1-center[1])*height-16),rid,fill=color)
            result.paste(panel,(x0,y0+24))
    result.save(args.output)
    print(args.output)
if __name__=='__main__':main()
