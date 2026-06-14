#!/usr/bin/env python3
"""Convierte un .3mf (geometría) a .glb binario sin trimesh/blender.
Parser SAX en streaming (memoria acotada) + normales por vértice.
Uso: python3 convert_3mf_glb.py <in.3mf> <out.glb>
"""
import sys, zipfile, struct, json, math
from array import array
import xml.sax

SRC, OUT = sys.argv[1], sys.argv[2]

# localizar el .model dentro del zip 3mf
with zipfile.ZipFile(SRC) as z:
    model_name = next(n for n in z.namelist() if n.endswith('.model') and 'Objects' in n)
    print('modelo:', model_name)

class MeshHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.verts = array('f')
        self.idx = array('I')
    def startElement(self, name, attrs):
        n = name.split(':')[-1]
        if n == 'vertex':
            self.verts.append(float(attrs.get('x')))
            self.verts.append(float(attrs.get('y')))
            self.verts.append(float(attrs.get('z')))
        elif n == 'triangle':
            self.idx.append(int(attrs.get('v1')))
            self.idx.append(int(attrs.get('v2')))
            self.idx.append(int(attrs.get('v3')))

h = MeshHandler()
with zipfile.ZipFile(SRC) as z, z.open(model_name) as f:
    xml.sax.parse(f, h)
verts, idx = h.verts, h.idx
nv, nt = len(verts) // 3, len(idx) // 3
print(f'vertices={nv} triangulos={nt}')

# normales por vértice (acumular normal de cara, luego normalizar)
nrm = array('f', [0.0]) * (nv * 3)
for t in range(nt):
    a = idx[t*3]*3; b = idx[t*3+1]*3; c = idx[t*3+2]*3
    ax,ay,az = verts[a],verts[a+1],verts[a+2]
    bx,by,bz = verts[b],verts[b+1],verts[b+2]
    cx,cy,cz = verts[c],verts[c+1],verts[c+2]
    ux,uy,uz = bx-ax,by-ay,bz-az
    vx,vy,vz = cx-ax,cy-ay,cz-az
    nx = uy*vz - uz*vy
    ny = uz*vx - ux*vz
    nz = ux*vy - uy*vx
    for off in (a,b,c):
        nrm[off]+=nx; nrm[off+1]+=ny; nrm[off+2]+=nz
for i in range(nv):
    o=i*3; x,y,z=nrm[o],nrm[o+1],nrm[o+2]
    l=math.sqrt(x*x+y*y+z*z) or 1.0
    nrm[o]=x/l; nrm[o+1]=y/l; nrm[o+2]=z/l

# bounding box / min-max para accessors
xs=verts[0::3]; ys=verts[1::3]; zs=verts[2::3]
pmin=[min(xs),min(ys),min(zs)]; pmax=[max(xs),max(ys),max(zs)]

# --- ensamblar GLB ---
def pad4(b, fill=b'\x00'): return b + fill*((4-len(b)%4)%4)
pos_b = verts.tobytes()
nrm_b = nrm.tobytes()
idx_b = idx.tobytes()
bin_blob = pad4(pos_b)+pad4(nrm_b)+pad4(idx_b)
off_pos=0; off_nrm=len(pad4(pos_b)); off_idx=off_nrm+len(pad4(nrm_b))

gltf={
 "asset":{"version":"2.0","generator":"d3x-3mf2glb"},
 "scene":0,"scenes":[{"nodes":[0]}],
 "nodes":[{"mesh":0}],
 "meshes":[{"primitives":[{"attributes":{"POSITION":0,"NORMAL":1},"indices":2,"material":0}]}],
 "materials":[{"pbrMetallicRoughness":{"baseColorFactor":[0.72,0.74,0.78,1.0],"metallicFactor":0.15,"roughnessFactor":0.6}}],
 "buffers":[{"byteLength":len(bin_blob)}],
 "bufferViews":[
   {"buffer":0,"byteOffset":off_pos,"byteLength":len(pos_b),"target":34962},
   {"buffer":0,"byteOffset":off_nrm,"byteLength":len(nrm_b),"target":34962},
   {"buffer":0,"byteOffset":off_idx,"byteLength":len(idx_b),"target":34963},
 ],
 "accessors":[
   {"bufferView":0,"componentType":5126,"count":nv,"type":"VEC3","min":pmin,"max":pmax},
   {"bufferView":1,"componentType":5126,"count":nv,"type":"VEC3"},
   {"bufferView":2,"componentType":5125,"count":len(idx),"type":"SCALAR"},
 ],
}
json_blob=pad4(json.dumps(gltf,separators=(',',':')).encode('utf-8'), b'\x20')  # JSON chunk: padding con espacios (spec GLB)
total=12+8+len(json_blob)+8+len(bin_blob)
with open(OUT,'wb') as o:
    o.write(b'glTF'); o.write(struct.pack('<II',2,total))
    o.write(struct.pack('<I',len(json_blob))); o.write(b'JSON'); o.write(json_blob)
    o.write(struct.pack('<I',len(bin_blob))); o.write(b'BIN\x00'); o.write(bin_blob)
print(f'OK -> {OUT}  ({total/1e6:.1f} MB)')
print(f'bbox min={pmin} max={pmax}')
