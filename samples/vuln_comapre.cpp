#include <iostream>
#include <string>

using namespace std;



int main()
{
    string pass = "PING20241337";
    string input = "";
    cout << "Enter the password: ";
    cin >> input;
    if (pass.compare(input) == 0)
    {
        cout << "Correct password" << endl;
    }
    else
    {
        cout << "Incorrect password" << endl;
    }  
    return 0;
 
}