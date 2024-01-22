#include <stdio.h>
#include <stdlib.h>
#include <strings.h>
#include <ctype.h>

int main()
{
    int a='A', c;
    char command[256], filename[256], ext[20], arcdir[80], cdir[256];
    char *p1=NULL, *p2=NULL;
    char CrPictures=0, CrEXEs=0, CrARCs=0, CrWTFs=0, CrGIFs=0, CrDOCs=0, CrPDFs=0, CrTorrents=0, Cr=0;
    filename[0]='"';
    strcpy(arcdir, "\"m:\\Archive\\Downloads\\Downloads - undated");
    strcpy(command, "dir c:\\Users\\Icee\\Downloads /a-d /b > Filesorter-tmp");
    system(command);
    FILE *Tmpf;
    Tmpf=fopen("Filesorter-tmp", "r");
    while(a!=EOF){
        ///---------------------------------------------------------------------------------
        c=1;
        a=fgetc(Tmpf);
        while((a!='\n')&&(a!=EOF)){
            if((a>=0x80)&&(a<0xB0)){
                a+=0x40;
            }
            else if((a>=0xE0)&&(a<0xF0)){
                a+=0x10;
            }
            filename[c]=a;
            c++;
            a=fgetc(Tmpf);
        }
        filename[c]='"';
        filename[c+1]='\0';
        if(strlen(filename)==2){
            printf("\nDone.\n");
            break;
        }
        ///---------------------------------------------------------------------------------
        p1=filename;
        while((p1=strstr(p1, "."))!=NULL){
            p2=p1;
            p1++;
        }
        if(p2!=NULL){
            strcpy(ext, (p2+1));
            ext[(strstr(ext, "\"")-ext)]='\0';
            c=0;
            while(ext[c]!='\0'){
                ext[c]=tolower(ext[c]);
                c++;
            }
        }
        //printf("\n%s - %s\n", filename, ext);
        ///---------------------------------------------------------------------------------
        Cr=0;
        if((strcmp(ext, "jpg")==0)||(strcmp(ext, "jpeg")==0)||(strcmp(ext, "png")==0)||(strcmp(ext, "tga")==0)||(strcmp(ext, "bmp")==0)){
            strcpy(cdir, arcdir);
            strcat(cdir, "\\Pictures\"");
            if(CrPictures==0){
                CrPictures=1;
                Cr=1;
            }
        }
        else if((strcmp(ext, "gif")==0)){
            strcpy(cdir, arcdir);
            strcat(cdir, "\\GIFs\"");
            if(CrGIFs==0){
                CrGIFs=1;
                Cr=1;
            }
        }
        else if((strcmp(ext, "exe")==0)){
            strcpy(cdir, arcdir);
            strcat(cdir, "\\EXEs\"");
            if(CrEXEs==0){
                CrEXEs=1;
                Cr=1;
            }
        }
        else if((strcmp(ext, "zip")==0)||(strcmp(ext, "rar")==0)||(strcmp(ext, "7z")==0)){
            strcpy(cdir, arcdir);
            strcat(cdir, "\\ARCs\"");
            if(CrARCs==0){
                CrARCs=1;
                Cr=1;
            }
        }
        else if((strcmp(ext, "pdf")==0)){
            strcpy(cdir, arcdir);
            strcat(cdir, "\\PDFs\"");
            if(CrPDFs==0){
                CrPDFs=1;
                Cr=1;
            }
        }
        else if((strcmp(ext, "doc")==0)||(strcmp(ext, "docx")==0)||(strcmp(ext, "xls")==0)||(strcmp(ext, "ppt")==0)){
            strcpy(cdir, arcdir);
            strcat(cdir, "\\DOCs\"");
            if(CrDOCs==0){
                CrDOCs=1;
                Cr=1;
            }
        }
        else if((strcmp(ext, "torrent")==0)){
            strcpy(cdir, arcdir);
            strcat(cdir, "\\Torrents\"");
            if(CrTorrents==0){
                CrTorrents=1;
                Cr=1;
            }
        }
        else{
            strcpy(cdir, arcdir);
            strcat(cdir, "\\WTFs\"");
            if(CrWTFs==0){
                CrWTFs=1;
                Cr=1;
            }
        }
        if(Cr==1){
           strcpy(command, "mkdir ");
            strcat(command, cdir);
            //printf(">> %s\n", command);
            system(command);
        }
        ///---------------------------------------------------------------------------------
        strcpy(command, "move \"c:\\Users\\Icee\\Downloads\\");
        strcat(command, (filename+1));
        strcat(command, " ");
        strcat(command, cdir);
        //printf(">> %s\n", command);
        system(command);
        ///---------------------------------------------------------------------------------
        //getchar();
    }
    fclose(Tmpf);
    strcpy(command, "del /q Filesorter-tmp");
    system(command);
    return(0);
}
