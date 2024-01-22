#include <iostream>
#include <fstream>
//#include <cstdlib>
//#include <cwctype>
//#include <clocale>
//#include <locale>
//#include <codecvt>
#include <sstream>

// An attempt to make C++ version work again on a new C::B install after disc cleanup
// Apparently it has to understand unicode to work properly with non-ascii chars

//using namespace std; // <- one anon said it's bad

int main()
{
    // I'll need widestrings for unicode - that is, for file names and commands, but how do I type into the damn things!?
    // Everything has to be wstring if I don't want to deal with convertion issues, but I can't = a wstring with "string"
    // For now, let's try without unicode to figure out what's wrong with getline()
    // UPDATE: non-Unicode version seem to be working on simple files, getline() bugged out because of the line in the file
    std::wstring arcdir;
    std::wstring command;
    std::wstring filename;
    std::wstring ext;
    std::wstring cdir;
    std::size_t dir_file_size;
    wchar_t temp_c;
    char CrPictures=0, CrEXEs=0, CrARCs=0, CrWTFs=0, CrGIFs=0, CrDOCs=0, CrTorrents=0, Cr=0;
    arcdir = L"\"k:\\Archive\\_Data\\Downloads\\Downloads - undated";
    system("chcp 1200");
    system("dir c:\\Users\\Icee\\Downloads /a-d /b > Filesorter_tmp");
    /*// Now this, THIS IS HORRIBLE
    system("for %I in (Filesorter-tmp) do @echo %~zI > Size_file");
    std::ifstream size_file("Size_file", std::ios::in);
    std::string size_string;
    std::getline(size_file, size_string);
    dir_file_size = std::stoi(size_string);
    //*/
    // Debug - putting all commands into a file instead
    std::wofstream command_file("Commands_debug", std::ios::binary);
    std::ifstream dir_file("Filesorter_tmp", std::ios::binary);
    ///---------------------------------------------------------------------------------
    // New method: readstupid, stackoverflow code
    // SO: skip BOM
    //dir_file.seekg(2);    // apparently there's no BOM

    // SO: read as raw bytes
    std::stringstream temp_ss;
    temp_ss << dir_file.rdbuf();
    std::string temp_bytes = temp_ss.str();    // so this shit comverts from stream to string
    std::cout << temp_bytes;

    // SO: make sure len is divisible by 2
    dir_file_size = temp_bytes.size();
    std::cout << dir_file_size << "\n";
    if(dir_file_size % 2) dir_file_size--;

    std::wstring file_wstring;
    for(size_t i = 0; i < dir_file_size;){
        // SO: little-endian
        int lo = temp_bytes[i++] & 0xFF;
        int hi = temp_bytes[i++] & 0xFF;
        file_wstring.push_back(hi << 8 | lo);
    }
    std::wcout << file_wstring;
    // Now the whole file should be in file_wstring. The problem is, how do I read a bloody wstring!?
    ///---------------------------------------------------------------------------------
    for(size_t i = 0; i < dir_file_size;){
        temp_c = file_wstring[i];
        if(temp_c != L'\n'){
            filename += temp_c;
        }
        else{
            ///---------------------------------------------------------------------------------
            Cr=0;
            if((filename.rfind(L".jpg")!=std::string::npos)
               ||(filename.rfind(L".jpeg")!=std::string::npos)
               ||(filename.rfind(L".png")!=std::string::npos)
               ||(filename.rfind(L".tga")!=std::string::npos)
               ||(filename.rfind(L".bmp")!=std::string::npos)){
                cdir = arcdir + L"\\Pictures\"";
                if(CrPictures==0){
                    CrPictures=1;
                    Cr=1;
                }
            }
            else if((filename.rfind(L".gif")!=std::string::npos)){
                cdir = arcdir + L"\\GIFs\"";
                if(CrGIFs==0){
                    CrGIFs=1;
                    Cr=1;
                }
            }
            else if((filename.find(L"exe")!=std::string::npos)){
                cdir = arcdir + L"\\EXEs\"";
                if(CrEXEs==0){
                    CrEXEs=1;
                    Cr=1;
                }
            }
            else if((filename.find(L".zip")!=std::string::npos)
                    ||(filename.find(L".rar")!=std::string::npos)
                    ||(filename.find(L".7z")!=std::string::npos)){
                cdir = arcdir + L"\\ARCs\"";
                if(CrARCs==0){
                    CrARCs=1;
                    Cr=1;
                }
            }
            else if((filename.find(L".doc")!=std::string::npos)
                    ||(filename.find(L".docx")!=std::string::npos)
                    ||(filename.find(L".xls")!=std::string::npos)
                    ||(filename.find(L".xlsx")!=std::string::npos)
                    ||(filename.find(L".ppt")!=std::string::npos)
                    ||(filename.find(L".pdf")!=std::string::npos)){
                cdir = arcdir + L"\\DOCs\"";
                if(CrDOCs==0){
                    CrDOCs=1;
                    Cr=1;
                }
            }
            else if((filename.find(L".torrent")!=std::string::npos)){
                cdir = arcdir + L"\\Torrent files\"";
                if(CrTorrents==0){
                    CrTorrents=1;
                    Cr=1;
                }
            }
            else{
                cdir = arcdir + L"\\WTFs\"";
                if(CrWTFs==0){
                    CrWTFs=1;
                    Cr=1;
                }
            }
            if(Cr==1){
                command = L"mkdir " + cdir;
                //std::cout << ">> mkdiring: " << command << std::endl;
                //system(command.c_str());
                command_file << command;    // Debug - write command into file instead
            }
            ///---------------------------------------------------------------------------------
            command = L"mv \"c:\\Users\\Icee\\Downloads\\" + filename + L"\" " + cdir;    // cygwin mv for no feedback -> speedup
            //std::cout << ">> " << command << std::endl;
            //system(command.c_str());
            command_file << command;    // Debug - write command into file instead
            ///---------------------------------------------------------------------------------
            filename.clear();
        }
    }
    std::cout << std::endl << "Done." << std::endl;
    system("del /q Filesorter_tmp");
    system("pause");
    return(0);
}
