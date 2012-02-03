import sfle
import sfleoo
import sys
import collections
import math
from pandas import *


def screen_usearch_wdb( io ):
    tab = ((l[0].split(' ')[0],l[1].split('_')[1],float(l[-1])) 
		for l in io.inp_tab())
    f2p, f2b, p2b = {}, {}, {}
    for f,p,b in tab:
        if f in f2p and b < f2b[f]:
            continue
        if p in p2b and b < p2b[p]:
            continue 
        if p in p2b:
            for ff in f2p.keys():
                if p in f2p[ff]:
                    del f2p[ff]
                    del f2b[ff]
        f2p[f], f2b[f], p2b[p] = p, b, b
    io.out_tab( f2p.items()  ) 
        
def img_add_mtol( io ):
    df = DataFrame.from_csv(io.inpf[0],sep='\t')
    o2lp = dict( [(int(ll[0]),ll[1]) for ll in 
                     (l.strip().split('\t') for l in open(io.inpf[1])) ] )
    df['mtol400 Proteins Count'] = [(o2lp[k] if k in o2lp else -1) for k in df.index] 
    df.to_csv( io.outf[0], sep = '\t' ) 

def annotate_img_l( io ):
    clades = io.inp_dict()
    df = DataFrame.from_csv(io.inpf[1],sep='\t')
    nmax = float(max(df['mtol400 Proteins Count']))
    rmax = float(max(df['16S rRNA Count']))
    n = len(clades)
    ew = (1.0/math.log(float(n)))**3*100.0
    annots = ["*\twidth\t1\t1.0\n"]
    annots += ["*\twidth\t4\t0.8\n"]
    annots += ["*\tbranch_line_width\t"+str(ew)]
    annots += ["*\tannotation_ext_offset\t0.001\n"]
    annots += ["*\tbranch_acestor_clade_color\t0\n"]
    annots += ["*\tsub_branches_opening_point\t0.75\n"]
    annots += ["*\tedge_width\t1\t0.0\n"]
    annots += ["*\tedge_width\t2\t0.0\n"]
    annots += ["*\tedge_width\t3\t0.0\n"]
    annots += ["*\theight\t1\t0.5\n"]
    annots += ["*\theight\t2\t0.5\n"]
    annots += ["*\theight\t3\t0.5\n"]
    annots += ["\t".join( [k,'height','4',str(float(df['mtol400 Proteins Count'][int(v)])*3.0/nmax) ])
                    for k,v in clades.items()]
    annots += ["\t".join( [k,'fill_color','4','#DDD000' ])
                    for k,v in clades.items() if df['Status'][int(v)] == 'Draft']
    annots += ["\t".join( [k,'fill_color','4','#00AA00' ])
                    for k,v in clades.items() if df['Status'][int(v)] == 'Finished']
    annots += ["\t".join( [k,'alpha','1',str(df['16S rRNA Count'][int(v)]/rmax*3.0) ])
                    for k,v in clades.items() if df['16S rRNA Count'][int(v)] > 0 ]
    annots += ["\t".join( [k,'fill_color','1','#0000FF' ])
                    for k,v in clades.items() if df['16S rRNA Count'][int(v)] > 0 ]
    annots += ["\t".join( [k,'fill_color','1','#FF0000']) 
                    for k,v in clades.items() if df['16S rRNA Count'][int(v)] <= 0 ]
    annots += ["\t".join( [k,'fill_color','2','#00FF00' ])
                    for k,v in clades.items() if df['Gram Staining'][int(v)] == 'Gram+' ]
    annots += ["\t".join( [k,'fill_color','2','#FF0000' ])
                    for k,v in clades.items() if df['Gram Staining'][int(v)] == 'Gram-' ]
    oxy2col = { 'Obligate aerobe':'#00EE00',
                'Aerobe':'#008B00',
                'Microaerophilic':'#003000',
                'Facultative':'#000000',
                'Anaerobe':'#8B0000',
                'Obligate anaerobe':'#DD0000' }
    annots += ["\t".join( [k,'fill_color','3',oxy2col[df['Oxygen Requirement'][int(v)]] ])
                    for k,v in clades.items() if df['Oxygen Requirement'][int(v)] != '-1' ]
    fams = collections.defaultdict(list)
    phys = collections.defaultdict(list)
    for c,t in clades.items():
        cs = c.split('.')
        if cs[4] == 'unclassified':
            continue
        fams[cs[4]].append(int(t))
        phys[".".join(cs[:2])].append(int(t))
    nmin = n / 360.0 * 5
    nmin2 = n / 360.0 * 12
    for k,v in fams.items():
        if len(v) > nmin:
            annots += ["\t".join( [str(k),'clade_fill_color','#DD0000' ])]
            if len(v) > nmin2:
                annots += ["\t".join( [str(k),'annotation_label',str(k) ])]
            else:
                annots += ["\t".join( [str(k),'annotation_label',str(k)[:5]+"." ])]
            annots += ["\t".join( [str(k),'annotation_color','#DD0000' ])]
    for k,v in phys.items():
        if len(v) > nmin:
            annots += ["\t".join( [str(k),'clade_fill_color','#0000DD' ])]
            if len(v) > nmin2:
                annots += ["\t".join( [str(k),'annotation_label',str(k).split('.')[-1] ])]
            else:
                annots += ["\t".join( [str(k),'annotation_label',str(k).split('.')[-1][:5]+"." ])]
            annots += ["\t".join( [str(k),'annotation_color','#0000DD' ])]
    io.out_tab( annots )

def count_ups( io ):
    ups = set()
    for ll in ( l.strip().split('\t') for l in open( io.inpf[1] ) ):
        ups |= set(ll)
    orgs2ups = collections.defaultdict( list )
    for l in io.inp_tab():
        for ll in l[1:]:
            if ll in ups:
                orgs2ups[l[0]].append( ll )
    io.out_tab( [(str(k),str(len(v))) for k,v in orgs2ups.items()] ) 

def extract_o2g( io ):
    prots = [l[0][1:].split(' ')[0] for l in io.inp_tab() if l[0][0] == '>']
    io.out_tab( [[io.args['t']] + prots] )

def merge_t2up_maps( io ):
    up2p = collections.defaultdict( list )
    for f in io.inpf:
        for p,up in (l.strip().split('\t') for l in open(f).readlines()):
            up2p[up].append( p )
    io.out_tab( ([k]+v for k,v in up2p.items())  )
