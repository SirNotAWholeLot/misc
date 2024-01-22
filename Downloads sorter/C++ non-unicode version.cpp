#include <iostream>
#include <fstream>
#include <cstdlib>
#include <cwctype>
#include <clocale>

// An attempt to make C++ version work again on a new C::B install after disc cleanup
// Non-unicode version, seems to be working fine with codepage 1251

//using namespace std; // <- one anon said it's bad

int main()
{
    //std::cout << ">> Init start" << std::endl;
    std::string arcdir;
    std::string command;
    std::string filename;
    std::string ext;
    std::string cdir;
    char CrPictures=0, CrEXEs=0, CrARCs=0, CrWTFs=0, CrGIFs=0, CrDOCs=0, CrTorrents=0, Cr=0;
    arcdir = "\"k:\\Archive\\_Data\\Downloads\\Downloads - NEW";
    system("chcp 1251");
    system("dir c:\\Users\\Iri\\Downloads /a-d /b > k:\\Archive\\_Data\\Downloads\\Filesorter_tmp");
    std::ifstream dir_file("k:\\Archive\\_Data\\Downloads\\Filesorter_tmp", std::ios::in);
    std::ofstream bat_file;
    bat_file.open("k:\\Archive\\_Data\\Downloads\\Filesorter_exec.ps1", std::ios::out);
    while( (std::getline(dir_file, filename, '\n')) ){
        ///---------------------------------------------------------------------------------
        Cr=0;
        if((filename.rfind(".jpg")!=std::string::npos)
           ||(filename.rfind(".jpeg")!=std::string::npos)
           ||(filename.rfind(".png")!=std::string::npos)
           ||(filename.rfind(".tga")!=std::string::npos)
           ||(filename.rfind(".bmp")!=std::string::npos)){
            cdir = arcdir + "\\Pictures\"";
            if(CrPictures==0){
                CrPictures=1;
                Cr=1;
            }
        }
        else if((filename.rfind(".gif")!=std::string::npos)
                ||(filename.rfind(".webm")!=std::string::npos)
                ||(filename.rfind(".mp4")!=std::string::npos)){
            cdir = arcdir + "\\GIFs and videos\"";
            if(CrGIFs==0){
                CrGIFs=1;
                Cr=1;
            }
        }
        else if((filename.rfind(".exe")!=std::string::npos)){
            cdir = arcdir + "\\EXEs\"";
            if(CrEXEs==0){
                CrEXEs=1;
                Cr=1;
            }
        }
        else if((filename.rfind(".zip")!=std::string::npos)
                ||(filename.rfind(".rar")!=std::string::npos)
                ||(filename.rfind(".7z")!=std::string::npos)){
            cdir = arcdir + "\\ARCs\"";
            if(CrARCs==0){
                CrARCs=1;
                Cr=1;
            }
        }
        else if((filename.rfind(".doc")!=std::string::npos)
                ||(filename.rfind(".docx")!=std::string::npos)
                ||(filename.rfind(".xls")!=std::string::npos)
                ||(filename.rfind(".xlsx")!=std::string::npos)
                ||(filename.rfind(".ppt")!=std::string::npos)
                ||(filename.rfind(".pdf")!=std::string::npos)){
            cdir = arcdir + "\\DOCs\"";
            if(CrDOCs==0){
                CrDOCs=1;
                Cr=1;
            }
        }
        else if((filename.rfind(".torrent")!=std::string::npos)){
            cdir = arcdir + "\\Torrent files\"";
            if(CrTorrents==0){
                CrTorrents=1;
                Cr=1;
            }
        }
        else{
            cdir = arcdir + "\\WTFs\"";
            if(CrWTFs==0){
                CrWTFs=1;
                Cr=1;
            }
        }
        ///---------------------------------------------------------------------------------
        if(Cr==1){
            command = "mkdir " + cdir;
            //std::cout << ">> mkdiring: " << command << std::endl;
            system(command.c_str());
        }
        ///---------------------------------------------------------------------------------
        command = "mv \"c:\\Users\\Iri\\Downloads\\" + filename + "\" " + cdir;    // cygwin mv for no feedback -> speedup
        //std::cout << ">> " << command << std::endl;
        bat_file << command << std::endl;
        ///---------------------------------------------------------------------------------
    }
    std::cout << std::endl << "Parsing complete." << std::endl;
    dir_file.close();
    bat_file.close();
    system("Powershell k:\\Archive\\_Data\\Downloads\\Filesorter_exec.ps1");
    system("del /q k:\\Archive\\_Data\\Downloads\\Filesorter_tmp");
    system("del /q k:\\Archive\\_Data\\Downloads\\Filesorter_exec.ps1");
    std::cout << std::endl << "Done." << std::endl;
    return(0);
}
