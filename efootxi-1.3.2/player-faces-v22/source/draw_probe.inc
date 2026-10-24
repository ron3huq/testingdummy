/* Read-only draw inspection on native callback threads. Never change render
 * flags/materials or scan undeclared object memory. All strings copied to BSS;
 * no UObject pointers are exposed to the Python reporting thread. */
#define PROBE_ROWS 8
#define PROBE_NAMES 13
#define PROBE_CHARS 96
typedef struct{u32 slot,primary,flags;u16 names[PROBE_NAMES][PROBE_CHARS];}DrawProbe;
typedef struct{uptr card;u32 count,generation;DrawProbe rows[PROBE_ROWS];}DrawSample;
static volatile DrawSample draw_samples[8];
static u32 draw_generation,draw_sample_cursor;
static struct{void*actor,*mesh;u32 tick;} draw_owners[16];
static u32 draw_cursor;
static int probe_card(uptr id){return id==TARGET||id==TARGET_2006||id==106734785925546UL||id==105765448873424UL||id==105643042189511UL||id==106778792700170UL||id==88038776539586UL||id==105807861630781UL;}
static void probe_name(void*object,u16*out){
 FString s={0};
 if(object)((void(*)(const void*,FString*))(engine_base+0x4415ac8))((char*)object+0x18,&s);
 for(int j=0;j<PROBE_CHARS;j++)out[j]=s.data&&s.count>0&&s.count<1024&&j<s.count&&j<PROBE_CHARS-1?s.data[j]:0;
 if(s.data)((void(*)(void*))(engine_base+0x42cc968))((void*)s.data);
}
static int probe_instance(void*object){
 if(!object)return 0;void*cls=*(void**)((char*)object+0x10);if(!cls)return 0;u16 name[PROBE_CHARS];probe_name(cls,name);
 const char*prefix="MaterialInstance";for(int i=0;prefix[i];i++)if(name[i]!=(u16)prefix[i])return 0;return 1;
}
static void inspect_head_draw(void*actor,void*mesh){
 if(!actor||!mesh||!enabled)return;uptr id=*(uptr*)((char*)actor+0x10b0);if(!probe_card(id))return;
 void*components[PROBE_ROWS];u32 slots[PROBE_ROWS],count=0;void*root=*(void**)((char*)actor+0x228);
 if(root){components[count]=root;slots[count++]=0x228;}
 const u32 offsets[]={0x1a70,0x1a80,0x1ad0};
 for(u32 a=0;a<3;a++){
  void**list=*(void***)((char*)actor+offsets[a]);int n=*(int*)((char*)actor+offsets[a]+8),cap=*(int*)((char*)actor+offsets[a]+12);
  if(!list||n<0||n>32||cap<n||cap>64)continue;
  for(int j=0;j<n&&count<PROBE_ROWS;j++){
   void*c=list[j];if(!c)continue;int repeated=0;for(u32 k=0;k<count;k++)if(components[k]==c)repeated=1;
   if(!repeated){components[count]=c;slots[count++]=offsets[a]+(u32)j*0x10000;}
  }
 }
 DrawProbe rows[PROBE_ROWS];
 for(u32 i=0;i<count;i++){
  void*c=components[i];void*current=*(void**)((char*)c+0x468);rows[i].slot=slots[i];rows[i].primary=current==mesh;rows[i].flags=*(u32*)((char*)c+0x210);
  for(int k=0;k<PROBE_NAMES;k++)probe_name(0,rows[i].names[k]);probe_name(current,rows[i].names[0]);
  /* Only a component proven to hold the callback's private mesh is queried
   * through GetMaterial. Other meshes are listed with names/flags only. */
  if(current!=mesh)continue;
  const u32 actor_tex[]={0x1a40,0x1a48,0x1a90,0x1a98};for(int a=0;a<4;a++)probe_name(*(void**)((char*)actor+actor_tex[a]),rows[i].names[a+9]);
  void**v=*(void***)c;if(!v||!v[0x588/8])continue;
  void*material=((void*(*)(void*,int))v[0x588/8])(c,0);probe_name(material,rows[i].names[1]);
  if(!probe_instance(material))continue;void*parent=*(void**)((char*)material+0xd0);probe_name(parent,rows[i].names[2]);
  if(probe_instance(parent)){void*grand=*(void**)((char*)parent+0xd0);probe_name(grand,rows[i].names[7]);if(probe_instance(grand))probe_name(*(void**)((char*)grand+0xd0),rows[i].names[8]);}
  const char*parameters[]={"faceBaseColor","BaseColorMap","NormalMap","SROMap"};
  for(int p=0;p<4;p++){uptr key=0;((NameFn)(engine_base+0x4414bec))(&key,parameters[p],1);void*t=((GetTexFn)(engine_base+0x59b8a2c))(material,key);probe_name(t,rows[i].names[p+3]);}
 }
 if(!take())return;int sample=-1;
 for(int i=0;i<8;i++)if(draw_samples[i].card==id){sample=i;break;}
 if(sample<0){for(int i=0;i<8;i++)if(!draw_samples[i].card){sample=i;break;}}
 if(sample<0)sample=(int)(draw_sample_cursor++%8);
 draw_samples[sample].generation=++draw_generation;
 draw_samples[sample].card=id;draw_samples[sample].count=count;
 for(u32 i=0;i<count;i++){draw_samples[sample].rows[i].slot=rows[i].slot;draw_samples[sample].rows[i].primary=rows[i].primary;draw_samples[sample].rows[i].flags=rows[i].flags;for(int k=0;k<PROBE_NAMES;k++)for(int j=0;j<PROBE_CHARS;j++)draw_samples[sample].rows[i].names[k][j]=rows[i].names[k][j];}
 draw_samples[sample].generation=++draw_generation;drop();
}

static void observe_draw_mesh(void*actor,void*mesh){
 if(!actor||!mesh||!probe_card(*(uptr*)((char*)actor+0x10b0)))return;int slot=-1;
 for(int i=0;i<16;i++)if(draw_owners[i].actor==actor){slot=i;break;}
 if(slot<0)slot=(int)(draw_cursor++%16);draw_owners[slot].actor=actor;draw_owners[slot].mesh=mesh;draw_owners[slot].tick=0;inspect_head_draw(actor,mesh);
}
static void observe_draw_bake(void*actor){
 if(!actor||!enabled)return;
 for(int i=0;i<16;i++)if(draw_owners[i].actor==actor){if((++draw_owners[i].tick&255)==0)inspect_head_draw(actor,draw_owners[i].mesh);break;}
}
__attribute__((visibility("default"))) u32 noodle_draw_value(u32 sample,u32 row,u32 field){
 if(sample>=8||!take())return 0;u32 v=0;
 if(row==PROBE_ROWS){if(field==0)v=(u32)draw_samples[sample].card;else if(field==1)v=(u32)(draw_samples[sample].card>>32);else if(field==2)v=draw_samples[sample].count;else if(field==3)v=draw_samples[sample].generation;}
 else if(row<draw_samples[sample].count){if(field==0)v=draw_samples[sample].rows[row].slot;else if(field==1)v=draw_samples[sample].rows[row].primary;else if(field==2)v=draw_samples[sample].rows[row].flags;}
 drop();return v;
}
__attribute__((visibility("default"))) u32 noodle_draw_char(u32 sample,u32 row,u32 field,u32 index){u32 v=0;if(sample<8&&row<PROBE_ROWS&&field<PROBE_NAMES&&index<PROBE_CHARS&&take()){if(row<draw_samples[sample].count)v=draw_samples[sample].rows[row].names[field][index];drop();}return v;}

__attribute__((visibility("default"))) const u16*noodle_draw_text(u32 sample,u32 row,u32 field){if(sample>=8||row>=PROBE_ROWS||field>=PROBE_NAMES)return 0;return (const u16*)draw_samples[sample].rows[row].names[field];}
