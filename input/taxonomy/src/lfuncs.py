import sfle
import sfleoo
import sys
import collections
import math
from pandas import *


# User-defined local funtions
def alnum( s ):
    return "".join([ss if ss.isalnum() else '_' for ss in s])

def extract_ncbi_taxonomy( io ):
    import tarfile
    import collections
    tar = tarfile.open(io.inpf[0])
    tree = collections.defaultdict(list)
    id2names = dict([(int(v[0]),alnum(v[1])) 
                    for v in (l.strip().split('\t|\t') 
                        for l in tar.extractfile("names.dmp").readlines()) 
                            if v[3][:-2] == "scientific name"])
    names2id = dict(((v,k) for k,v in id2names.items()))
    for c,f,t in (l.strip().split('\t|\t')[:3] 
                for l in  tar.extractfile("nodes.dmp").readlines()):
        if c != f:
            tree[int(f)].append(int(c))
    root = 'root' if 'root' not in io.args else io.args['root']
    with open( io.outf[0], 'w' ) as outf:
        def print_rec( cl, s = "root" ):
            if not tree[cl]:
                outf.write( s +"\n" ) 
            for v in tree[cl]:
                print_rec( v, s + "." + id2names[v] )
        print_rec( names2id[root], root )


def screen_img_taxonomy( io ):
    df = DataFrame.from_csv(io.inpf[0],sep='\t')
    if 'Domain' in io.args:
        df = df[df['Domain'] == io.args['Domain']]
    
    for n,c in [ ('min_CDSs','CDS Count'),
                 ('min_CDS_perc','CDS %'),   
                 ('min_genome_size','Genome Size'),
                 ]:
        if n in io.args:
            df = df[df[c] >= io.args[n]]
    df.to_csv( io.outf[0], sep = '\t' )

def process_img_taxonomy( io ):
    df = DataFrame.from_csv(io.inpf[0],sep='\t')
    tax_levs = [ ('d__','Domain'),('p__','Phylum'),('c__','Class'),
                 ('o__','Order'),('f__','Family'),('g__','Genus'),
                 ('s__','Species'),('o__','Strain') ]
   
    outs = ( ".".join( [alnum(df[v][ind]) for k,v in tax_levs] ) + "\t" + str(ind)
                for ind in df.index 
                    if not ( 'Domain' in io.args and
                             io.args['Domain'] == df['Domain'][ind]) )
    io.out_tab(sorted(outs))

def annotate_img( io ):
    clades = io.inp_dict()
    df = DataFrame.from_csv(io.inpf[1],sep='\t')
    nmax = float(max(df['CDS Count']))
    rmax = float(max(df['16S rRNA Count']))
    n = len(clades)
    ew = (1.0/math.log(float(n)))**3*100.0
    annots = ["*\twidth\t1\t1.0\n"]
    annots += ["*\twidth\t2\t0.8\n"]
    annots += ["*\tbranch_line_width\t"+str(ew)]
    annots += ["*\tannotation_ext_offset\t0.001\n"]
    annots += ["*\tbranch_acestor_clade_color\t0\n"]
    annots += ["*\tsub_branches_opening_point\t0.75\n"]
    annots += ["*\tedge_width\t1\t0.0\n"]
    annots += ["*\theight\t1\t0.5\n"]
    annots += ["\t".join( [k,'height','2',str(df['CDS Count'][int(v)]/nmax*3.0) ])
                    for k,v in clades.items()]
    annots += ["\t".join( [k,'fill_color','2','#DDD000' ])
                    for k,v in clades.items() if df['Status'][int(v)] == 'Draft']
    annots += ["\t".join( [k,'fill_color','2','#00AA00' ])
                    for k,v in clades.items() if df['Status'][int(v)] == 'Finished']
    annots += ["\t".join( [k,'alpha','1',str(df['16S rRNA Count'][int(v)]/rmax*3.0) ])
                    for k,v in clades.items() if df['16S rRNA Count'][int(v)] > 0 ]
    annots += ["\t".join( [k,'fill_color','1','#0000FF' ])
                    for k,v in clades.items() if df['16S rRNA Count'][int(v)] > 0 ]
    annots += ["\t".join( [k,'fill_color','1','#FF0000']) 
                    for k,v in clades.items() if df['16S rRNA Count'][int(v)] <= 0 ]
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

