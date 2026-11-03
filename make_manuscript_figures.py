"""Figures 1-5 of the manuscript, drawn from the pooled summary values reported in the paper."""
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, numpy as np
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,'axes.spines.right':False})
G1,G2,G3,G4='#2b5d8a','#8fb3d9','#c0504d','#e8a29f'
# Fig 1 flow
fig,ax=plt.subplots(figsize=(6.2,3.6)); ax.axis('off')
def box(x,y,w,h,t,fc='white'):
    ax.add_patch(plt.Rectangle((x,y),w,h,fc=fc,ec='black',lw=0.8)); ax.text(x+w/2,y+h/2,t,ha='center',va='center',fontsize=8)
box(0.18,0.82,0.64,0.14,'457 patients with paired anterior and posterior\nwhole-body scans and a recorded label (2016–2025)')
box(0.56,0.5,0.44,0.21,'Excluded by image-level audit: 28\n  identical ANT and POST image: 24\n  image shared with another ID: 5\n  (one patient had both)')
box(0.0,0.5,0.42,0.21,'Indeterminate label: 85\n(not classified; unlabelled images\nused only for domain adaptation)')
box(0.18,0.24,0.64,0.14,'Classification cohort: 344 patients\nMetastatic 123 · Degenerative 122 · Normal 99')
box(0.04,0.0,0.4,0.14,'Machine 1 (GE Infinia): 166\nMet 65 · Deg 59 · Nor 42')
box(0.56,0.0,0.4,0.14,'Machine 2 (Siemens): 178\nMet 58 · Deg 63 · Nor 57')
for (x1,y1,x2,y2) in [(0.5,0.82,0.5,0.38),(0.5,0.6,0.56,0.6),(0.5,0.6,0.42,0.6),(0.5,0.24,0.24,0.14),(0.5,0.24,0.76,0.14)]:
    ax.annotate('',xy=(x2,y2),xytext=(x1,y1),arrowprops=dict(arrowstyle='->',lw=0.8))
ax.set_xlim(-0.02,1.02); ax.set_ylim(-0.02,1); fig.savefig('fig1.png',dpi=300,bbox_inches='tight'); plt.close()
# Fig 2
lab=['Own machine','Other machine','Both machines\n(all data)','Both machines\n(size-matched)']
V={('ImageNet','Machine 1'):[0.714,0.714,0.758,0.726],('ImageNet','Machine 2'):[0.764,0.659,0.807,0.755],
   ('BS-80K','Machine 1'):[0.773,0.778,0.808,0.785],('BS-80K','Machine 2'):[0.832,0.796,0.859,0.832]}
fig,axs=plt.subplots(1,2,figsize=(7,2.9),sharey=True)
for ax,init in zip(axs,['ImageNet','BS-80K']):
    x=np.arange(2); w=0.2
    for j,(l,c) in enumerate(zip(lab,[G1,G3,G2,G4])):
        v=[V[(init,m)][j] for m in ['Machine 1','Machine 2']]
        b=ax.bar(x+(j-1.5)*w,v,w,color=c,label=l.replace('\n',' '))
        for xi,vi in zip(x+(j-1.5)*w,v): ax.text(xi,vi+0.004,f'{vi:.2f}',ha='center',fontsize=6.5)
    ax.set_xticks(x); ax.set_xticklabels(['Test: Machine 1','Test: Machine 2']); ax.set_title(f'{init} initialisation',fontsize=9); ax.set_ylim(0.6,0.89)
axs[0].set_ylabel('Macro-F1 (5 tasks × 4 backbones)')
axs[1].legend(fontsize=7,frameon=False,loc='upper left',bbox_to_anchor=(1.0,1.0))
fig.tight_layout(); fig.savefig('fig2.png',dpi=300,bbox_inches='tight'); plt.close()
# Fig 3 forest
rows=[('DANN','3 seeds',+0.022,0.000,0.043,-0.001,-0.010,0.008),
      ('Deep CORAL','3 seeds',+0.028,0.010,0.047,-0.003,-0.012,0.007),
      ('Recalibration (20 labelled)','3 seeds',+0.054,0.028,0.080,+0.004,-0.007,0.015),
      ('Intensity normalisation','seed 1',-0.040,-0.061,-0.019,-0.055,-0.079,-0.033),
      ('Intensity augmentation','seed 1',+0.037,0.007,0.067,+0.003,-0.011,0.018),
      ('MixStyle','seed 1',+0.012,-0.007,0.029,+0.005,-0.004,0.015)]
fig,axs=plt.subplots(1,2,figsize=(7,2.6),sharey=True)
y=np.arange(len(rows))[::-1]
for k,(ax,t) in enumerate(zip(axs,['ImageNet, Machine 1 → Machine 2','BS-80K, both directions'])):
    for yi,r in zip(y,rows):
        e,lo,hi=r[2+3*k],r[3+3*k],r[4+3*k]; c=G3 if hi<0 else (G1 if lo>0 else 'grey')
        ax.plot([lo,hi],[yi,yi],color=c,lw=1.5); ax.plot(e,yi,'o',color=c,ms=4)
    ax.axvline(0,color='black',lw=0.6); ax.set_title(t,fontsize=9); ax.set_xlabel('Δ macro-F1 vs no adaptation (95% CI)')
axs[0].set_yticks(y); axs[0].set_yticklabels([f'{r[0]} ({r[1]})' for r in rows],fontsize=7.5)
fig.tight_layout(); fig.savefig('fig3.png',dpi=300,bbox_inches='tight'); plt.close()
# Fig 4 BS-80K->machines
meth=['none','recal','iaug','mixstyle','dann','coralstd']; mlab=['BS-80K only','+ Recalibration','+ Intensity aug.','+ MixStyle','+ DANN','+ Deep CORAL']
S={'T3':[0.654,0.718,0.669,0.716,0.618,0.756],'T2':[0.649,0.669,0.609,0.692,0.575,0.674],'T4':[0.611,0.640,0.532,0.656,0.557,0.639]}
own={'T3':0.767,'T2':0.807,'T4':0.787}; oth={'T3':0.724,'T2':0.736,'T4':0.712}
tn={'T3':'T3 metastatic vs normal','T2':'T2 metastatic vs non-metastatic','T4':'T4 metastatic vs degenerative'}
fig,axs=plt.subplots(1,3,figsize=(7.2,2.8),sharey=True)
for ax,t in zip(axs,['T3','T2','T4']):
    cols=['#9e9e9e',G2,G2,G2,G4,G1]
    ax.bar(range(6),S[t],color=cols)
    for i,v in enumerate(S[t]): ax.text(i,v+0.006,f'{v:.2f}',ha='center',fontsize=6.5)
    ax.axhline(own[t],color='black',ls='--',lw=0.8); ax.axhline(oth[t],color='black',ls=':',lw=0.8)
    ax.set_xticks(range(6)); ax.set_xticklabels(mlab,rotation=55,ha='right',fontsize=7); ax.set_title(tn[t],fontsize=8); ax.set_ylim(0.5,0.85)
axs[0].set_ylabel('Macro-F1 on Machines 1 + 2')
axs[2].plot([],[],'k--',lw=0.8,label='Own-machine model'); axs[2].plot([],[],'k:',lw=0.8,label='Other-machine model'); fig.legend(fontsize=7,frameon=False,loc='lower center',ncol=2,bbox_to_anchor=(0.5,-0.06))
fig.tight_layout(); fig.savefig('fig4.png',dpi=300,bbox_inches='tight'); plt.close()
# Fig 5 detection by burden
bins=['0–2\n(n=35)','3–5\n(n=42)','6–9\n(n=27)','≥10\n(n=10)']
D={'T2, ImageNet':[54,81,89,100],'T2, BS-80K':[57,90,96,100],'T3, ImageNet':[60,81,89,100],'T3, BS-80K':[77,93,96,100]}
fig,ax=plt.subplots(figsize=(5,2.6)); w=0.2; x=np.arange(4)
for j,(k,c) in enumerate(zip(D,[G2,G1,G4,G3])): ax.bar(x+(j-1.5)*w,D[k],w,color=c,label=k)
ax.set_xticks(x); ax.set_xticklabels(bins); ax.set_xlabel('Reader-confirmed lesions per patient'); ax.set_ylabel('Metastatic patients detected (%)'); ax.set_ylim(0,105)
ax.legend(fontsize=7,frameon=False,ncol=2,loc='lower right'); fig.tight_layout(); fig.savefig('fig5.png',dpi=300,bbox_inches='tight'); plt.close()
print('ok')
