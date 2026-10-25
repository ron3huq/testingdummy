typedef unsigned long U;typedef unsigned int I;typedef unsigned short H;typedef struct{H*data;I num,cap;}Str;
static U args[6],common_count;static H input[200],output[220];static int input_n,output_n;static U(*path_hook)(void*,const H*,int);static int(*text_hook)(void*,I);static I msg,text_mode;static unsigned char label[24];
__attribute__((visibility("default"))) void prepare(U path,U text,I message,I mode){path_hook=(void*)path;text_hook=(void*)text;msg=message;text_mode=mode;}
__attribute__((visibility("default"))) void set_path(const H*p,I n){for(I i=0;i<n;i++)input[i]=p[i];input_n=n;}
__attribute__((visibility("default"))) U record_path(void*out,const H*p,int n){(void)out;output_n=n;for(int i=0;i<n&&i<219;i++)output[i]=p[i];output[n<219?n:219]=0;return 777;}
__attribute__((visibility("default"))) void detail(void*a,I model,I sleeve,I variant,I mode,I flag){args[0]=(U)a;args[1]=model;args[2]=sleeve;args[3]=variant;args[4]=mode;args[5]=flag;if(path_hook)path_hook(0,input,input_n);}
__attribute__((visibility("default"))) void common(void*a,I model,I sleeve,I variant,I mode,I flag){common_count++;detail(a,model,sleeve,variant,mode,flag);}
__attribute__((visibility("default"))) U value(I i){if(i<6)return args[i];if(i==6)return common_count;if(i==7)return(U)output;if(i==8)return output_n;if(i==9)return(U)label;return 0;}
__attribute__((visibility("default"))) int original_text(void*out,I id){(void)id;unsigned char*b=out;for(int i=0;i<24;i++)b[i]=0;if(text_mode){const char*p="Native text";b[0]=22;for(int i=0;i<11;i++)b[i+1]=p[i];return 1;}return 0;}
__attribute__((visibility("default"))) void original_page(void*widget,U id){(void)widget;(void)id;text_hook(label,msg);}
__attribute__((visibility("default"))) void build(void*out,const void*spec){(void)out;(void)spec;}
static H logo_data[240];
__attribute__((visibility("default"))) void write_logo(void*key,I size,I theme,Str*out){(void)key;(void)theme;const char*p=size==1?"Texture2D'/Game/Assets/ui/Data/Symbol/EmblemLC/emb_0473_f_s.emb_0473_f_s'":size==2?"/Game/Assets/ui/Data/Symbol/EmblemLC/emb_0473_f_l.emb_0473_f_l":"/Game/Assets/ui/Data/Symbol/EmblemLC/emb_0473_f.emb_0473_f";int i=0;while(p[i]){logo_data[i]=p[i];i++;}logo_data[i]=0;out->data=logo_data;out->num=i+1;out->cap=240;}
__attribute__((visibility("default"),naked)) void original_logo(void){__asm__ volatile("mov x3,x8\nb write_logo");}
