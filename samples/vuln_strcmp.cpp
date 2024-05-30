#include <iostream>
#include <cstring>

using namespace std;



int main()
{
    const char *pass = "PING20241337";
    char input[100];
    cout << "Enter the password: ";
    cin >> input;
    if (strcmp(pass, input) == 0)
    {
        cout << "Correct password" << endl;
    }
    else
    {
        cout << "Incorrect password" << endl;
    }  
    return 0;
 
}